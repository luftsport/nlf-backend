from flask import Blueprint, current_app as app

from ext.app.eve_helper import eve_abort, eve_response

# import base64
# from ext.auth.tokenauth import TokenAuth
# from ext.notifications.notifications import notify

Heartbeat = Blueprint('Heartbeat Blueprint', __name__, )


def _mongo():
    pass


def _lungo():
    pass


def auth():
    pass


@Heartbeat.route("/", methods=['GET'])
def heartbeat():
    try:

        # Mongo check
        info = int(app.data.driver.db.client.server_info().get('ok', 0))
        return eve_response({'_status': True, 'message': {'mongo': info}}, 200)
    except Exception as e:
        return eve_response({'_status': False, 'message': {'mongo': 0}}, 500)
