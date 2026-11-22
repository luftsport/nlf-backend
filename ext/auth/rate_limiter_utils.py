from datetime import datetime, timedelta, timezone
from flask import request, g, current_app as app
from ext.app.decorators import _require_token, _require_client_access_token
from ext.scf import RATE_LIMITER_PENALTY_TIERS, RATE_LIMITER_MAX_STRIKES, RATE_LIMITER_CLAMPED_RESOURCES, RATE_LIMITER_DEFAULT_HIGH_LIMIT
from pymongo import ReturnDocument

_indexes_initialized = False


def get_current_resource():
    """Extract the Eve resource name (e.g., 'categories') from request.endpoint."""
    if not request.endpoint:
        return None
    # Eve formats endpoints as '<resource>|resource' or '<resource>|item'
    return request.endpoint.split('|')[0]


def dynamic_rate_limit():
    now = datetime.now(timezone.utc)
    penalty = get_penalty_collection().find_one({
        **get_penalty_filter(),
        "expires_at": {"$gt": now}
    })

    # 1. Active penalty always overrides resource limits
    if penalty:
        strikes = min(penalty.get("strikes", 1), RATE_LIMITER_MAX_STRIKES)
        return RATE_LIMITER_PENALTY_TIERS[strikes]

    # 2. Check if this DOMAIN resource is in your clamped-down list
    resource = get_current_resource()
    if resource in RATE_LIMITER_CLAMPED_RESOURCES:
        return RATE_LIMITER_CLAMPED_RESOURCES[resource]

    # 3. Generous default for all other resources
    return RATE_LIMITER_DEFAULT_HIGH_LIMIT


def get_penalty_collection():
    """Return the MongoDB penalty collection and ensure TTL + lookup indexes exist once."""
    global _indexes_initialized
    db = app.data.driver.db
    col = db['rate_penalties']
    if not _indexes_initialized:
        col.create_index("expires_at", expireAfterSeconds=0)
        col.create_index("person_id", sparse=True)
        col.create_index("ip", sparse=True)
        _indexes_initialized = True

    return col


def get_rate_limit_key():
    """Key function for Flask-Limiter (still needs a single string identifier)."""
    resolve_current_user()
    if getattr(g, 'id', None):
        return f"person:{g.id}"
    return f"ip:{request.remote_addr}"


def is_exempt_user():
    """Return True if the authenticated user is a client with valid token"""
    person_id = getattr(g, 'id', None)
    if person_id is None:
        return False

    try:
        return int(person_id) < 0
    except (ValueError, TypeError):
        return False


def get_user_or_ip():
    """Return the person_id if authenticated, otherwise the IP address."""
    try:
        _ = _require_token()
    except:
        try:
            _ = _require_client_access_token()
        except:
            return request.remote_addr

    if getattr(g, 'id', None):
        return g.id
    return request.remote_addr


def get_penalty_filter():
    """Build the MongoDB query filter using person_id if authenticated, otherwise ip."""
    r = get_user_or_ip()
    if isinstance(r, int):
        return {"person_id": r}
    return {"ip": r}


def dynamic_rate_limit_legacy():
    """Return the rate limit corresponding to the user's current active strike tier."""
    now = datetime.now(timezone.utc)
    query = {
        **get_penalty_filter(),
        "expires_at": {"$gt": now}
    }

    penalty = get_penalty_collection().find_one(query)

    if penalty:
        strikes = penalty.get("strikes", 1)
        # Cap at the highest tier (Tier 3: "5 per day") for 3 or more strikes
        tier = min(strikes, max(RATE_LIMITER_PENALTY_TIERS.keys()))
        return RATE_LIMITER_PENALTY_TIERS[tier]

    return "5 per minute"


def issue_penalty(seconds=86400, reason="rate_limit_exceeded"):
    """Increment strikes up to RATE_LIMITER_MAX_STRIKES (3) and set a 24-hour expiration window."""

    if is_exempt_user():
        return 0, "exempt", datetime.now(timezone.utc)

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=seconds)
    identity_filter = get_penalty_filter()
    col = get_penalty_collection()

    existing = col.find_one(identity_filter)

    # Check if an existing penalty is still active
    if existing and existing.get("expires_at"):
        existing_exp = existing["expires_at"]
        if existing_exp.tzinfo is None:
            existing_exp = existing_exp.replace(tzinfo=timezone.utc)

        if existing_exp > now:
            # Already at max lockout (Strike 3): do NOT reset their 24h timer on every retry
            if existing.get("strikes", 1) >= RATE_LIMITER_MAX_STRIKES:
                return RATE_LIMITER_MAX_STRIKES, RATE_LIMITER_PENALTY_TIERS[RATE_LIMITER_MAX_STRIKES], existing_exp

            # Otherwise escalate to the next strike and start a fresh 24-hour window
            doc = col.find_one_and_update(
                identity_filter,
                {
                    "$inc": {"strikes": 1},
                    "$set": {
                        "expires_at": expires_at,
                        "reason": reason,
                        "updated_at": now
                    }
                },
                return_document=ReturnDocument.AFTER
            )
            strikes = min(doc.get("strikes", 1), RATE_LIMITER_MAX_STRIKES)
            return strikes, RATE_LIMITER_PENALTY_TIERS[strikes], expires_at

    # New penalty or previously expired penalty -> start fresh at Strike 1
    doc = col.find_one_and_update(
        identity_filter,
        {
            "$set": {
                "strikes": 1,
                "expires_at": expires_at,
                "reason": reason,
                "updated_at": now,
                "created_at": now
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return 1, RATE_LIMITER_PENALTY_TIERS[1], expires_at
