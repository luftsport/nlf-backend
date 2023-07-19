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
