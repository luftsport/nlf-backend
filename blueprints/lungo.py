"""
    Custom lungo passthrough route
    ==============================

    Basically a clean passthrough to Lungo

"""

from flask import Blueprint, request, current_app as app
from ext.scf import LUNGO_HEADERS, LUNGO_URL
from ext.app.eve_helper import eve_response, eve_abort
from ext.app.decorators import require_token
import requests

#LUNGO_URL = 'http://127.0.0.1:9191/api/v1'
# Supress insecre warning
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Lungo = Blueprint('Lungo passthrough', __name__, )


@Lungo.route("/syncdaemon/workers/start", methods=["POST"])
@require_token()
def syncdaemon_workers_start():
    resp = requests.post('{}/syncdaemon/workers/start'.format(LUNGO_URL),
                         data=None,
                         headers=LUNGO_HEADERS,
                         verify=app.config.get('REQUESTS_VERIFY', True))

    return eve_response(resp.json(), resp.status_code)


@Lungo.route("/syncdaemon/worker/reboot/<int:index>", methods=["POST"])
@require_token()
def lungo_worker_reboot(index):
    resp = requests.post('{}/syncdaemon/worker/reboot/{}'.format(LUNGO_URL, index),
                         data=None,
                         headers=LUNGO_HEADERS,
                         verify=app.config.get('REQUESTS_VERIFY', True))

    return eve_response(resp.json(), resp.status_code)


@Lungo.route("/nif/change/", methods=["POST"])
@require_token()
def lungo_change_message():
    data = request.get_json()
    resp = requests.post('{}/nif/change/'.format(LUNGO_URL),
                         json=data,
                         headers=LUNGO_HEADERS,
                         verify=app.config.get('REQUESTS_VERIFY', True))

    return eve_response(resp.json(), resp.status_code)


@Lungo.route("/", defaults={"path": ""}, methods=['GET'])
@Lungo.route("/<string:path>", methods=['GET'])
@Lungo.route("/<path:path>", methods=['GET'])
@require_token()
def lungo(path):
    resp = requests.get('{}/{}'.format(LUNGO_URL, path),
                        params=request.args.to_dict(),
                        headers=LUNGO_HEADERS,
                        verify=app.config.get('REQUESTS_VERIFY', True))

    try:
        return eve_response(resp.json(), resp.status_code)
    except Exception as e:
        app.logger.exception('Error in Lungo response')
        app.logger.error(resp.text)

    return eve_abort(502, 'Unknown error')
