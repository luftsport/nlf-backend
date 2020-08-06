"""
    Eve compatible layer
    ====================
    
    Just a custom wrapper to resemble eve response for custom Flask endpoints
"""

from flask import jsonify, abort, Response, current_app as app
import sys
import json  # simplejson as json
import bson.json_util as json_util
from ..scf import Scf
from ext.app.eve_jsonencoder import EveJSONEncoder

from ext.notifications.sms import Sms  # Email

# from ext.app.decorators import async

CRITICAL_ERROR_CODES = [503]


def eve_abort(status=500, message='', sysinfo=None) -> Response:
    """Abort processing and logging
    @Param: code http code
    @Param: message string representation"""
    app.logger.error(status, message)
    try:
        status = int(status)
        if sysinfo == None:
            try:
                sysinfo = sys.exc_info()[0]
            except:
                pass

        if 100 <= status <= 299:
            # app.logger.info("%s: %s" % (message, sysinfo))
            pass
        elif 300 <= status <= 399:
            # app.logger.warn("%s: %s" % (message, sysinfo))
            pass
        elif 400 <= status <= 499:
            # app.logger.error("%s: %s" % (message, sysinfo))
            pass
        elif 500 <= status <= 599:
            # Check if mongo is down
            # app.logger.error("%s: %s" % (message, sysinfo))

            # 503 Service Unavailable
            if status in CRITICAL_ERROR_CODES:
                if not is_mongo_alive(status):
                    app.logger.critical("MongoDB is down")
                    send_sms(status, "MongoDB is down (%s)" % app.config['APP_INSTANCE'])
                else:
                    app.logger.critical(message)
                    send_sms(status, "%s (%s)" % (message, app.config['APP_INSTANCE']))

        else:
            # app.logger.debug("%s: %s" % (message, sysinfo))
            pass
    except:
        pass

    # Eve formatted abort
    # abort(status, message)

    # Using flask Response
    # resp = eve_response(message, status)
    # abort(status, resp)

    # If using this pattern, make sure all eve_abort is returned in situ!
    data = {'_status': 'ERR', '_error': {'code': status, 'message': message}}
    return eve_response(data=data, status=status)

    # Should never be reached:
    abort(500)

def eve_error_response(message, status):
    return eve_response(data={'_status': 'ERR', '_error': message}, status=status)


def eve_response(data={}, status=200):
    """Manually send a response like Eve
    Uses Flask's Response object
    def __init__(self, response=None, status=None, headers=None,mimetype=None, content_type=None, direct_passthrough=False):
    """

    if isinstance(data, dict):
        pass
    elif isinstance(data, list):
        data = {'_items': data}
    elif isinstance(data, int):
        data = {'data': data}
    elif isinstance(data, str):
        data = {'data': data}

    try:
        resp = Response(json.dumps(data, cls=EveJSONEncoder), status=status, mimetype='application/json')
        return resp
    except:
        data.update({'_not_flask_response': True})
        resp = jsonify(**data)
        return resp

    abort(500)


def eve_response_pppd(data={}, status=200, error_message=False):
    """Manually create a reponse for POST, PATCH, PUT, DELETE"""

    # Add status OK | ERR to data.
    if error_message is False:
        data.update({'_status': 'OK'})
    else:
        data.update({'_status': 'ERR'})
        data.update({'_error': error_message})

    return eve_response(data, status)


def eve_response_get(data={}, status=200, error_message=False):
    return eve_response(data, status)


def eve_response_post(data={}, status=200, error_message=False):
    return eve_response_pppd(data, status, error_message)


def eve_response_delete(data={}, status=200, error_message=False):
    return eve_response_pppd(data, status, error_message)


def eve_response_put(data={}, status=200, error_message=False):
    return eve_response_pppd(data, status, error_message)


def eve_response_patch(data={}, status=200, error_message=False):
    return eve_response_pppd(data, status, error_message)


def is_mongo_alive(status=502):
    try:
        app.data.driver.db.command('ping')
        return True
    except:
        send_sms(status, "Mongodb is down (%s)" % app.config['APP_INSTANCE'])
        return False


def send_sms(status, message):
    try:
        sms = Sms()
        config = Scf()
        sms.send(mobile=config.get_warn_sms(), message="[%s] %s" % (status, message))
    except:
        pass
