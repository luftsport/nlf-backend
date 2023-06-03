"""
Lungo functions defined here
"""
import requests
from ext.scf import ECCAIRS2_M2M
from functools import wraps
import inspect
import os
import time
from ext.app.responseless_decorators import _async
import socketio
from ext.scf import SOCKET_IO_TOKEN, SOCKET_IO_PORT, SOCKET_IO_HOST
from settings import E5X_WORKING_DIR
from instance import APP_INSTANCE
# To be able to use this standalone
from flask import current_app as app, g

try:
    if app.config:
        pass
except:
    app = {'config': {'REQUESTS_VERIFY': False}}

BASE_URL = ECCAIRS2_M2M[APP_INSTANCE]['base_url']
TOKEN_PATH = '/auth/api/token'
FILE_UPLOAD_PATH = '/frontfile-api/files/migrate'
FILE_UPLOAD_RESULT_PATH = '/frontfile-api/results/e5xresults'
OCCURRENCE_GET_PATH = '/occurrences/get/'
OCCURRENCE_ORIGINAL_REPORT_PATH = '/occurrences/reporter/original-report'
OCCURRENCE_ORIGINAL_REPORT_PATH = '/occurrences/reporter/original-report'
OCCURRENCE_READABLE_PATH = '/occurrences/readable'
OCCURRENCE_READABLE_FIELD_PATH = '/occurrences/readable/fields'
TAXONOMY_PATH = '/taxonomy-service/released-taxonomy'
TAXANOMY_VALUE_PATH = '/taxonomy-service/listofvalue/valuelist'
TAXANOMY_VALUE_LIST_PATH = '/taxonomy/valueLists/public/'

ECCAIRS2_NLF_ID = 2169

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
def broadcast(title, message, room, activity, obsreg_id, style='success'):
    try:
        sio = socketio.Client()
        sio.connect(f'http://{SOCKET_IO_HOST}:{SOCKET_IO_PORT}/socket.io/', auth={'token': SOCKET_IO_TOKEN})
        # room = str(g.get('user_id'))
        # sio.emit('join_room', room) No need server user has access!
        sio.emit('action',
                 {
                     'title': title,
                     'message': message,
                     'style': style,
                     'action': 'obsreg_e5x_finished_processing',
                     'link': [activity, obsreg_id],
                     'room': room,
                     'autohide': False,
                     'delay': 60000
                 }
                 )
        time.sleep(0.1)
        sio.disconnect()
    except:
        pass


class ECCAIRS2:
    """
    All messages has
    All the methods responses have the same format
    {
    data response data
    errorDetails
    returnCode 1: OK, 2: ERROR
    }
    """
    HEADERS = None
    authenticated = False

    def __init__(self):
        pass

    def _authenticate(self) -> None:

        if self.authenticated is False:
            auth_url = f'{BASE_URL}{TOKEN_PATH}?grant_type=password&password={ECCAIRS2_M2M[APP_INSTANCE]["passwd"]}&username={ECCAIRS2_M2M[APP_INSTANCE]["user"]}'
            r = requests.post(auth_url)
            if r.status_code == 200:
                result = r.json()
                token = result['access_token']
                self.HEADERS = {'Authorization': f'Bearer {token}'}

    @authenticate
    def e5x_file_upload(self, activity, obsreg_id, version, file_name) -> (bool, int, dict):
        """
        Response "data":
        OCC_FBS_310: Your file has been successfully uploaded and is being processed.
        System messages:
        OCC_FBS_310: Your file has been successfully uploaded and is being processed.
        OCC_FBW_309: Your request has been queued. It may take a while to be completed. It will
        be automatically processed once the queue gets released.

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
                    self.get_results(eccairs2_id, g.get('user_id', 0), obsreg_id, activity)
                except:
                    pass

                return True if eccairs2_id is not None else False, eccairs2_id, resp.json()

        return False, eccairs2_id, None

    def _get_results(self, eccairs2_id) -> (bool, int, int, dict):
        """

        ERROR:
        migrationStatus': 'Processed with Errors', 'message': '"Error Unzipping File"'
        SUCCESS
        'migrationStatus': 'Successfully migrated', 'message': '"success"'

        :param eccairs2_id:
        :return:
        """
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
                eccairs2_id = result['reportInfoList'][0]['message'].replace('"', '')
                e5zE5xId = result['e5zE5xId']
                return True, eccairs2_id, e5zE5xId, result
            else:
                current_retries += 1
                time.sleep(delta + current_retries)
                if current_retries >= max_retries:
                    finished = True
                    return False, None, None, None

    @_async
    def get_results(self, eccairs2_id, user_id, obsreg_id, activity) -> None:

        status, eccairs2_id, e5zE5xId, result = self._get_results(eccairs2_id)

        if status is True:
            # Update obsreg?
            try:
                from settings import MONGO_DBNAME
                from pymongo import MongoClient
                client = MongoClient()
                db = client[MONGO_DBNAME]
                col = db[f'{activity}_observations']

                obsreg = col.find_one({'id': obsreg_id})
                elements = len(obsreg.get('e5x', {}).get('audit', []))
                if elements > 0:
                    last_element_index = elements - 1
                    _update = col.update_one({'id': obsreg_id},
                                             {'$set': {f'e5x.audit.{last_element_index}.eccairs2.result': result}})
            except Exception as e:
                print('ERR getting result {}'.format(e))

            broadcast(
                title=f'E5X fil konvertert for #{obsreg_id}',
                message=f'E5X filen for {activity} med id {obsreg_id} ble konvertert til ECCAIRS2 format med eccairs2 id {eccairs2_id}. Reload observasjonen for å se endringene i e5x',
                activity=activity,
                obsreg_id=obsreg_id,
                room=str(user_id)
            )

        else:
            broadcast(
                title=f'E5X fil for #{obsreg_id} feilet konvertering',
                message=f'E5X filen for {activity} med id {obsreg_id} feilet konvertering fra E5X fil til ECCAIRS2 format',
                activity=activity,
                obsreg_id=obsreg_id,
                room=str(user_id),
                style='danger'
            )

    def get_OR(self, eccairs2_id) -> (bool, dict):
        r = requests.get(f'{BASE_URL}{OCCURRENCE_GET_PATH}{eccairs2_id}', headers=self.HEADERS)

        if r.status_code == 200:
            return True, r.json()['data']

        return False, None

    def get_OR_list(self, max_results=1000, page=0) -> (bool, dict):

        params = {'$skip': page * max_results, '$top': max_results, '$orderby': 'creationDate desc'}
        json = {
            "status": [
                "SENT",
                "PROCESSED",
                "ARCHIVED",
                "DELETED"
            ]
        }
        r = requests.post(f'{BASE_URL}{OCCURRENCE_ORIGINAL_REPORT_PATH}', headers=self.HEADERS, params=params,
                          json=json)

        if r.status_code in [200, 201]:
            # data.elements|total
            # errorDetails': '',  'returnCode': 1
            results = r.json()
            return True, {'_items': results['data']['elements'],
                          '_meta': {'page': page, 'max_results': max_results, 'total': results['data']['total']}
                          }

        return False, None

    def get_taxonomy_version(self) -> (bool, dict):
        """

        :return: data (taxonomy)id|name|version
        """

        r = requests.get(f'{BASE_URL}{TAXONOMY_PATH}', headers=self.HEADERS)

        if r.status_code == 200:
            return True, r.json['data']

        return False, None

    def get_taxonomy_value_list(self, taxonomy_version=6) -> (bool, dict):

        r = requests.get(f'{BASE_URL}{TAXANOMY_VALUE_LIST_PATH}{taxonomy_version}', headers=self.HEADERS)
        if r.status_code == 200:
            result = r.json()
            return True, {
                '_items': result['data']['responseData']['list'],
                '_meta': {
                    'page': result['data']['responseData']['page'],
                    'max_results': result['data']['responseData']['pageSize'],
                    'total': result['data']['responseData']['totalRows']
                }
            }

        return False, None

    def get_taxonomy_options(self, value_id, taxonomy_version) -> (bool, list):

        r = requests.get(f'{BASE_URL}{TAXANOMY_VALUE_PATH}{value_id}/{taxonomy_version}', headers=self.HEADERS)

        if r.status_code == 200:
            result = r.json()
            return True, {
                '_items': result['data'],
                '_meta': {'page': 0, 'max_results': len(result['data']), 'total': len(result['data'])}
            }

        return False, None

    def get_readable_report(self, eccairs2_id) -> (bool, dict):

        r = requests.get(f'{BASE_URL}{OCCURRENCE_READABLE_PATH}/{eccairs2_id}', headers=self.HEADERS)
        if r.status_code == 200:
            result = r.json()
            return True, result['data']

        return False, None

    def get_readable_report_field(self, eccairs2_id, field_id) -> (bool, list):
        json = [field_id]
        r = requests.get(f'{BASE_URL}{OCCURRENCE_READABLE_FIELD_PATH}/{eccairs2_id}', json=json, headers=self.HEADERS)
        if r.status_code == 200:
            result = r.json()
            return True, result['data']

        return False, None
