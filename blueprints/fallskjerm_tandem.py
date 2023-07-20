from flask import Blueprint, request, current_app as app, jsonify
from ext.scf import LUNGO_HEADERS, LUNGO_URL
from ext.app.eve_helper import eve_response, eve_abort
from ext.app.decorators import require_token

from nif_tools import tandem
from ext.scf import NIF_TOOLS_USER, NIF_TOOLS_PASSWD

FallskjermTandem = Blueprint('Fallskjerm - registrer tandemer fra csv fil', __name__, )


@FallskjermTandem.route("/search", methods=['GET'])
def search():
    allowed = ['first_name', 'last_name', 'mobile', 'email']
    params = {key: value for (key, value) in request.args.items() if key in allowed}

    nif = tandem.Tandem(NIF_TOOLS_USER, NIF_TOOLS_PASSWD)
    status, result = nif._search(params.get('first_name', ''), params.get('last_name', ''))
    return eve_response(result.get('SearchResults', []), status)


def _products(person_id):
    nif = tandem.Tandem(NIF_TOOLS_USER, NIF_TOOLS_PASSWD)
    status, result = nif.get_person_products(person_id)
    return status, result #eve_response(result, status)

@FallskjermTandem.route("/registered/<int:org_id>/<int:person_id>", methods=['GET'])
def person_has_tandem(person_id, org_id):
    status, products = _products(person_id)

    for v in products.get('Categories', []):
        if v['CategoryName'] == 'Unntak':
            for org in v['Orgs']:
                if org['ClubOrgId'] == org_id:
                    for p in org['Details']:
                        if p['ProductDetailId'] == 4 and p['Selected'] is True:
                            return eve_response({'person_id': person_id, 'org_id': org_id, 'tandem': True}, status)

    return eve_response({'person_id': person_id, 'org_id': org_id, 'tandem': False}, status)