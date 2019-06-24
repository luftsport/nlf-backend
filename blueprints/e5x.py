from flask import Blueprint, current_app as app, request, Response, abort, jsonify, send_file
from bson import json_util
import simplejson as json
import subprocess
from pprint import pprint
import os
import datetime
import time
from gridfs import GridFS
from gridfs.errors import NoFile
from bson.objectid import ObjectId

from ext.app.decorators import *
from ext.app.eve_helper import eve_abort, eve_response

import base64
from ext.auth.tokenauth import TokenAuth
from ext.notifications.notifications import notify

E5X = Blueprint('E5X Blueprint', __name__, )


# ID = '49'
# VERSION = '6'
# ACTIVITY = 'motorfly'

# FILE_NAME = 'nlf_{}_{}_v{}'.format(ACTIVITY, ID, VERSION)

# @TODO add version to dir motorfly/49/6/filer...
# E5X_WORKING_DIR_FILES = '{}/{}/{}'.format(E5X_WORKING_DIR, ACTIVITY, ID)
# DATA = {}
# JSON_FILE = '{}/{}/{}/{}.json'.format(E5X_WORKING_DIR, ACTIVITY, ID, FILE_NAME)
# XML_FILE = '{}/{}/{}/{}.xml'.format(E5X_WORKING_DIR, ACTIVITY, ID, FILE_NAME)
# E5X_FILE = '{}/{}/{}/{}.e5x'.format(E5X_WORKING_DIR, ACTIVITY, ID, FILE_NAME)

def has_permission():
    print(request.args)
    try:

        b64token = request.args.get('token', default=None, type=str)
        token = base64.b64decode(b64token)[:-1]
        auth = TokenAuth()

        if not auth.check_auth(token=token.decode("utf-8"),
                               method=request.method,
                               resource=request.path[len(app.globals.get('prefix')):],
                               allowed_roles=None):
            eve_abort(404, 'Please provide proper credentials')

    except:
        eve_abort(404, 'Please provide proper credentials')
    return True


def execute(cmdArray, workingDir):
    stdout = ''
    stderr = ''

    try:
        try:
            process = subprocess.Popen(cmdArray, cwd=workingDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       bufsize=1)
        except OSError:
            return [False, '', 'ERROR : command(' + ' '.join(cmdArray) + ') could not get executed!']

        for line in iter(process.stdout.readline, b''):

            try:
                echoLine = line.decode("utf-8")
            except:
                echoLine = str(line)

            stdout += echoLine

        for line in iter(process.stderr.readline, b''):

            try:
                echoLine = line.decode("utf-8")
            except:
                echoLine = str(line)

            stderr += echoLine

    except (KeyboardInterrupt, SystemExit) as err:
        return [False, '', str(err)]

    process.stdout.close()

    returnCode = process.wait()
    if returnCode != 0 or stderr != '':
        return [False, stdout, stderr]
    else:
        return [True, stdout, stderr]


def generate_structure(activity, ors_id, version):
    try:
        if os.path.exists('{}/{}/{}/{}'.format(app.config['E5X_WORKING_DIR'], activity, ors_id, version)) is False:

            if os.path.exists('{}/{}/{}'.format(app.config['E5X_WORKING_DIR'], activity, ors_id)) is False:

                if os.path.exists('{}/{}'.format(app.config['E5X_WORKING_DIR'], activity)) is False:
                    _, stdout, stderr = execute(['mkdir', activity], app.config['E5X_WORKING_DIR'])

                _, stdout, stderr = execute(['mkdir', '{}/{}'.format(activity, ors_id)], app.config['E5X_WORKING_DIR'])

            _, stdout, stderr = execute(['mkdir', '{}/{}/{}'.format(activity, ors_id, version)],
                                        app.config['E5X_WORKING_DIR'])
        return True
    except:
        return False


@E5X.route("/generate/<objectid:_id>", methods=['POST'])
@require_token()
def generate(_id):
    data = request.get_json(force=True)
    col = app.data.driver.db['motorfly_observations']
    # db.companies.find().skip(NUMBER_OF_ITEMS * (PAGE_NUMBER - 1)).limit(NUMBER_OF_ITEMS )
    cursor = col.find({'$and': [{'_etag': data.get('_etag', None), '_id': _id},
                                {'$or': [{'acl.execute.users': {'$in': [app.globals['user_id']]}},
                                         {'acl.execute.roles': {'$in': app.globals['acl']['roles']}}]}]})
    total_items = cursor.count()

    # _items = list(cursor.sort(sort['field'], sort['direction']).skip(max_results * (page - 1)).limit(max_results))
    _items = list(cursor)

    if (len(_items) == 1):
        # print(_items)
        ors = _items[0]

        FILE_WORKING_DIR = '{}/{}/{}/{}'.format(app.config['E5X_WORKING_DIR'], 'motorfly', ors.get('id'),
                                                ors.get('_version'))

        file_name = 'nlf_{}_{}_v{}'.format(ors.get('_model', {}).get('type', None), ors.get('id'),
                                           ors.get('_version'))

        if generate_structure(ors.get('_model', {}).get('type', None), ors.get('id'), ors.get('_version')) is True:
            # Process files!
            file_list = []
            if len(ors.get('files', [])) > 0:
                col_files = app.data.driver.db['files']

                for key, _file in enumerate(ors.get('files', [])):
                    file = col_files.find_one({'_id': ObjectId(_file['f'])})

                    try:
                        grid_fs = GridFS(app.data.driver.db)
                        if not grid_fs.exists(_id=file['file']):
                            pass
                        else:
                            stream = grid_fs.get(file['file'])  # get_last_version(_id=file['file'])
                            file_list.append('{}-{}'.format(key, file['name']))
                            with open('{}/{}-{}'.format(FILE_WORKING_DIR, key, file['name']), 'wb') as f:
                                f.write(stream.read())

                    except Exception as e:
                        print('Oh ah file err', e)

            try:
                json_file_name = '{}.json'.format(file_name)

                print('PATHS', FILE_WORKING_DIR, json_file_name)

                with open('{}/{}'.format(FILE_WORKING_DIR, json_file_name), 'w') as f:
                    json.dump(data.get('e5x', {}), f)

                _, stdout, stderr = execute(
                    ['node', 'e5x-gen.js', str(ors.get('id')), str(ors.get('_version')), 'motorfly'],
                    app.config['E5X_WORKING_DIR'])

                print('Stdout', stdout.rstrip())
                print('Stderr', stderr.rstrip())

                # Zip it! Add files to it!
                if stderr.rstrip() == '':
                    time.sleep(0.5)
                    cmds = ['zip', '{}.e5x'.format(file_name), '{}.xml'.format(file_name)]
                    cmds += file_list
                    print('CMDS', file_list, cmds)
                    _, stdout, stderr = execute(
                        cmds,
                        FILE_WORKING_DIR)
                    print('Stdout', stdout.rstrip())
                    print('Stderr', stderr.rstrip())

                    try:
                        status = data.get('e5x').get('entities', {}).get('reportingHistory', [])[0].get('attributes', {}).get('reportStatus', {}).get('value', 5)
                    except Exception as e:
                        status = 0
                        print('Error gettings status', status, e)


                    # Some audit and bookkeeping
                    audit = ors.get('e5x', {}).get('audit', [])
                    audit.append({
                        'date': datetime.datetime.now(),
                        'person_id': app.globals.get('user_id'),
                        'sent': False,
                        'status': status,
                        'version': ors.get('_version'),
                        'file': '{}.e5x'.format(file_name),
                        'e5y': {
                            'key': 'abrakadabra',
                            'number': 'c5de0c62-fbc9-4202-bbe8-ff52c1e79ae0',
                            'path': '/OCCS/A24A5466CDD843FFAAAA2DA663762C5E.E4O',
                            'created': '2019-06-19T22:57:46.6719259+02:00',
                            'modified': '2019-06-19T22:57:46.6719259+02:00',
                            'taxonomy': '4.1.0.6'
                        }
                    })

                    e5x = {'audit': audit,
                           'status': 'sent',
                           'latest_version': ors.get('_version')}

                    _update = col.update_one({'_id': ors.get('_id'), '_etag': ors.get('_etag')}, {'$set': {'e5x': e5x}})

                    print('UPDATED DB SAID: ', _update.raw_result, dir(_update))

                    #### TEST EMAIL!
                    recepients = list(set([app.globals.get('user_id')]
                                          + ors.get('organization', {}).get('ors', [])
                                          + ors.get('organization', {}).get('dto', [])
                                          ))
                    print('RECEPIENTS', recepients)

                    message = 'Hei\n\nDette er en leveringsbekreftelse for ORS #{0} version {1}\n\n \
                              Levert:\t{2}\
                              Status:\t{3}\
                              Fil:\t{4}\
                              Sent:\t{5}'.format(ors.get('id', ''),
                                                 ors.get('_version', ''),
                                                 datetime.datetime.now(),
                                                 status,
                                                 '{}.e5x'.format(file_name),
                                                 'email')

                    subject = 'E5X Leveringsbekreftelse ORS {0} v{1}'.format(ors.get('id', ''), ors.get('_version', ''))
                    print(subject)
                    print(message)
                    notify(recepients, subject, message)

                    return eve_response({'e5x': {'audit': audit}}, 200)

            except Exception as e:
                print('Oh my fucking god', e)

            return eve_response({'ERR': 'Could not process'}, 422)


@E5X.route("/download/<string:activity>/<int:ors_id>/<int:version>", methods=['GET'])
def download(activity, ors_id, version):
    if has_permission() is True:
        print(app.globals.get('user_id', 'AWDFULLLL'))
        col = app.data.driver.db['motorfly_observations']
        # db.companies.find().skip(NUMBER_OF_ITEMS * (PAGE_NUMBER - 1)).limit(NUMBER_OF_ITEMS )
        cursor = col.find({'$and': [{'id': ors_id},
                                    {'$or': [{'acl.execute.users': {'$in': [app.globals['user_id']]}},
                                             {'acl.execute.roles': {'$in': app.globals['acl']['roles']}}]}]})

        # _items = list(cursor.sort(sort['field'], sort['direction']).skip(max_results * (page - 1)).limit(max_results))
        _items = list(cursor)

        # Have access!
        if (len(_items) == 1):

            try:
                FILE_WORKING_DIR = '{}/{}/{}/{}'.format(app.config['E5X_WORKING_DIR'],
                                                        activity,
                                                        ors_id,
                                                        version)

                file_name = 'nlf_{}_{}_v{}.e5x'.format(activity,
                                                       ors_id,
                                                       version)
                print('{}/{}'.format(FILE_WORKING_DIR, file_name))
                # print('####',
                app.config['static_url_path'] = FILE_WORKING_DIR
                # with open('{}/{}'.format(FILE_WORKING_DIR, file_name), 'wb') as f:
                #    
                return send_file('{}/{}'.format(FILE_WORKING_DIR, file_name), as_attachment=True,
                                 attachment_filename=file_name, mimetype="'application/octet-stream'")
            except Exception as e:
                print('Download failed', e)
                return eve_response({'ERR': 'Could not send file'}, 422)
