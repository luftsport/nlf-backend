"""
    Distinct field content in collection
    ====================================

"""

from flask import g, Blueprint, current_app as app, request, Response, abort, jsonify
from ext.app.eve_helper import eve_abort, eve_response
from ext.app.decorators import require_token
from importlib import import_module


# Search filter builder whitelist fields for
COLLECTIONS_WHITELIST = [
    'fallskjerm_observations',
    'motorfly_observations',
    'sportsfly_observations',
    'seilfly_observations'
]

Distinct = Blueprint('List distinct field values from collection', __name__, )


def _get_field_contents(collection, field):
    print('Get field contents distinct', collection, field)
    try:
        if collection in COLLECTIONS_WHITELIST:

            # Import domain file dynamically and get schema definition
            module = import_module('domain.{}'.format(collection))
            schema = getattr(module, 'definition')

            if field in schema.get('allowed_filters', []):
                col = app.data.driver.db[collection]

                values = list(col.distinct(field))

                if len(values) > 0 and isinstance(values[0], dict):
                    values = [list(x.keys()) for x in values]
                    values = list(set(sum(values, [])))

                return 200, values
    except Exception as e:
        print('Error field', field, e)

    return 403, None


@Distinct.route("/<string:collection>/<string:field>", methods=['GET'])
@require_token()
def get_field_contents(collection, field):
    status, values = _get_field_contents(collection, field)

    if status == 200:
        return eve_response(values)

    abort(403)

