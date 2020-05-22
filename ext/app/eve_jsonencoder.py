import json
from bson import ObjectId
from datetime import datetime
from dateutil import tz
from decimal import Decimal

LOCAL_TIMEZONE = 'UTC'

class EveJSONEncoder(json.JSONEncoder):
    """For all Eve special fields
    Note that self.tz_format needs to be in sync with DATE_FORMAT in eve settings.py
    """

    # Always assume non-tz aware is CET
    tz_local = tz.gettz(LOCAL_TIMEZONE)
    tz_utc = tz.gettz('UTC')

    # Eve's time format
    tz_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def default(self, o):

        if isinstance(o, ObjectId):
            """ObjectId to string"""
            return str(o)

        if isinstance(o, datetime):
            """TZ aware and non-aware datetime objects"""

            # Need to fix if year, month and day is 1
            if o.year == 1 and o.month == 1 and o.day == 1:
                o = datetime(1, 1, 1, 0, 0, 0).replace(tzinfo=self.tz_utc)

            if o.tzinfo is not None and o.tzinfo.utcoffset(o) is not None:
                """o is already timezone aware!"""
                pass

            elif o.tzinfo is None or o.tzinfo.utcoffset(o) is None:
                """o is naive, no timezone we assume CET"""

                o.replace(tzinfo=self.tz_local)

            # Always return as UTC in Zulu time
            return o.astimezone(self.tz_utc).strftime(self.tz_format)

        if isinstance(o, Decimal):
            return str(float(o))

        return json.JSONEncoder.default(self, o)
