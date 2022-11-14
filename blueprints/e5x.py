from flask import g, Blueprint, current_app as app, request, Response, abort, jsonify, send_file
from bson import json_util
import simplejson as json
import subprocess
from pprint import pprint
import os
import datetime
import time

from pymongo import MongoClient
from gridfs.errors import NoFile
from gridfs import GridFS
from bson.objectid import ObjectId

from ext.app.decorators import *
from ext.app.eve_helper import eve_abort, eve_response

import base64
from ext.auth.tokenauth import TokenAuth
from ext.auth.acl import parse_acl_flat
from ext.notifications.notifications import notify
from ext.app.notifications import ors_e5x
import pysftp
import traceback

from ext.scf import E5X_SEND_TO_LT

E5X_RIT_DEFAULT_VERSION = '4.1.0.3'

E5X = Blueprint('E5X Blueprint', __name__, )


def has_permission():
    try:

        b64token = request.args.get('token', default=None, type=str)
        token = base64.b64decode(b64token)[:-1]
        auth = TokenAuth()

        if not auth.check_auth(token=token.decode("utf-8"),
                               method=request.method,
                               resource=request.path[len(app.globals.get('prefix')):],
                               allowed_roles=None):
            return eve_abort(404, 'Please provide proper credentials')

    except:
        return eve_abort(404, 'Please provide proper credentials')

    # If so far, then goodie!
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
                echo_line = line.decode("utf-8")
            except:
                echo_line = str(line)

            stdout += echo_line

        for line in iter(process.stderr.readline, b''):

            try:
                echo_line = line.decode("utf-8")
            except:
                echo_line = str(line)

            stderr += echo_line

    except (KeyboardInterrupt, SystemExit) as err:
        return [False, '', str(err)]

    process.stdout.close()

    return_code = process.wait()
    if return_code != 0 or stderr != '':
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
    except Exception as e:
        app.logger.exception('[E5X] Generate structure failed')

    return False


def transport_e5x(dir, file_name, sftp_settings):
    if not sftp_settings:
        return False, {}

    # Transport to out
    result = False
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(sftp_settings['host'], username=sftp_settings['username'],
                               password=sftp_settings['password'], cnopts=cnopts) as sftp:

            try:
                result = sftp.put('{}/{}.e5x'.format(dir, file_name))
            except Exception as e:
                app.logger.exception('Could not send file via SFTP')
                return False, {}

    except Exception as e:
        app.logger.exception('Unknown error in SFTP')
        return False, {}

    if result:
        return True, {
            'mtime': result.st_mtime,
            'size': result.st_size,
            'uid': result.st_uid,
            'gid': result.st_gid
        }

    return False, {}


def remove_empty_nodes(obj):
    """Remove empty nodes with only id, refs pointing to nonexisting id's and empty lists and dicts"""

    def recursive_iter(obj, keys=()):
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from recursive_iter(v, keys + (k,))
        elif any(isinstance(obj, t) for t in (list, tuple)):
            for idx, item in enumerate(obj):
                yield from recursive_iter(item, keys + (idx,))
        else:
            yield keys, obj

    def clean_empty(d):
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (clean_empty(v) for v in d) if v]

        # 'NaN' is empty
        return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v and v != 'NaN'}

    def scrub(obj, bad_key="id", bad_values=[]):
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if key == bad_key and (len(obj.keys()) == 1 or obj[key] in bad_values):
                    del obj[key]
                else:
                    scrub(obj[key], bad_key)
        elif isinstance(obj, list):
            for i in reversed(range(len(obj))):
                if obj[i] == bad_key and len(obj) == 1:
                    del obj[i]
                else:
                    scrub(obj[i], bad_key)

        else:
            # neither a dict nor a list, do nothing
            pass

        return obj

    # Remove all single id's
    obj = scrub(obj, bad_key='id')
    # Remove all no values only unit
    obj = scrub(obj, bad_key='unit')
    # Remove all with only additionalTextEncoding
    obj = scrub(obj, bad_key='additionalTextEncoding')

    # Find all refs and remaining ids
    refs = []
    ids = []
    for keys, item in recursive_iter(obj):
        if keys[len(keys) - 1] == 'ref':
            refs.append(item)
        elif keys[len(keys) - 1] == 'id':
            ids.append(item)

    # Remove all refs pointing to nonexisting id's
    obj = scrub(obj, bad_key='ref', bad_values=[x for x in refs if x not in ids])

    return clean_empty(obj)


def cast_item_recursive(obj, keys, e5x_multiple_keys):
    # Check if any object keys matches id/choices.
    try:
        if isinstance(obj, dict):
            if any(x in keys for x in list(obj.keys())):
                for key in keys:

                    if (
                            key in list(obj.keys()) and
                            key in e5x_multiple_keys and
                            isinstance(obj[key], dict) and
                            'value' in obj[key]
                    ):
                        if isinstance(obj[key]['value'], list):
                            obj[key]['value'] = ['{}'.format(int(float(x))) for x in obj[key]['value']]
                        else:
                            obj[key] = [obj[key]['value']]

                    if key in list(obj.keys()):
                        if 'value' in list(obj[key].keys()):
                            if isinstance(obj[key]['value'], list):
                                obj[key]['value'] = ['{}'.format(int(float(x))) for x in obj[key]['value']]
                            elif isinstance(obj[key]['value'], dict) is False:
                                obj[key]['value'] = '{}'.format(int(float(obj[key]['value'])))
                        elif isinstance(obj[key], list):
                            if (
                                    len(obj[key]) > 0 and
                                    isinstance(obj[key][0], list) is False and
                                    isinstance(obj[key][0], dict) is False
                            ):
                                obj[key] = ['{}'.format(int(float(x))) for x in obj[key]]
                return obj
    except Exception as e:
        app.logger.exception('[E5X] Error casting value(s)')
        pass

    # If not key in keys and dict or list
    # Dict
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                obj[k] = cast_item_recursive(v, keys, e5x_multiple_keys)
            elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                obj[k] = cast_item_recursive(v, keys, e5x_multiple_keys)
            elif k in keys and isinstance(v, list) and len(v) > 0 and isinstance(v[0], str):
                obj[k] = ['{}'.format(int(float(x))) for x in obj[k]]
                return obj

    # List of dicts
    if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], dict):

        for k, v in enumerate(obj):
            if isinstance(v, dict):
                obj[k] = cast_item_recursive(v, keys, e5x_multiple_keys)
            elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                obj[k] = cast_item_recursive(v, keys, e5x_multiple_keys)

    return obj


def convert_to_integer_ids(e5x_data):
    try:
        col = app.data.driver.db['e5x_attributes']
        data = list(col.find({"choices_key": {"$ne": None}, "rit_version": E5X_RIT_DEFAULT_VERSION}))
        l = []
        l2 = []
        for k in data:
            l.append(k['attribute'].split('.')[-1])
            if k['max'] not in [0, 1]:
                l2.append(k['attribute'].split('.')[-1])

        e5x_keys = [x[0].lower() + x[1:] for x in l]
        e5x_multiple_keys = [x[0].lower() + x[1:] for x in l2]

        return cast_item_recursive(e5x_data, e5x_keys, e5x_multiple_keys)
    except Exception as e:
        app.logger.exception("[ERROR] Could not convert e5x data", e5x_data)

    return e5x_data


@E5X.route("/generate/<string:activity>/<objectid:_id>", methods=['POST'])
@require_token()
def generate(activity, _id):
    data = request.get_json(force=True)
    resource_collection = '{}_observations'.format(activity)
    col = app.data.driver.db[resource_collection]
    cursor = col.find({'$and': [{'_etag': data.get('_etag', None), '_id': _id},
                                {'$or': [{'acl.execute.users': {'$in': [g.user_id]}},
                                         {'acl.execute.roles': {'$in': g.acl.get('roles', [])}}]}]})
    total_items = cursor.count()

    # _items = list(cursor.sort(sort['field'], sort['direction']).skip(max_results * (page - 1)).limit(max_results))
    _items = list(cursor)

    if (len(_items) == 1):

        # print(_items)
        ors = _items[0]

        FILE_WORKING_DIR = '{}/{}/{}/{}'.format(app.config['E5X_WORKING_DIR'], activity, ors.get('id'),
                                                ors.get('_version'))

        file_name = 'nlf_{}_{}_v{}'.format(ors.get('_model', {}).get('type', None), ors.get('id'),
                                           ors.get('_version'))

        if generate_structure(activity, ors.get('id'), ors.get('_version')) is True:

            app.logger.debug('[E5X] Structure ok')

            # Process files!
            file_list = []

            if len(ors.get('files', [])) > 0:
                app.logger.debug('[E5X] Adding files')
                col_files = app.data.driver.db['files']

                # Fix data structures
                # if 'report' not in \
                #        data.get('value', {}).get('occurrence', {}).get('entities', {}).get('reportingHistory', [])[
                #            0].get('attributes', {}).get('report'):
                data['e5x']['entities']['reportingHistory'][0]['attributes']['report'] = []  # = {
                # 'attachments': []}
                # 'attributes': {'resourceLocator': []}}

                ## Folder for files
                files_working_path = '{}/{}'.format(FILE_WORKING_DIR, file_name)
                if os.path.exists(files_working_path) is False:
                    _, stdout, stderr = execute(['mkdir', file_name], FILE_WORKING_DIR)
                    app.logger.debug('[E5X] Created folder for files')

                for key, _file in enumerate(ors.get('files', [])):
                    try:
                        file = col_files.find_one({'_id': ObjectId(_file['f'])})

                        """
                        @TODO need to verify size for LT
                        """
                        try:
                            grid_fs = GridFS(app.data.driver.db)
                            if not grid_fs.exists(_id=file['file']):
                                pass
                            else:

                                stream = grid_fs.get(file['file'])  # get_last_version(_id=file['file'])

                                file_list.append('{}/{}-{}'.format(file_name, key, file['name']))

                                with open('{}/{}-{}'.format(files_working_path, key, file['name']), 'wb') as f:
                                    f.write(stream.read())

                                try:
                                    # data['e5x']['entities']['reportingHistory'][0]['attributes']['report']['attributes']['resourceLocator'].append(
                                    #    {'fileName': '{}-{}'.format(key, file['name']), 'description': ''}
                                    # )
                                    data['e5x']['entities']['reportingHistory'][0]['attributes']['report'].append(
                                        {'fileName': '{}-{}'.format(key, file['name']), 'description': ''}
                                    )
                                except Exception as e:
                                    app.logger.exception("[ERROR] Could not add file name to report")
                                    app.logger.error(e)

                        except Exception as e:
                            app.logger.exception("[ERR] Getting files")
                    except KeyError as e:
                        app.logger.exception("[ERROR] Could not add file, KeyError: {}".format(_file))
                        app.logger.error(e)
                    except Exception as e:
                        app.logger.exception("[ERROR] Could not add file, unknown error: {}".format(_file))
                        app.logger.error(e)

            try:
                app.logger.debug('[III] In try')
                json_file_name = '{}.json'.format(file_name)

                # Fix e5x data
                # Remove all empty nodes, run twice if sequence wrong
                data['e5x'] = remove_empty_nodes(remove_empty_nodes(data.get('e5x', {})))
                # Convert all integer id's to integers
                data['e5x'] = convert_to_integer_ids(data.get('e5x', {}))

                # 1 Dump to json file
                with open('{}/{}'.format(FILE_WORKING_DIR, json_file_name), 'w') as f:
                    json.dump(data['e5x'], f)

                # 2 Generate xml file
                # e5x-generate.js will make folder relative to e5x-generate.js
                _, stdout, stderr = execute(
                    [
                        'node',
                        'e5x-generate.js',
                        str(ors.get('id')),
                        str(ors.get('_version')),
                        activity,
                        str(data.get('rit_version', E5X_RIT_DEFAULT_VERSION))

                    ],
                    app.config['E5X_WORKING_DIR'])

                app.logger.debug('[STDOUT] {}'.format(stdout))
                app.logger.debug('[STDERR] {}'.format(stderr))

                # 3 Zip it! Add files to it!
                if stderr.rstrip() == '':
                    time.sleep(0.5)
                    cmds = ['zip', '{}.e5x'.format(file_name), '{}.xml'.format(file_name)]
                    cmds += file_list
                    # dir:
                    # cmds += file_name
                    # print('CMDS', file_list, cmds)
                    _, stdout, stderr = execute(
                        cmds,
                        FILE_WORKING_DIR
                    )

                    try:
                        status = data.get('e5x').get('entities', {}) \
                            .get('reportingHistory', [])[0] \
                            .get('attributes', {}) \
                            .get('reportStatus', {}).get('value', 5)

                    except Exception as e:
                        app.logger.exception('Error gettings status {}'.format(status))
                        status = 0

                    # SFTP DELIVERY!
                    # Only dev and prod should be able to deliver to LT
                    if app.config.get('APP_INSTANCE', '') == 'dev-removeme-test':
                        from ext.scf import LT_SFTP_TEST_CFG as SFTP
                    elif app.config.get('APP_INSTANCE', '') == 'prod':
                        from ext.scf import LT_SFTP_CFG as SFTP
                    else:
                        app.logger.warning('No SFTP settings for this instance')
                        SFTP = False

                    # Manual flag set via local E5X_SEND_TO_LT
                    if E5X_SEND_TO_LT is False:
                        SFTP = False

                    transport_status, transport = transport_e5x(FILE_WORKING_DIR, file_name, SFTP)

                    # Some audit and bookkeeping
                    audit = ors.get('e5x', {}).get('audit', [])

                    audit.append({
                        'date': datetime.datetime.now(),
                        'person_id': g.user_id,
                        'sent': transport_status,
                        'status': status,
                        'version': ors.get('_version'),
                        'file': '{}.e5x'.format(file_name),
                        'rit_version': data.get('rit_version', E5X_RIT_DEFAULT_VERSION),
                        'e5y': transport
                    })

                    """
                    'e5y': {
                        'key': 'abrakadabra',
                        'number': 'c5de0c62-fbc9-4202-bbe8-ff52c1e79ae0',
                        'path': '/OCCS/A24A5466CDD843FFAAAA2DA663762C5E.E4O',
                        'created': '2019-06-19T22:57:46.6719259+02:00',
                        'modified': '2019-06-19T22:57:46.6719259+02:00',
                        'taxonomy': '4.1.0.6'
                    }
                    """

                    e5x = {'audit': audit,
                           'status': 'sent',
                           'latest_version': ors.get('_version')}

                    _update = col.update_one({'_id': ors.get('_id'), '_etag': ors.get('_etag')}, {'$set': {'e5x': e5x}})

                    if not _update:
                        app.logger.error('Error storing e5x delivery message in database')

                    # print('UPDATED DB SAID: ', _update.raw_result, dir(_update))
                    try:
                        recepients = parse_acl_flat(ors.get('acl', {}))

                        ors_e5x(recepients=recepients,
                                event_from=resource_collection,
                                event_from_id=ors.get('_id', ''),
                                source=ors.get('_version', ''),
                                status=status,
                                ors_id=ors.get('id', None),
                                ors_tags=ors.get('tags', []),
                                file_name='{}.e5x'.format(file_name),
                                transport='sftp',
                                context='sent'
                                )
                        """
                        
                        #### TEST EMAIL!
                        recepients = list(set([g.user_id]
                                              + ors.get('organization', {}).get('ors', [])
                                              + ors.get('organization', {}).get('dto', [])
                                              ))
                        # print('RECEPIENTS', recepients)

                        message = 'Hei\n\nDette er en leveringsbekreftelse for OBSREG #{0} versjon {1}\n\n \
                                  Levert:\t{2}\n\
                                  Status:\t{3}\n\
                                  Fil:\t{4}\n\
                                  Levert via:\t{5}\n\
                                  Instans:\t{6}\n'.format(ors.get('id', ''),
                                                          ors.get('_version', ''),
                                                          datetime.datetime.now(),
                                                          status,
                                                          '{}.e5x'.format(file_name),
                                                          'sftp',
                                                          app.config.get('APP_INSTANCE', ''))

                        subject = 'E5X Leveringsbekreftelse OBSREG {0} v{1}'.format(ors.get('id', ''),
                                                                                 ors.get('_version', ''))

                        notify(recepients, subject, message)
                        """
                    except Exception as e:
                        app.logger.exception('Error delivering e5x delivery notification')

                    return eve_response({'e5x': {'audit': audit}, 'err': traceback.format_exc()}, 200)

                else:
                    app.logger.error('STDERR: {}'.format(stderr))

            except Exception as e:
                app.logger.exception('Error processing e5x file')
                return eve_response({'ERR': 'Could not process', 'err': traceback.format_exc()}, 422)

    return eve_response({'ERR': 'Could not process e5x', 'err': traceback.format_exc()}, 422)


@E5X.route("/download/<string:activity>/<int:ors_id>/<int:version>", methods=['GET'])
def download(activity, ors_id, version):
    if has_permission() is True:
        col = app.data.driver.db['{}_observations'.format(activity)]
        # db.companies.find().skip(NUMBER_OF_ITEMS * (PAGE_NUMBER - 1)).limit(NUMBER_OF_ITEMS )
        cursor = col.find({'$and': [{'id': ors_id},
                                    {'$or': [
                                        {'reporter': g.user_id},
                                        {'acl.execute.users': {'$in': [g.user_id]}},
                                        {'acl.execute.roles': {'$in': g.acl.get('roles', [])}}
                                    ]
                                    }
                                    ]
                           }
                          )

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
                app.logger.debug('[E5X DOWNLOAD] {}/{}'.format(FILE_WORKING_DIR, file_name))
                # print('####',
                app.config['static_url_path'] = FILE_WORKING_DIR
                # with open('{}/{}'.format(FILE_WORKING_DIR, file_name), 'wb') as f:
                #    
                return send_file('{}/{}'.format(FILE_WORKING_DIR, file_name),
                                 as_attachment=True,
                                 attachment_filename=file_name,
                                 mimetype="'application/octet-stream'")
            except Exception as e:
                # print('Download failed', e)
                app.logger.debug('[E5X DOWNLOAD ERR] {}'.format(e))

        app.logger.debug(
            '[E5X DOWNLOAD ERR] Returned {} items for {} id {} version {}'.format(len(_items), activity, ors_id,
                                                                                  version))

        return eve_response({'ERR': 'Could not send file'}, 422)
