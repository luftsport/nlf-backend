"""
Lungo functions defined here
"""
import requests
from ext.scf import ECCAIRS2_USER, ECCAIRS2_PASSWD
from functools import wraps
import inspect
import os
import time
from ext.app.responseless_decorators import _async
import socketio
from ext.scf import SOCKET_IO_TOKEN, SOCKET_IO_PORT, SOCKET_IO_HOST
from settings import E5X_WORKING_DIR
# To be able to use this standalone
from flask import current_app as app, g

try:
    if app.config:
        pass
except:
    app = {'config': {'REQUESTS_VERIFY': False}}

BASE_URL = 'https://api.sandbox.aviationreporting.eu'
TOKEN_PATH = '/auth/api/token'
FILE_UPLOAD_PATH = '/frontfile-api/files/migrate'
FILE_UPLOAD_RESULT_PATH = '/frontfile-api/results/e5xresults'

SOCKET_MESSAGE_TEMPLATE = {'channel': '', }



def authenticate(f):
    @wraps(f)
    def wrapper(self, *args, **kw):
        if hasattr(self, '_authenticate') and inspect.ismethod(self._authenticate):
            self._authenticate()
        result = f(self, *args, **kw)
        return result

    return wrapper


@_async
def broadcast(title, message, style='success'):
    try:
        sio = socketio.Client()
        sio.connect(f'http://{SOCKET_IO_HOST}:{SOCKET_IO_PORT}/socket.io/?token={SOCKET_IO_TOKEN}')
        room = str(g.get('user_id'))
        sio.emit('join_room', room)
        sio.emit('message_room',
                 {
                     'title': title,
                     'message': message,
                     'room': room,
                     'style': style,
                     'action': 'obsreg_e5x_finished_processing'
                 }
                 )
        time.sleep(0.1)
        sio.disconnect()
    except:
        pass


class ECCAIRS2:
    HEADERS = None
    authenticated = False

    def __init__(self):
        pass

    def _authenticate(self):

        if self.authenticated is False:
            auth_url = f'{BASE_URL}{TOKEN_PATH}?grant_type=password&password={ECCAIRS2_PASSWD}&username={ECCAIRS2_USER}'
            r = requests.post(auth_url)
            if r.status_code == 200:
                result = r.json()
                token = result['access_token']
                self.HEADERS = {'Authorization': f'Bearer {token}'}

    @authenticate
    def e5x_file_upload(self, activity, obsreg_id, version, file_name):
        """
        Upload only supports one file at a time
        :param activity:
        :param obsreg_id:
        :param version:
        :param file_name:
        :return: status, eccairs2_id
        """
        eccairs2_id = None

        file_path = '{0}/{1}/{2}/{3}/{4}'.format(E5X_WORKING_DIR, activity, obsreg_id, version, file_name)
        files = {
            'files': (file_name, open(file_path, 'rb')),
        }
        """ @TODO remove Legacy
        json = {
            'pdfCode': '2',
        }
        """

        if os.path.exists:
            resp = requests.post(f'{BASE_URL}{FILE_UPLOAD_PATH}', files=files, headers=self.HEADERS)

            if resp.status_code in [200, 201]:  # Note ECCAIRS uses 200 not 201!
                try:
                    eccairs2_id = resp.json()['data']['files'][0]
                    self.get_results(eccairs2_id)
                except:
                    pass

                return True if eccairs2_id is not None else False, eccairs2_id, resp.json()

        return False, eccairs2_id, None

    def _get_results(self, eccairs2_id):
        finished = False
        max_retries = 10
        current_retries = 0
        delta = 5

        while finished is False:
            print('Trying to get result', current_retries + 1)
            # Get results of file migration process:

            resp = requests.get(
                f'{BASE_URL}{FILE_UPLOAD_RESULT_PATH}?format=json&idFile={eccairs2_id}&only-validation=false',
                headers=self.HEADERS
            )
            print(resp.json())
            if resp.status_code == 200 and resp.json().get('e5zE5xId', 0) > 0:
                print('SUCCESS!!')
                print(resp.json())
                finished = True
                result = resp.json()
                e2_id = result['reportInfoList'][0]['message'].replace('"', '')
                e5zE5xId = result['e5zE5xId']
                return True, e2_id, e5zE5xId, result
            else:
                current_retries += 1
                time.sleep(delta + current_retries)
                if current_retries >= max_retries:
                    finished = True
                    return False, None, None, None

    @_async
    def get_results(self, eccairs2_id):

        status, e2_id, e5zE5xId, result = self._get_results(eccairs2_id)

        if status is True:
            # Update obsreg?
            broadcast(title='E5X fil konvertert', message=f'E5X filen med id {eccairs2_id} ble konvertert til ECCAIRS2 format')
