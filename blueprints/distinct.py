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
    'seilfly_observations',
    'hps_observations',
    'modellfly_observations',
]

Distinct = Blueprint('List distinct field values from collection', __name__, )


def _get_field_contents(collection, field):

    try:
        if collection in COLLECTIONS_WHITELIST:

            # Import domain file dynamically and get schema definition
            module = import_module('domain.{}'.format(collection))
            schema = getattr(module, 'definition')

            # Note: Allowed filters are defined in the domain file schema definition, and is used by the search filter builder to know which fields to build filters for.
            # So if a field is in allowed filters, it should be safe to query distinct values for it.
            if field in schema.get('allowed_filters', []):
                col = app.data.driver.db[collection]

                values = list(col.distinct(field))

                if len(values) > 0 and isinstance(values[0], dict):
                    values = [list(x.keys()) for x in values]
                    values = list(set(sum(values, [])))
                elif len(values) > 0 and isinstance(values[0], list):
                    values = list(set([x for l in values for x in l]))

                return 200, values
    except Exception as e:
        app.logger.exception(f'Error fetching distinct values for field {field} in collection {collection}: {e}')

    return 403, None


@Distinct.route("/<string:collection>/<string:field>", methods=['GET'])
@require_token()
def get_field_contents(collection, field):
    status, values = _get_field_contents(collection, field)

    if status == 200:
        return eve_response(values)

    abort(403)
