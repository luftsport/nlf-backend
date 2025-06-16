from flask import g, Blueprint, current_app as app
from ext.app.decorators import require_token
from ext.app.eve_helper import eve_abort, eve_response

from eve.methods.get import get_internal

UserORS = Blueprint('Users ORSes', __name__, )


@UserORS.route("/<regex('(fallskjerm|motorfly|sportsfly|seilfly|modellfly)'):collection>", methods=['GET'])
@require_token()
def my_orses(collection):
    data = []
    status = 404
    try:
        person_id = g.user_id
        collection = '{}_observations'.format(collection)

        lookup = {
            '$or':
                [
                    {'involved.id': person_id},
                    {'organization.hfl.id': person_id},
                    {'organization.hm.id': person_id},
                    {'organization.hl.id': person_id},
                    {'organization.pilot.id': person_id},
                    {'aircrafts.crew.person': person_id}
                ],
            'workflow.state': {'$in': ['closed']}
        }

        response, _, _, status, _ = get_internal(collection, **lookup)
        if status == 200:
            data = [
                {
                    'id': x['id'],
                    'title': '/'.join(x['tags']),
                    'discipline': x['discipline'],
                    'state': x['workflow']['state'],
                    'type': x['type'],
                    'when': x.get('when', None),
                    'rating': x.get('rating', {})
                } for x in response.get('_items', [])
            ]
    except Exception as e:
        pass
    
    return eve_response(data, status)
