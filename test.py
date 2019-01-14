d = {'ENV': 'production', 'DEBUG': True, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None,
     'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SECRET_KEY': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31),
     'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session',
     'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True,
     'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True,
     'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200),
     'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False,
     'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': False,
     'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSONIFY_MIMETYPE': 'application/json', 'TEMPLATES_AUTO_RELOAD': None,
     'MAX_COOKIE_SIZE': 4093, 'ALLOWED_FILTERS': ['*'], 'ALLOWED_ITEM_READ_ROLES': [], 'ALLOWED_ITEM_ROLES': [],
     'ALLOWED_ITEM_WRITE_ROLES': [], 'ALLOWED_READ_ROLES': [], 'ALLOWED_ROLES': [], 'ALLOWED_WRITE_ROLES': [],
     'ALLOW_CUSTOM_FIELDS_IN_GEOJSON': False, 'ALLOW_OVERRIDE_HTTP_METHOD': True, 'ALLOW_UNKNOWN': False,
     'API_VERSION': 'v1', 'AUTH_FIELD': None, 'AUTO_COLLAPSE_MULTI_KEYS': False, 'AUTO_CREATE_LISTS': False,
     'BANDWIDTH_SAVER': True, 'BULK_ENABLED': True, 'CACHE_CONTROL': 'max-age=20', 'CACHE_EXPIRES': 20,
     'DATE_CREATED': '_created', 'DATE_FORMAT': '%Y-%m-%dT%H:%M:%S.%fZ', 'DELETED': '_deleted', 'EMBEDDING': True,
     'ENFORCE_IF_MATCH': True, 'ERROR': '_error', 'ETAG': '_etag',
     'EXTENDED_MEDIA_INFO': ['content_type', 'name', 'length'], 'EXTRA_RESPONSE_FIELDS': [], 'HATEOAS': True,
     'HEADER_TOTAL_COUNT': 'X-Total-Count', 'ID_FIELD': '_id', 'IF_MATCH': True, 'INFO': None,
     'INTERNAL_RESOURCE': False, 'ISSUES': '_issues', 'ITEMS': '_items', 'ITEM_CACHE_CONTROL': '', 'ITEM_LOOKUP': True,
     'ITEM_LOOKUP_FIELD': '_id', 'ITEM_METHODS': ['GET', 'PATCH', 'DELETE', 'PUT'], 'ITEM_URL': 'regex("[a-f0-9]{24}")',
     'JSONP_ARGUMENT': None, 'JSON_REQUEST_CONTENT_TYPES': ['application/json'], 'LAST_UPDATED': '_updated',
     'LATEST_VERSION': '_latest_version', 'LINKS': '_links', 'MEDIA_BASE_URL': None, 'MEDIA_ENDPOINT': 'media',
     'MEDIA_URL': 'regex("[a-f0-9]{24}")', 'MERGE_NESTED_DOCUMENTS': True, 'META': '_meta',
     'MONGO_OPTIONS': {'connect': True, 'tz_aware': True}, 'MONGO_QUERY_BLACKLIST': ['$where', '$regex'],
     'MONGO_WRITE_CONCERN': {'w': 1}, 'MULTIPART_FORM_FIELDS_AS_JSON': False, 'NORMALIZE_DOTTED_FIELDS': True,
     'OPLOG': False, 'OPLOG_AUDIT': True, 'OPLOG_CHANGE_METHODS': ['DELETE', 'PATCH', 'PUT'], 'OPLOG_ENDPOINT': None,
     'OPLOG_METHODS': ['DELETE', 'POST', 'PATCH', 'PUT'], 'OPLOG_NAME': 'oplog', 'OPLOG_RETURN_EXTRA_FIELD': False,
     'OPTIMIZE_PAGINATION_FOR_SPEED': False, 'PAGINATION': True, 'PAGINATION_DEFAULT': 25, 'PAGINATION_LIMIT': 1000000,
     'PROJECTION': True, 'PUBLIC_ITEM_METHODS': [], 'PUBLIC_METHODS': [], 'QUERY_AGGREGATION': 'aggregate',
     'QUERY_EMBEDDED': 'embedded', 'QUERY_MAX_RESULTS': 'max_results', 'QUERY_PAGE': 'page',
     'QUERY_PROJECTION': 'projection', 'QUERY_SORT': 'sort', 'QUERY_WHERE': 'where', 'RATE_LIMIT_DELETE': None,
     'RATE_LIMIT_GET': None, 'RATE_LIMIT_PATCH': None, 'RATE_LIMIT_POST': None,
     'RENDERERS': ['eve.render.JSONRenderer'], 'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
     'RETURN_MEDIA_AS_BASE64_STRING': True, 'RETURN_MEDIA_AS_URL': False, 'SCHEMA_ENDPOINT': None,
     'SHOW_DELETED_PARAM': 'show_deleted', 'SOFT_DELETE': False, 'SORTING': True,
     'STANDARD_ERRORS': [400, 401, 404, 405, 406, 409, 410, 412, 422, 428], 'STATUS': '_status', 'STATUS_ERR': 'ERR',
     'STATUS_OK': 'OK', 'UPSERT_ON_PUT': True, 'URL_PREFIX': 'api', 'VALIDATE_FILTERS': False,
     'VALIDATION_ERROR_AS_LIST': False, 'VALIDATION_ERROR_STATUS': 422, 'VERSION': '_version', 'VERSIONING': False,
     'VERSIONS': '_versions', 'VERSION_DIFF_INCLUDE': [], 'VERSION_ID_SUFFIX': '_document', 'VERSION_PARAM': 'version',
     'X_ALLOW_CREDENTIALS': None, 'X_DOMAINS': ['http://localhost:4200', 'https://doc.nlf.no'], 'X_DOMAINS_RE': None,
     'X_EXPOSE_HEADERS': None, 'X_HEADERS': ['Content-Type', 'If-Match'], 'X_MAX_AGE': 21600,
     'APP_ALL': ['nlf-backend'], 'APP_AUTHOR': 'Einar Huseby', 'APP_COPYRIGHT': '(c) 2014-2019 NLF',
     'APP_HOST': '127.0.0.1', 'APP_INSTANCE': 'dev', 'APP_INSTANCES': ['dev', 'beta', 'app'], 'APP_LICENSE': 'GPLV1',
     'APP_PORT': 8082, 'APP_VERSION': '0.1.0', 'AUTH_SESSION_LENGHT': 3600, 'DOMAIN': {
        'users': {'item_title': 'users', 'url': 'users',
                  'datasource': {'source': 'users', 'default_sort': [('id', 1)], 'filter': None,
                                 'projection': {'id': 1, 'avatar': 1, 'settings': 1, 'custom': 1, 'info': 1,
                                                'statistics': 1, 'acl': 1, '_id': 1, '_updated': 1, '_created': 1,
                                                '_etag': 1, '_version': 1, '_id_document': 1}, 'aggregation': None},
                  'extra_response_fields': ['id'], 'resource_methods': ['POST', 'GET'],
                  'item_methods': ['GET', 'PATCH'], 'auth_field': 'id', 'versioning': True,
                  'additional_lookup': {'url': 'regex("[\\d{1,6}]+")', 'field': 'id'},
                  'mongo_indexes': {'person id': ([('id', 1)], {'background': True}),
                                    'acl': ([('acl', 1)], {'background': True})},
                  'schema': {'id': {'type': 'integer', 'required': True, 'readonly': True}, 'avatar': {'type': 'media'},
                             'settings': {'type': 'dict', 'default': {}}, 'custom': {'type': 'dict'},
                             'info': {'type': 'dict'}, 'statistics': {'type': 'dict', 'readonly': True},
                             'acl': {'type': 'dict', 'readonly': True, 'schema': {
                                 'groups': {'type': 'list', 'default': [], 'schema': {'type': 'objectid'}},
                                 'roles': {'type': 'list', 'default': [], 'schema': {'type': 'objectid'}}},
                                     'default': {'groups': [], 'roles': []}}, '_id': {'type': 'objectid'}},
                  'public_methods': [], 'allowed_roles': [], 'allowed_read_roles': [], 'allowed_write_roles': [],
                  'cache_control': 'max-age=20', 'cache_expires': 20, 'id_field': '_id', 'item_lookup_field': '_id',
                  'item_url': 'regex("[a-f0-9]{24}")', 'resource_title': 'users', 'item_lookup': True,
                  'public_item_methods': [], 'allowed_item_roles': [], 'allowed_item_read_roles': [],
                  'allowed_item_write_roles': [], 'allowed_filters': ['*'], 'sorting': True, 'embedding': True,
                  'embedded_fields': [], 'pagination': True, 'projection': True, 'soft_delete': False,
                  'bulk_enabled': True, 'internal_resource': False, 'etag_ignore_fields': None, 'allow_unknown': False,
                  'mongo_write_concern': {'w': 1}, 'hateoas': True, 'authentication': 't',
                  'merge_nested_documents': True, 'normalize_dotted_fields': True,
                  '_media': ['avatar']}, 'users_acl': {'item_title': 'users/acl', 'url': 'users/acl',
                                                       'datasource': {'source': 'users', 'default_sort': [('id', 1)],
                                                                      'filter': None,
                                                                      'projection': {'id': 1, 'acl': 1, '_id': 1,
                                                                                     '_updated': 1,
                                                                                     '_created': 1, '_etag': 1},
                                                                      'aggregation': None},
                                                       'extra_response_fields': ['id'],
                                                       'resource_methods': ['GET'], 'item_methods': ['GET'],
                                                       'allowed_write_roles': ['superadmin'],
                                                       'allowed_item_write_roles': ['superadmin'],
                                                       'additional_lookup': {'url': 'regex("[\\d{1,6}]+")',
                                                                             'field': 'id'},
                                                       'schema': {'id': {'type': 'integer', 'readonly': True},
                                                                  'acl': {'type': 'dict', 'readonly': False, 'schema': {
                                                                      'groups': {'type': 'list', 'default': [],
                                                                                 'schema': {'type': 'objectid'}},
                                                                      'roles': {'type': 'list', 'default': [],
                                                                                'schema': {'type': 'objectid'}}}},
                                                                  '_id': {'type': 'objectid'}}, 'public_methods': [],
                                                       'allowed_roles': [], 'allowed_read_roles': [],
                                                       'cache_control': 'max-age=20',
                                                       'cache_expires': 20, 'id_field': '_id',
                                                       'item_lookup_field': '_id',
                                                       'item_url': 'regex("[a-f0-9]{24}")',
                                                       'resource_title': 'users/acl',
                                                       'item_lookup': True, 'public_item_methods': [],
                                                       'allowed_item_roles': [],
                                                       'allowed_item_read_roles': [], 'allowed_filters': ['*'],
                                                       'sorting': True,
                                                       'embedding': True, 'embedded_fields': [], 'pagination': True,
                                                       'projection': True, 'versioning': False, 'soft_delete': False,
                                                       'bulk_enabled': True, 'internal_resource': False,
                                                       'etag_ignore_fields': None,
                                                       'auth_field': None, 'allow_unknown': False,
                                                       'mongo_write_concern': {'w': 1},
                                                       'mongo_indexes': {}, 'hateoas': True, 'authentication'
                                                       : < ext.auth.tokenauth.TokenAuth
        object
            at
        0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True,
     '_media': []}, 'users_auth': {
                                      'item_title': 'user auth',
                                      'internal_resource': True,
                                      'datasource': {
                                          'source': 'users_auth',
                                          'default_sort': [
                                              (
                                                  'id',
                                                  1)],
                                          'filter': None,
                                          'projection': {
                                              'id': 1,
                                              'acl': 1,
                                              'auth': 1,
                                              'user': 1,
                                              '_id': 1,
                                              '_updated': 1,
                                              '_created': 1,
                                              '_etag': 1},
                                          'aggregation': None},
                                      'resource_methods': [],
                                      'item_methods': [],
                                      'versioning': False,
                                      'additional_lookup': {
                                          'url': 'regex("[\\d{1,6}]+")',
                                          'field': 'id'},
                                      'mongo_indexes': {
                                          'person id': (
                                              [
                                                  (
                                                      'id',
                                                      1)],
                                              {
                                                  'background': True}),
                                          'acl': (
                                              [
                                                  (
                                                      'acl',
                                                      1)],
                                              {
                                                  'background': True}),
                                          'auth': (
                                              [
                                                  (
                                                      'auth',
                                                      1)],
                                              {
                                                  'background': True}),
                                          'user': (
                                              [
                                                  (
                                                      'user',
                                                      1)],
                                              {
                                                  'background': True})},
                                      'schema': {
                                          'id': {
                                              'type': 'integer',
                                              'required': True},
                                          'acl': {
                                              'type': 'dict'},
                                          'auth': {
                                              'type': 'dict',
                                              'schema': {
                                                  'token': {
                                                      'type': 'string'},
                                                  'valid': {
                                                      'type': 'datetime'}}},
                                          'user': {
                                              'type': 'objectid',
                                              'data_relation': {
                                                  'resource': 'users',
                                                  'field': '_id',
                                                  'embeddable': True}},
                                          '_id': {
                                              'type': 'objectid'}},
                                      'url': 'users_auth',
                                      'public_methods': [],
                                      'allowed_roles': [],
                                      'allowed_read_roles': [],
                                      'allowed_write_roles': [],
                                      'cache_control': 'max-age=20',
                                      'cache_expires': 20,
                                      'id_field': '_id',
                                      'item_lookup_field': '_id',
                                      'item_url': 'regex("[a-f0-9]{24}")',
                                      'resource_title': 'users_auth',
                                      'item_lookup': True,
                                      'public_item_methods': [],
                                      'allowed_item_roles': [],
                                      'allowed_item_read_roles': [],
                                      'allowed_item_write_roles': [],
                                      'allowed_filters': [
                                          '*'],
                                      'sorting': True,
                                      'embedding': True,
                                      'embedded_fields': [],
                                      'pagination': True,
                                      'projection': True,
                                      'soft_delete': False,
                                      'bulk_enabled': True,
                                      'etag_ignore_fields': None,
                                      'auth_field': None,
                                      'allow_unknown': False,
                                      'extra_response_fields': [],
                                      'mongo_write_concern': {
                                          'w': 1},
                                      'hateoas': True,
                                      'authentication'
                                      : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'acl_groups': {
                                                                                                                    'item_title': 'acl_groups',
                                                                                                                    'item_name': 'acl_groups',
                                                                                                                    'url': 'acl/groups',
                                                                                                                    'datasource': {
                                                                                                                        'source': 'acl_groups',
                                                                                                                        'filter': None,
                                                                                                                        'default_sort': None,
                                                                                                                        'projection': {
                                                                                                                            'name': 1,
                                                                                                                            'description': 1,
                                                                                                                            'ref': 1,
                                                                                                                            '_id': 1,
                                                                                                                            '_updated': 1,
                                                                                                                            '_created': 1,
                                                                                                                            '_etag': 1},
                                                                                                                        'aggregation': None},
                                                                                                                    'allowed_write_roles': [
                                                                                                                        'superadmin'],
                                                                                                                    'allowed_item_write_roles': [
                                                                                                                        'superadmin'],
                                                                                                                    'internal_resource': False,
                                                                                                                    'concurrency_check': True,
                                                                                                                    'resource_methods': [
                                                                                                                        'GET',
                                                                                                                        'POST'],
                                                                                                                    'item_methods': [
                                                                                                                        'GET',
                                                                                                                        'PATCH'],
                                                                                                                    'versioning': False,
                                                                                                                    'additional_lookup': {
                                                                                                                        'url': 'regex("[\\d{3}\\-\\w{1}]+")',
                                                                                                                        'field': 'ref'},
                                                                                                                    'mongo_indexes': {
                                                                                                                        'name': (
                                                                                                                            [
                                                                                                                                (
                                                                                                                                    'name',
                                                                                                                                    1)],
                                                                                                                            {
                                                                                                                                'background': True}),
                                                                                                                        'ref': (
                                                                                                                            [
                                                                                                                                (
                                                                                                                                    'ref',
                                                                                                                                    1)],
                                                                                                                            {
                                                                                                                                'background': True})},
                                                                                                                    'schema': {
                                                                                                                        'name': {
                                                                                                                            'type': 'string',
                                                                                                                            'required': 'true',
                                                                                                                            'unique': True},
                                                                                                                        'description': {
                                                                                                                            'type': 'string'},
                                                                                                                        'ref': {
                                                                                                                            'type': 'string',
                                                                                                                            'unique': True},
                                                                                                                        '_id': {
                                                                                                                            'type': 'objectid'}},
                                                                                                                    'public_methods': [],
                                                                                                                    'allowed_roles': [],
                                                                                                                    'allowed_read_roles': [],
                                                                                                                    'cache_control': 'max-age=20',
                                                                                                                    'cache_expires': 20,
                                                                                                                    'id_field': '_id',
                                                                                                                    'item_lookup_field': '_id',
                                                                                                                    'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                    'resource_title': 'acl/groups',
                                                                                                                    'item_lookup': True,
                                                                                                                    'public_item_methods': [],
                                                                                                                    'allowed_item_roles': [],
                                                                                                                    'allowed_item_read_roles': [],
                                                                                                                    'allowed_filters': [
                                                                                                                        '*'],
                                                                                                                    'sorting': True,
                                                                                                                    'embedding': True,
                                                                                                                    'embedded_fields': [],
                                                                                                                    'pagination': True,
                                                                                                                    'projection': True,
                                                                                                                    'soft_delete': False,
                                                                                                                    'bulk_enabled': True,
                                                                                                                    'etag_ignore_fields': None,
                                                                                                                    'auth_field': None,
                                                                                                                    'allow_unknown': False,
                                                                                                                    'extra_response_fields': [],
                                                                                                                    'mongo_write_concern': {
                                                                                                                        'w': 1},
                                                                                                                    'hateoas': True,
                                                                                                                    'authentication'
                                                                                                                    : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'acl_roles': {
                                                                                                                   'item_title': 'acl/roles',
                                                                                                                   'url': 'acl/roles',
                                                                                                                   'allowed_write_roles': [
                                                                                                                       'superadmin'],
                                                                                                                   'allowed_item_write_roles': [
                                                                                                                       'superadmin'],
                                                                                                                   'datasource': {
                                                                                                                       'source': 'acl_roles',
                                                                                                                       'filter': None,
                                                                                                                       'default_sort': None,
                                                                                                                       'projection': {
                                                                                                                           'name': 1,
                                                                                                                           'description': 1,
                                                                                                                           'ref': 1,
                                                                                                                           'group': 1,
                                                                                                                           '_id': 1,
                                                                                                                           '_updated': 1,
                                                                                                                           '_created': 1,
                                                                                                                           '_etag': 1},
                                                                                                                       'aggregation': None},
                                                                                                                   'internal_resource': False,
                                                                                                                   'concurrency_check': True,
                                                                                                                   'resource_methods': [
                                                                                                                       'GET',
                                                                                                                       'POST'],
                                                                                                                   'item_methods': [
                                                                                                                       'GET',
                                                                                                                       'PATCH'],
                                                                                                                   'versioning': False,
                                                                                                                   'mongo_indexes': {
                                                                                                                       'name': (
                                                                                                                           [
                                                                                                                               (
                                                                                                                                   'name',
                                                                                                                                   1)],
                                                                                                                           {
                                                                                                                               'background': True}),
                                                                                                                       'ref': (
                                                                                                                           [
                                                                                                                               (
                                                                                                                                   'ref',
                                                                                                                                   1)],
                                                                                                                           {
                                                                                                                               'background': True}),
                                                                                                                       'group': (
                                                                                                                           [
                                                                                                                               (
                                                                                                                                   'group',
                                                                                                                                   1)],
                                                                                                                           {
                                                                                                                               'background': True})},
                                                                                                                   'schema': {
                                                                                                                       'name': {
                                                                                                                           'type': 'string',
                                                                                                                           'required': 'true'},
                                                                                                                       'description': {
                                                                                                                           'type': 'string'},
                                                                                                                       'ref': {
                                                                                                                           'type': 'string',
                                                                                                                           'unique': True},
                                                                                                                       'group': {
                                                                                                                           'type': 'objectid',
                                                                                                                           'required': True,
                                                                                                                           'data_relation': {
                                                                                                                               'resource': 'acl/groups',
                                                                                                                               'field': '_id',
                                                                                                                               'embeddable': True}},
                                                                                                                       '_id': {
                                                                                                                           'type': 'objectid'}},
                                                                                                                   'public_methods': [],
                                                                                                                   'allowed_roles': [],
                                                                                                                   'allowed_read_roles': [],
                                                                                                                   'cache_control': 'max-age=20',
                                                                                                                   'cache_expires': 20,
                                                                                                                   'id_field': '_id',
                                                                                                                   'item_lookup_field': '_id',
                                                                                                                   'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                   'resource_title': 'acl/roles',
                                                                                                                   'item_lookup': True,
                                                                                                                   'public_item_methods': [],
                                                                                                                   'allowed_item_roles': [],
                                                                                                                   'allowed_item_read_roles': [],
                                                                                                                   'allowed_filters': [
                                                                                                                       '*'],
                                                                                                                   'sorting': True,
                                                                                                                   'embedding': True,
                                                                                                                   'embedded_fields': [],
                                                                                                                   'pagination': True,
                                                                                                                   'projection': True,
                                                                                                                   'soft_delete': False,
                                                                                                                   'bulk_enabled': True,
                                                                                                                   'etag_ignore_fields': None,
                                                                                                                   'auth_field': None,
                                                                                                                   'allow_unknown': False,
                                                                                                                   'extra_response_fields': [],
                                                                                                                   'mongo_write_concern': {
                                                                                                                       'w': 1},
                                                                                                                   'hateoas': True,
                                                                                                                   'authentication'
                                                                                                                   : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'f_ors': {
                                                                                                               'item_title': 'Fallskjerm Observations',
                                                                                                               'url': 'f/observations',
                                                                                                               'datasource': {
                                                                                                                   'source': 'f_observations',
                                                                                                                   'projection': {
                                                                                                                       'acl': 0,
                                                                                                                       'id': 1,
                                                                                                                       'type': 1,
                                                                                                                       'flags': 1,
                                                                                                                       'ask': 1,
                                                                                                                       'tags': 1,
                                                                                                                       'club': 1,
                                                                                                                       'location': 1,
                                                                                                                       'owner': 1,
                                                                                                                       'reporter': 1,
                                                                                                                       'when': 1,
                                                                                                                       'involved': 1,
                                                                                                                       'organization': 1,
                                                                                                                       'rating': 1,
                                                                                                                       'weather': 1,
                                                                                                                       'components': 1,
                                                                                                                       'files': 1,
                                                                                                                       'related': 1,
                                                                                                                       'actions': 1,
                                                                                                                       'comments': 1,
                                                                                                                       'workflow': 1,
                                                                                                                       'watchers': 1,
                                                                                                                       'audit': 1,
                                                                                                                       '_id': 1,
                                                                                                                       '_updated': 1,
                                                                                                                       '_created': 1,
                                                                                                                       '_etag': 1,
                                                                                                                       '_version': 1,
                                                                                                                       '_id_document': 1},
                                                                                                                   'filter': None,
                                                                                                                   'default_sort': None,
                                                                                                                   'aggregation': None},
                                                                                                               'additional_lookup': {
                                                                                                                   'url': 'regex("[\\d{1,9}]+")',
                                                                                                                   'field': 'id'},
                                                                                                               'extra_response_fields': [
                                                                                                                   'id'],
                                                                                                               'versioning': True,
                                                                                                               'resource_methods': [
                                                                                                                   'GET',
                                                                                                                   'POST'],
                                                                                                               'item_methods': [
                                                                                                                   'GET',
                                                                                                                   'PATCH',
                                                                                                                   'PUT'],
                                                                                                               'mongo_indexes': {
                                                                                                                   'id': (
                                                                                                                       [
                                                                                                                           (
                                                                                                                               'id',
                                                                                                                               1)],
                                                                                                                       {
                                                                                                                           'background': True}),
                                                                                                                   'persons': (
                                                                                                                       [
                                                                                                                           (
                                                                                                                               'owner',
                                                                                                                               1),
                                                                                                                           (
                                                                                                                               'reporter',
                                                                                                                               1)],
                                                                                                                       {
                                                                                                                           'background': True}),
                                                                                                                   'when': (
                                                                                                                       [
                                                                                                                           (
                                                                                                                               'when',
                                                                                                                               1)],
                                                                                                                       {
                                                                                                                           'background': True}),
                                                                                                                   'type': (
                                                                                                                       [
                                                                                                                           (
                                                                                                                               'type',
                                                                                                                               1)],
                                                                                                                       {
                                                                                                                           'background': True}),
                                                                                                                   'rating': (
                                                                                                                       [
                                                                                                                           (
                                                                                                                               'rating',
                                                                                                                               1)],
                                                                                                                       {
                                                                                                                           'background': True}),
                                                                                                                   'title': (
                                                                                                                       [
                                                                                                                           (
                                                                                                                               'tags',
                                                                                                                               'text')],
                                                                                                                       {
                                                                                                                           'background': True})},
                                                                                                               'schema': {
                                                                                                                   'id': {
                                                                                                                       'type': 'integer',
                                                                                                                       'required': False,
                                                                                                                       'readonly': True},
                                                                                                                   'type': {
                                                                                                                       'type': 'string',
                                                                                                                       'allowed': [
                                                                                                                           'sharing',
                                                                                                                           'unsafe_act',
                                                                                                                           'near_miss',
                                                                                                                           'incident',
                                                                                                                           'accident']},
                                                                                                                   'flags': {
                                                                                                                       'type': 'dict',
                                                                                                                       'schema': {
                                                                                                                           'aviation': {
                                                                                                                               'type': 'boolean',
                                                                                                                               'default': False},
                                                                                                                           'insurance': {
                                                                                                                               'type': 'boolean',
                                                                                                                               'default': False}}},
                                                                                                                   'ask': {
                                                                                                                       'type': 'dict',
                                                                                                                       'schema': {
                                                                                                                           'attitude': {
                                                                                                                               'type': 'integer',
                                                                                                                               'default': 0},
                                                                                                                           'skills': {
                                                                                                                               'type': 'integer',
                                                                                                                               'default': 0},
                                                                                                                           'knowledge': {
                                                                                                                               'type': 'integer',
                                                                                                                               'default': 0},
                                                                                                                           'text': {
                                                                                                                               'type': 'dict',
                                                                                                                               'default': {}}}},
                                                                                                                   'tags': {
                                                                                                                       'type': 'list',
                                                                                                                       'default': []},
                                                                                                                   'club': {
                                                                                                                       'type': 'string',
                                                                                                                       'required': True},
                                                                                                                   'location': {
                                                                                                                       'type': 'dict',
                                                                                                                       'default': {}},
                                                                                                                   'owner': {
                                                                                                                       'type': 'integer',
                                                                                                                       'readonly': True},
                                                                                                                   'reporter': {
                                                                                                                       'type': 'integer',
                                                                                                                       'readonly': True},
                                                                                                                   'when': {
                                                                                                                       'type': 'datetime',
                                                                                                                       'default': datetime.datetime(
                                                                                                                           2019,
                                                                                                                           1,
                                                                                                                           6,
                                                                                                                           14,
                                                                                                                           11,
                                                                                                                           28,
                                                                                                                           728999)},
                                                                                                                   'involved': {
                                                                                                                       'type': 'list',
                                                                                                                       'default': []},
                                                                                                                   'organization': {
                                                                                                                       'type': 'dict',
                                                                                                                       'default': {}},
                                                                                                                   'rating': {
                                                                                                                       'type': 'dict',
                                                                                                                       'schema': {
                                                                                                                           'actual': {
                                                                                                                               'type': 'integer',
                                                                                                                               'default': 1},
                                                                                                                           'potential': {
                                                                                                                               'type': 'integer',
                                                                                                                               'default': 1}}},
                                                                                                                   'weather': {
                                                                                                                       'type': 'dict',
                                                                                                                       'schema': {
                                                                                                                           'auto': {
                                                                                                                               'type': 'dict'},
                                                                                                                           'manual': {
                                                                                                                               'type': 'dict'}}},
                                                                                                                   'components': {
                                                                                                                       'type': 'list',
                                                                                                                       'default': []},
                                                                                                                   'files': {
                                                                                                                       'type': 'list',
                                                                                                                       'schema': {
                                                                                                                           'type': 'dict',
                                                                                                                           'schema': {
                                                                                                                               'f': {
                                                                                                                                   'type': 'string'},
                                                                                                                               'r': {
                                                                                                                                   'type': 'boolean'}}},
                                                                                                                       'default': []},
                                                                                                                   'related': {
                                                                                                                       'type': 'list',
                                                                                                                       'default': []},
                                                                                                                   'actions': {
                                                                                                                       'type': 'dict'},
                                                                                                                   'comments': {
                                                                                                                       'type': 'list',
                                                                                                                       'default': [],
                                                                                                                       'readonly': True,
                                                                                                                       'schema': {
                                                                                                                           'type': 'dict',
                                                                                                                           'schema': {
                                                                                                                               'date': {
                                                                                                                                   'type': 'datetime'},
                                                                                                                               'user': {
                                                                                                                                   'type': 'integer'},
                                                                                                                               'comment': {
                                                                                                                                   'type': 'string'}}}},
                                                                                                                   'workflow': {
                                                                                                                       'type': 'dict',
                                                                                                                       'readonly': True,
                                                                                                                       'default': {}},
                                                                                                                   'watchers': {
                                                                                                                       'type': 'list',
                                                                                                                       'default': [],
                                                                                                                       'readonly': True},
                                                                                                                   'audit': {
                                                                                                                       'type': 'list',
                                                                                                                       'readonly': True,
                                                                                                                       'default': []},
                                                                                                                   'acl': {
                                                                                                                       'type': 'dict',
                                                                                                                       'readonly': True,
                                                                                                                       'schema': {
                                                                                                                           'read': {
                                                                                                                               'type': 'dict'},
                                                                                                                           'write': {
                                                                                                                               'type': 'dict'},
                                                                                                                           'execute': {
                                                                                                                               'type': 'dict'}}},
                                                                                                                   '_id': {
                                                                                                                       'type': 'objectid'}},
                                                                                                               'public_methods': [],
                                                                                                               'allowed_roles': [],
                                                                                                               'allowed_read_roles': [],
                                                                                                               'allowed_write_roles': [],
                                                                                                               'cache_control': 'max-age=20',
                                                                                                               'cache_expires': 20,
                                                                                                               'id_field': '_id',
                                                                                                               'item_lookup_field': '_id',
                                                                                                               'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                               'resource_title': 'f/observations',
                                                                                                               'item_lookup': True,
                                                                                                               'public_item_methods': [],
                                                                                                               'allowed_item_roles': [],
                                                                                                               'allowed_item_read_roles': [],
                                                                                                               'allowed_item_write_roles': [],
                                                                                                               'allowed_filters': [
                                                                                                                   '*'],
                                                                                                               'sorting': True,
                                                                                                               'embedding': True,
                                                                                                               'embedded_fields': [],
                                                                                                               'pagination': True,
                                                                                                               'projection': True,
                                                                                                               'soft_delete': False,
                                                                                                               'bulk_enabled': True,
                                                                                                               'internal_resource': False,
                                                                                                               'etag_ignore_fields': None,
                                                                                                               'auth_field': None,
                                                                                                               'allow_unknown': False,
                                                                                                               'mongo_write_concern': {
                                                                                                                   'w': 1},
                                                                                                               'hateoas': True,
                                                                                                               'authentication'
                                                                                                               : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'f_ors_agg': {
                                                                                                                   'item_title': 'Observation Aggregations',
                                                                                                                   'url': 'f/observations/aggregate',
                                                                                                                   'datasource': {
                                                                                                                       'source': 'f_observations',
                                                                                                                       'aggregation': {
                                                                                                                           'pipeline': [
                                                                                                                               {
                                                                                                                                   '$unwind': '$type'},
                                                                                                                               {
                                                                                                                                   '$match': {
                                                                                                                                       'when': {
                                                                                                                                           '$gte': '$from',
                                                                                                                                           '$lte': '$to'},
                                                                                                                                       'workflow.state': '$state'}},
                                                                                                                               {
                                                                                                                                   '$group': {
                                                                                                                                       '_id': '$type',
                                                                                                                                       'count': {
                                                                                                                                           '$sum': 1}}},
                                                                                                                               {
                                                                                                                                   '$sort': SON(
                                                                                                                                       [
                                                                                                                                           (
                                                                                                                                               'count',
                                                                                                                                               -1)])}],
                                                                                                                           'options': {}},
                                                                                                                       'filter': None,
                                                                                                                       'default_sort': None,
                                                                                                                       'projection': {
                                                                                                                           '_id': 1,
                                                                                                                           '_updated': 1,
                                                                                                                           '_created': 1,
                                                                                                                           '_etag': 1}},
                                                                                                                   'resource_methods': [
                                                                                                                       'GET'],
                                                                                                                   'public_methods': [],
                                                                                                                   'allowed_roles': [],
                                                                                                                   'allowed_read_roles': [],
                                                                                                                   'allowed_write_roles': [],
                                                                                                                   'cache_control': 'max-age=20',
                                                                                                                   'cache_expires': 20,
                                                                                                                   'id_field': '_id',
                                                                                                                   'item_lookup_field': '_id',
                                                                                                                   'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                   'resource_title': 'f/observations/aggregate',
                                                                                                                   'item_lookup': False,
                                                                                                                   'public_item_methods': [],
                                                                                                                   'allowed_item_roles': [],
                                                                                                                   'allowed_item_read_roles': [],
                                                                                                                   'allowed_item_write_roles': [],
                                                                                                                   'allowed_filters': [
                                                                                                                       '*'],
                                                                                                                   'sorting': True,
                                                                                                                   'embedding': True,
                                                                                                                   'embedded_fields': [],
                                                                                                                   'pagination': True,
                                                                                                                   'projection': True,
                                                                                                                   'versioning': False,
                                                                                                                   'soft_delete': False,
                                                                                                                   'bulk_enabled': True,
                                                                                                                   'internal_resource': False,
                                                                                                                   'etag_ignore_fields': None,
                                                                                                                   'item_methods': [
                                                                                                                       'GET',
                                                                                                                       'PATCH',
                                                                                                                       'DELETE',
                                                                                                                       'PUT'],
                                                                                                                   'auth_field': None,
                                                                                                                   'allow_unknown': False,
                                                                                                                   'extra_response_fields': [],
                                                                                                                   'mongo_write_concern': {
                                                                                                                       'w': 1},
                                                                                                                   'mongo_indexes': {},
                                                                                                                   'hateoas': True,
                                                                                                                   'authentication'
                                                                                                                   : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, 'schema': {
    '_id': {'type': 'objectid'}}, '_media': []}, 'legacy_licenses': {'item_title': 'licenses',
                                                                     'description': 'Licenses with added snacks',
                                                                     'url': 'legacy/licenses',
                                                                     'datasource': {'source': 'legacy_licenses',
                                                                                    'default_sort': [('id', 1)],
                                                                                    'filter': None,
                                                                                    'projection': {'id': 1, 'name': 1,
                                                                                                   'active': 1,
                                                                                                   'url': 1, '_id': 1,
                                                                                                   '_updated': 1,
                                                                                                   '_created': 1,
                                                                                                   '_etag': 1,
                                                                                                   '_version': 1,
                                                                                                   '_id_document': 1},
                                                                                    'aggregation': None},
                                                                     'extra_response_fields': ['id'],
                                                                     'resource_methods': ['GET', 'POST'],
                                                                     'item_methods': ['GET', 'PATCH', 'PUT'],
                                                                     'versioning': True, 'additional_lookup': {
        'url': 'regex("[\\w{1}\\-\\w{1,5}]+")', 'field': 'id'}, 'mongo_indexes': {
        'id': ([('id', 1)], {'background': True}), 'name': ([('name', 1)], {'background': True})}, 'schema': {
        'id': {'type': 'string', 'required': True, 'readonly': True}, 'name': {'type': 'string'},
        'active': {'type': 'boolean'}, 'url': {'type': 'string', 'required': False}, '_id': {'type': 'objectid'}},
                                                                     'public_methods': [], 'allowed_roles': [],
                                                                     'allowed_read_roles': [],
                                                                     'allowed_write_roles': [],
                                                                     'cache_control': 'max-age=20', 'cache_expires': 20,
                                                                     'id_field': '_id', 'item_lookup_field': '_id',
                                                                     'item_url': 'regex("[a-f0-9]{24}")',
                                                                     'resource_title': 'legacy/licenses',
                                                                     'item_lookup': True, 'public_item_methods': [],
                                                                     'allowed_item_roles': [],
                                                                     'allowed_item_read_roles': [],
                                                                     'allowed_item_write_roles': [],
                                                                     'allowed_filters': ['*'], 'sorting': True,
                                                                     'embedding': True, 'embedded_fields': [],
                                                                     'pagination': True, 'projection': True,
                                                                     'soft_delete': False, 'bulk_enabled': True,
                                                                     'internal_resource': False,
                                                                     'etag_ignore_fields': None, 'auth_field': None,
                                                                     'allow_unknown': False,
                                                                     'mongo_write_concern': {'w': 1}, 'hateoas': True,
                                                                     'authentication': < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'legacy_clubs': {
                                                                                                                      'item_title': 'club',
                                                                                                                      'description': 'Legacy clubs with added data',
                                                                                                                      'url': 'legacy/clubs',
                                                                                                                      'datasource': {
                                                                                                                          'source': 'legacy_clubs',
                                                                                                                          'default_sort': [
                                                                                                                              (
                                                                                                                                  'id',
                                                                                                                                  1)],
                                                                                                                          'filter': None,
                                                                                                                          'projection': {
                                                                                                                              'id': 1,
                                                                                                                              'name': 1,
                                                                                                                              'active': 1,
                                                                                                                              'org': 1,
                                                                                                                              'locations': 1,
                                                                                                                              'planes': 1,
                                                                                                                              'roles': 1,
                                                                                                                              'ot': 1,
                                                                                                                              'ci': 1,
                                                                                                                              'logo': 1,
                                                                                                                              'url': 1,
                                                                                                                              '_id': 1,
                                                                                                                              '_updated': 1,
                                                                                                                              '_created': 1,
                                                                                                                              '_etag': 1,
                                                                                                                              '_version': 1,
                                                                                                                              '_id_document': 1},
                                                                                                                          'aggregation': None},
                                                                                                                      'extra_response_fields': [
                                                                                                                          'id'],
                                                                                                                      'resource_methods': [
                                                                                                                          'GET',
                                                                                                                          'POST'],
                                                                                                                      'item_methods': [
                                                                                                                          'GET',
                                                                                                                          'PATCH',
                                                                                                                          'PUT'],
                                                                                                                      'versioning': True,
                                                                                                                      'additional_lookup': {
                                                                                                                          'url': 'regex("[\\d{3}\\-\\w{1}]+")',
                                                                                                                          'field': 'id'},
                                                                                                                      'mongo_indexes': {
                                                                                                                          'id': (
                                                                                                                              [
                                                                                                                                  (
                                                                                                                                      'id',
                                                                                                                                      1)],
                                                                                                                              {
                                                                                                                                  'background': True}),
                                                                                                                          'name': (
                                                                                                                              [
                                                                                                                                  (
                                                                                                                                      'name',
                                                                                                                                      1)],
                                                                                                                              {
                                                                                                                                  'background': True})},
                                                                                                                      'schema': {
                                                                                                                          'id': {
                                                                                                                              'type': 'string',
                                                                                                                              'required': True,
                                                                                                                              'readonly': True},
                                                                                                                          'name': {
                                                                                                                              'type': 'string'},
                                                                                                                          'active': {
                                                                                                                              'type': 'boolean'},
                                                                                                                          'org': {
                                                                                                                              'type': 'string'},
                                                                                                                          'locations': {
                                                                                                                              'type': 'list'},
                                                                                                                          'planes': {
                                                                                                                              'type': 'dict'},
                                                                                                                          'roles': {
                                                                                                                              'type': 'dict'},
                                                                                                                          'ot': {
                                                                                                                              'type': 'integer',
                                                                                                                              'required': True,
                                                                                                                              'allowed': [
                                                                                                                                  1,
                                                                                                                                  2]},
                                                                                                                          'ci': {
                                                                                                                              'type': 'integer',
                                                                                                                              'required': False},
                                                                                                                          'logo': {
                                                                                                                              'type': 'media',
                                                                                                                              'required': False},
                                                                                                                          'url': {
                                                                                                                              'type': 'string',
                                                                                                                              'required': False},
                                                                                                                          '_id': {
                                                                                                                              'type': 'objectid'}},
                                                                                                                      'public_methods': [],
                                                                                                                      'allowed_roles': [],
                                                                                                                      'allowed_read_roles': [],
                                                                                                                      'allowed_write_roles': [],
                                                                                                                      'cache_control': 'max-age=20',
                                                                                                                      'cache_expires': 20,
                                                                                                                      'id_field': '_id',
                                                                                                                      'item_lookup_field': '_id',
                                                                                                                      'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                      'resource_title': 'legacy/clubs',
                                                                                                                      'item_lookup': True,
                                                                                                                      'public_item_methods': [],
                                                                                                                      'allowed_item_roles': [],
                                                                                                                      'allowed_item_read_roles': [],
                                                                                                                      'allowed_item_write_roles': [],
                                                                                                                      'allowed_filters': [
                                                                                                                          '*'],
                                                                                                                      'sorting': True,
                                                                                                                      'embedding': True,
                                                                                                                      'embedded_fields': [],
                                                                                                                      'pagination': True,
                                                                                                                      'projection': True,
                                                                                                                      'soft_delete': False,
                                                                                                                      'bulk_enabled': True,
                                                                                                                      'internal_resource': False,
                                                                                                                      'etag_ignore_fields': None,
                                                                                                                      'auth_field': None,
                                                                                                                      'allow_unknown': False,
                                                                                                                      'mongo_write_concern': {
                                                                                                                          'w': 1},
                                                                                                                      'hateoas': True,
                                                                                                                      'authentication'
                                                                                                                      : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': [
    'logo']}, 'legacy_melwin_licenses': {'item_title': 'Legacy Melwin licenses', 'url': 'legacy/melwin/licenses',
                                         'description': 'Melwin passthrough',
                                         'datasource': {'source': 'legacy_melwin_licenses', 'default_sort': [('id', 1)],
                                                        'filter': None,
                                                        'projection': {'id': 1, 'name': 1, '_id': 1, '_updated': 1,
                                                                       '_created': 1, '_etag': 1}, 'aggregation': None},
                                         'resource_methods': ['GET'], 'item_methods': ['GET'], 'versioning': False,
                                         'additional_lookup': {'url': 'regex("[\\w{1}\\-\\w{1,5}]+")', 'field': 'id'},
                                         'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                                                           'name': ([('name', 1)], {'background': True})},
                                         'schema': {'id': {'type': 'string', 'required': True},
                                                    'name': {'type': 'string'}, '_id': {'type': 'objectid'}},
                                         'public_methods': [], 'allowed_roles': [], 'allowed_read_roles': [],
                                         'allowed_write_roles': [], 'cache_control': 'max-age=20', 'cache_expires': 20,
                                         'id_field': '_id', 'item_lookup_field': '_id',
                                         'item_url': 'regex("[a-f0-9]{24}")',
                                         'resource_title': 'legacy/melwin/licenses', 'item_lookup': True,
                                         'public_item_methods': [], 'allowed_item_roles': [],
                                         'allowed_item_read_roles': [], 'allowed_item_write_roles': [],
                                         'allowed_filters': ['*'], 'sorting': True, 'embedding': True,
                                         'embedded_fields': [], 'pagination': True, 'projection': True,
                                         'soft_delete': False, 'bulk_enabled': True, 'internal_resource': False,
                                         'etag_ignore_fields': None, 'auth_field': None, 'allow_unknown': False,
                                         'extra_response_fields': [], 'mongo_write_concern': {'w': 1}, 'hateoas': True,
                                         'authentication': < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'legacy_melwin_membership': {
                                                                                                                                  'item_title': 'membership',
                                                                                                                                  'description': 'Melwin passthrough',
                                                                                                                                  'url': 'legacy/melwin/membership',
                                                                                                                                  'datasource': {
                                                                                                                                      'source': 'legacy_melwin_membership',
                                                                                                                                      'default_sort': [
                                                                                                                                          (
                                                                                                                                              'id',
                                                                                                                                              1)],
                                                                                                                                      'filter': None,
                                                                                                                                      'projection': {
                                                                                                                                          'id': 1,
                                                                                                                                          'name': 1,
                                                                                                                                          '_id': 1,
                                                                                                                                          '_updated': 1,
                                                                                                                                          '_created': 1,
                                                                                                                                          '_etag': 1},
                                                                                                                                      'aggregation': None},
                                                                                                                                  'resource_methods': [
                                                                                                                                      'GET'],
                                                                                                                                  'item_methods': [
                                                                                                                                      'GET'],
                                                                                                                                  'versioning': False,
                                                                                                                                  'additional_lookup': {
                                                                                                                                      'url': 'regex("[\\w{3}]+")',
                                                                                                                                      'field': 'id'},
                                                                                                                                  'mongo_indexes': {
                                                                                                                                      'id': (
                                                                                                                                          [
                                                                                                                                              (
                                                                                                                                                  'id',
                                                                                                                                                  1)],
                                                                                                                                          {
                                                                                                                                              'background': True}),
                                                                                                                                      'name': (
                                                                                                                                          [
                                                                                                                                              (
                                                                                                                                                  'name',
                                                                                                                                                  1)],
                                                                                                                                          {
                                                                                                                                              'background': True})},
                                                                                                                                  'schema': {
                                                                                                                                      'id': {
                                                                                                                                          'type': 'string',
                                                                                                                                          'required': True},
                                                                                                                                      'name': {
                                                                                                                                          'type': 'string'},
                                                                                                                                      '_id': {
                                                                                                                                          'type': 'objectid'}},
                                                                                                                                  'public_methods': [],
                                                                                                                                  'allowed_roles': [],
                                                                                                                                  'allowed_read_roles': [],
                                                                                                                                  'allowed_write_roles': [],
                                                                                                                                  'cache_control': 'max-age=20',
                                                                                                                                  'cache_expires': 20,
                                                                                                                                  'id_field': '_id',
                                                                                                                                  'item_lookup_field': '_id',
                                                                                                                                  'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                                  'resource_title': 'legacy/melwin/membership',
                                                                                                                                  'item_lookup': True,
                                                                                                                                  'public_item_methods': [],
                                                                                                                                  'allowed_item_roles': [],
                                                                                                                                  'allowed_item_read_roles': [],
                                                                                                                                  'allowed_item_write_roles': [],
                                                                                                                                  'allowed_filters': [
                                                                                                                                      '*'],
                                                                                                                                  'sorting': True,
                                                                                                                                  'embedding': True,
                                                                                                                                  'embedded_fields': [],
                                                                                                                                  'pagination': True,
                                                                                                                                  'projection': True,
                                                                                                                                  'soft_delete': False,
                                                                                                                                  'bulk_enabled': True,
                                                                                                                                  'internal_resource': False,
                                                                                                                                  'etag_ignore_fields': None,
                                                                                                                                  'auth_field': None,
                                                                                                                                  'allow_unknown': False,
                                                                                                                                  'extra_response_fields': [],
                                                                                                                                  'mongo_write_concern': {
                                                                                                                                      'w': 1},
                                                                                                                                  'hateoas': True,
                                                                                                                                  'authentication'
                                                                                                                                  : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'legacy_melwin_clubs': {
                                                                                                                             'item_title': 'club',
                                                                                                                             'url': 'legacy/melwin/clubs',
                                                                                                                             'description': 'Melwin passthrough',
                                                                                                                             'datasource': {
                                                                                                                                 'source': 'legacy_melwin_clubs',
                                                                                                                                 'default_sort': [
                                                                                                                                     (
                                                                                                                                         'id',
                                                                                                                                         1)],
                                                                                                                                 'filter': None,
                                                                                                                                 'projection': {
                                                                                                                                     'id': 1,
                                                                                                                                     'name': 1,
                                                                                                                                     '_id': 1,
                                                                                                                                     '_updated': 1,
                                                                                                                                     '_created': 1,
                                                                                                                                     '_etag': 1},
                                                                                                                                 'aggregation': None},
                                                                                                                             'resource_methods': [
                                                                                                                                 'GET'],
                                                                                                                             'item_methods': [
                                                                                                                                 'GET'],
                                                                                                                             'versioning': False,
                                                                                                                             'additional_lookup': {
                                                                                                                                 'url': 'regex("[\\d{3}\\-\\w{1}]+")',
                                                                                                                                 'field': 'id'},
                                                                                                                             'mongo_indexes': {
                                                                                                                                 'id': (
                                                                                                                                     [
                                                                                                                                         (
                                                                                                                                             'id',
                                                                                                                                             1)],
                                                                                                                                     {
                                                                                                                                         'background': True}),
                                                                                                                                 'name': (
                                                                                                                                     [
                                                                                                                                         (
                                                                                                                                             'name',
                                                                                                                                             1)],
                                                                                                                                     {
                                                                                                                                         'background': True})},
                                                                                                                             'schema': {
                                                                                                                                 'id': {
                                                                                                                                     'type': 'string',
                                                                                                                                     'required': True},
                                                                                                                                 'name': {
                                                                                                                                     'type': 'string'},
                                                                                                                                 '_id': {
                                                                                                                                     'type': 'objectid'}},
                                                                                                                             'public_methods': [],
                                                                                                                             'allowed_roles': [],
                                                                                                                             'allowed_read_roles': [],
                                                                                                                             'allowed_write_roles': [],
                                                                                                                             'cache_control': 'max-age=20',
                                                                                                                             'cache_expires': 20,
                                                                                                                             'id_field': '_id',
                                                                                                                             'item_lookup_field': '_id',
                                                                                                                             'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                             'resource_title': 'legacy/melwin/clubs',
                                                                                                                             'item_lookup': True,
                                                                                                                             'public_item_methods': [],
                                                                                                                             'allowed_item_roles': [],
                                                                                                                             'allowed_item_read_roles': [],
                                                                                                                             'allowed_item_write_roles': [],
                                                                                                                             'allowed_filters': [
                                                                                                                                 '*'],
                                                                                                                             'sorting': True,
                                                                                                                             'embedding': True,
                                                                                                                             'embedded_fields': [],
                                                                                                                             'pagination': True,
                                                                                                                             'projection': True,
                                                                                                                             'soft_delete': False,
                                                                                                                             'bulk_enabled': True,
                                                                                                                             'internal_resource': False,
                                                                                                                             'etag_ignore_fields': None,
                                                                                                                             'auth_field': None,
                                                                                                                             'allow_unknown': False,
                                                                                                                             'extra_response_fields': [],
                                                                                                                             'mongo_write_concern': {
                                                                                                                                 'w': 1},
                                                                                                                             'hateoas': True,
                                                                                                                             'authentication'
                                                                                                                             : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'legacy_melwin_users': {
                                                                                                                             'item_title': 'Melwin Users',
                                                                                                                             'name': 'melwin/users',
                                                                                                                             'description': 'Melwin passthrough',
                                                                                                                             'url': 'legacy/melwin/users',
                                                                                                                             'datasource': {
                                                                                                                                 'source': 'legacy_melwin_users',
                                                                                                                                 'default_sort': [
                                                                                                                                     (
                                                                                                                                         'id',
                                                                                                                                         1)],
                                                                                                                                 'filter': None,
                                                                                                                                 'projection': {
                                                                                                                                     'id': 1,
                                                                                                                                     'active': 1,
                                                                                                                                     'updated': 1,
                                                                                                                                     'firstname': 1,
                                                                                                                                     'lastname': 1,
                                                                                                                                     'fullname': 1,
                                                                                                                                     'birthdate': 1,
                                                                                                                                     'gender': 1,
                                                                                                                                     'email': 1,
                                                                                                                                     'phone': 1,
                                                                                                                                     'location': 1,
                                                                                                                                     'membership': 1,
                                                                                                                                     'licenses': 1,
                                                                                                                                     '_id': 1,
                                                                                                                                     '_updated': 1,
                                                                                                                                     '_created': 1,
                                                                                                                                     '_etag': 1},
                                                                                                                                 'aggregation': None},
                                                                                                                             'resource_methods': [
                                                                                                                                 'GET'],
                                                                                                                             'item_methods': [
                                                                                                                                 'GET'],
                                                                                                                             'additional_lookup': {
                                                                                                                                 'url': 'regex("[\\d{1,10}]+")',
                                                                                                                                 'field': 'id'},
                                                                                                                             'versioning': False,
                                                                                                                             'mongo_indexes': {
                                                                                                                                 'id': (
                                                                                                                                     [
                                                                                                                                         (
                                                                                                                                             'id',
                                                                                                                                             1)],
                                                                                                                                     {
                                                                                                                                         'background': True}),
                                                                                                                                 'gender': (
                                                                                                                                     [
                                                                                                                                         (
                                                                                                                                             'gender',
                                                                                                                                             1)],
                                                                                                                                     {
                                                                                                                                         'background': True}),
                                                                                                                                 'membership': (
                                                                                                                                     [
                                                                                                                                         (
                                                                                                                                             'membership',
                                                                                                                                             1)],
                                                                                                                                     {
                                                                                                                                         'background': True}),
                                                                                                                                 'licenses': (
                                                                                                                                     [
                                                                                                                                         (
                                                                                                                                             'licenses',
                                                                                                                                             1)],
                                                                                                                                     {
                                                                                                                                         'background': True}),
                                                                                                                                 'text': (
                                                                                                                                     [
                                                                                                                                         (
                                                                                                                                             'fullname',
                                                                                                                                             'text'),
                                                                                                                                         (
                                                                                                                                             'body',
                                                                                                                                             'text')],
                                                                                                                                     {
                                                                                                                                         'background': True})},
                                                                                                                             'schema': {
                                                                                                                                 'id': {
                                                                                                                                     'type': 'integer',
                                                                                                                                     'unique': True,
                                                                                                                                     'required': True},
                                                                                                                                 'active': {
                                                                                                                                     'type': 'boolean'},
                                                                                                                                 'updated': {
                                                                                                                                     'type': 'datetime'},
                                                                                                                                 'firstname': {
                                                                                                                                     'type': 'string',
                                                                                                                                     'required': True},
                                                                                                                                 'lastname': {
                                                                                                                                     'type': 'string',
                                                                                                                                     'required': True},
                                                                                                                                 'fullname': {
                                                                                                                                     'type': 'string'},
                                                                                                                                 'birthdate': {
                                                                                                                                     'type': 'datetime'},
                                                                                                                                 'gender': {
                                                                                                                                     'type': 'string',
                                                                                                                                     'maxlength': 1,
                                                                                                                                     'allowed': [
                                                                                                                                         'M',
                                                                                                                                         'F']},
                                                                                                                                 'email': {
                                                                                                                                     'type': 'string'},
                                                                                                                                 'phone': {
                                                                                                                                     'type': 'string'},
                                                                                                                                 'location': {
                                                                                                                                     'type': 'dict',
                                                                                                                                     'schema': {
                                                                                                                                         'street': {
                                                                                                                                             'type': 'string'},
                                                                                                                                         'zip': {
                                                                                                                                             'type': 'string'},
                                                                                                                                         'city': {
                                                                                                                                             'type': 'string'},
                                                                                                                                         'country': {
                                                                                                                                             'type': 'string'},
                                                                                                                                         'geo': {
                                                                                                                                             'type': 'point'},
                                                                                                                                         'geo_class': {
                                                                                                                                             'type': 'string'},
                                                                                                                                         'geo_importance': {
                                                                                                                                             'type': 'float'},
                                                                                                                                         'geo_place_id': {
                                                                                                                                             'type': 'integer'},
                                                                                                                                         'geo_type': {
                                                                                                                                             'type': 'string'}}},
                                                                                                                                 'membership': {
                                                                                                                                     'type': 'dict',
                                                                                                                                     'schema': {
                                                                                                                                         'type': {
                                                                                                                                             'type': 'string'},
                                                                                                                                         'clubs': {
                                                                                                                                             'type': 'list'},
                                                                                                                                         'valid': {
                                                                                                                                             'type': 'datetime'},
                                                                                                                                         'enrolled': {
                                                                                                                                             'type': 'datetime'},
                                                                                                                                         'balance': {
                                                                                                                                             'type': 'number'},
                                                                                                                                         'fee': {
                                                                                                                                             'type': 'number'}}},
                                                                                                                                 'licenses': {
                                                                                                                                     'type': 'dict',
                                                                                                                                     'schema': {
                                                                                                                                         'rights': {
                                                                                                                                             'type': 'list'},
                                                                                                                                         'expiry': {
                                                                                                                                             'type': 'datetime'}}},
                                                                                                                                 '_id': {
                                                                                                                                     'type': 'objectid'}},
                                                                                                                             'public_methods': [],
                                                                                                                             'allowed_roles': [],
                                                                                                                             'allowed_read_roles': [],
                                                                                                                             'allowed_write_roles': [],
                                                                                                                             'cache_control': 'max-age=20',
                                                                                                                             'cache_expires': 20,
                                                                                                                             'id_field': '_id',
                                                                                                                             'item_lookup_field': '_id',
                                                                                                                             'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                             'resource_title': 'legacy/melwin/users',
                                                                                                                             'item_lookup': True,
                                                                                                                             'public_item_methods': [],
                                                                                                                             'allowed_item_roles': [],
                                                                                                                             'allowed_item_read_roles': [],
                                                                                                                             'allowed_item_write_roles': [],
                                                                                                                             'allowed_filters': [
                                                                                                                                 '*'],
                                                                                                                             'sorting': True,
                                                                                                                             'embedding': True,
                                                                                                                             'embedded_fields': [],
                                                                                                                             'pagination': True,
                                                                                                                             'projection': True,
                                                                                                                             'soft_delete': False,
                                                                                                                             'bulk_enabled': True,
                                                                                                                             'internal_resource': False,
                                                                                                                             'etag_ignore_fields': None,
                                                                                                                             'auth_field': None,
                                                                                                                             'allow_unknown': False,
                                                                                                                             'extra_response_fields': [],
                                                                                                                             'mongo_write_concern': {
                                                                                                                                 'w': 1},
                                                                                                                             'hateoas': True,
                                                                                                                             'authentication'
                                                                                                                             : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'content': {
                                                                                                                 'item_title': 'content',
                                                                                                                 'url': 'content',
                                                                                                                 'datasource': {
                                                                                                                     'source': 'content',
                                                                                                                     'filter': None,
                                                                                                                     'default_sort': None,
                                                                                                                     'projection': {
                                                                                                                         'title': 1,
                                                                                                                         'slug': 1,
                                                                                                                         'body': 1,
                                                                                                                         'space_key': 1,
                                                                                                                         'parent': 1,
                                                                                                                         'order': 1,
                                                                                                                         'ref': 1,
                                                                                                                         'owner': 1,
                                                                                                                         '_id': 1,
                                                                                                                         '_updated': 1,
                                                                                                                         '_created': 1,
                                                                                                                         '_etag': 1,
                                                                                                                         '_version': 1,
                                                                                                                         '_id_document': 1},
                                                                                                                     'aggregation': None},
                                                                                                                 'additional_lookup': {
                                                                                                                     'url': 'regex("[a-z0-9-]+")',
                                                                                                                     'field': 'slug'},
                                                                                                                 'extra_response_fields': [
                                                                                                                     'key'],
                                                                                                                 'versioning': True,
                                                                                                                 'resource_methods': [
                                                                                                                     'GET',
                                                                                                                     'POST'],
                                                                                                                 'item_methods': [
                                                                                                                     'GET',
                                                                                                                     'PATCH',
                                                                                                                     'DELETE'],
                                                                                                                 'mongo_indexes': {
                                                                                                                     'slug': (
                                                                                                                         [
                                                                                                                             (
                                                                                                                                 'slug',
                                                                                                                                 1)],
                                                                                                                         {
                                                                                                                             'background': True}),
                                                                                                                     'space': (
                                                                                                                         [
                                                                                                                             (
                                                                                                                                 'space_key',
                                                                                                                                 1)],
                                                                                                                         {
                                                                                                                             'background': True}),
                                                                                                                     'parent': (
                                                                                                                         [
                                                                                                                             (
                                                                                                                                 'parent',
                                                                                                                                 1)],
                                                                                                                         {
                                                                                                                             'background': True}),
                                                                                                                     'owner': (
                                                                                                                         [
                                                                                                                             (
                                                                                                                                 'owner',
                                                                                                                                 1)],
                                                                                                                         {
                                                                                                                             'background': True}),
                                                                                                                     'content': (
                                                                                                                         [
                                                                                                                             (
                                                                                                                                 'title',
                                                                                                                                 'text'),
                                                                                                                             (
                                                                                                                                 'body',
                                                                                                                                 'text')],
                                                                                                                         {
                                                                                                                             'background': True})},
                                                                                                                 'schema': {
                                                                                                                     'title': {
                                                                                                                         'type': 'string',
                                                                                                                         'required': True,
                                                                                                                         'readonly': False},
                                                                                                                     'slug': {
                                                                                                                         'type': 'string',
                                                                                                                         'required': True},
                                                                                                                     'body': {
                                                                                                                         'type': 'string',
                                                                                                                         'required': True},
                                                                                                                     'space_key': {
                                                                                                                         'type': 'string',
                                                                                                                         'required': True},
                                                                                                                     'parent': {
                                                                                                                         'type': 'objectid',
                                                                                                                         'default': None},
                                                                                                                     'order': {
                                                                                                                         'type': 'integer'},
                                                                                                                     'ref': {
                                                                                                                         'type': 'string'},
                                                                                                                     'owner': {
                                                                                                                         'type': 'integer',
                                                                                                                         'required': False,
                                                                                                                         'readonly': True},
                                                                                                                     '_id': {
                                                                                                                         'type': 'objectid'}},
                                                                                                                 'public_methods': [],
                                                                                                                 'allowed_roles': [],
                                                                                                                 'allowed_read_roles': [],
                                                                                                                 'allowed_write_roles': [],
                                                                                                                 'cache_control': 'max-age=20',
                                                                                                                 'cache_expires': 20,
                                                                                                                 'id_field': '_id',
                                                                                                                 'item_lookup_field': '_id',
                                                                                                                 'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                 'resource_title': 'content',
                                                                                                                 'item_lookup': True,
                                                                                                                 'public_item_methods': [],
                                                                                                                 'allowed_item_roles': [],
                                                                                                                 'allowed_item_read_roles': [],
                                                                                                                 'allowed_item_write_roles': [],
                                                                                                                 'allowed_filters': [
                                                                                                                     '*'],
                                                                                                                 'sorting': True,
                                                                                                                 'embedding': True,
                                                                                                                 'embedded_fields': [],
                                                                                                                 'pagination': True,
                                                                                                                 'projection': True,
                                                                                                                 'soft_delete': False,
                                                                                                                 'bulk_enabled': True,
                                                                                                                 'internal_resource': False,
                                                                                                                 'etag_ignore_fields': None,
                                                                                                                 'auth_field': None,
                                                                                                                 'allow_unknown': False,
                                                                                                                 'mongo_write_concern': {
                                                                                                                     'w': 1},
                                                                                                                 'hateoas': True,
                                                                                                                 'authentication'
                                                                                                                 : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'content_aggregate_parents': {
                                                                                                                                   'item_title': 'Content Parents Aggregation',
                                                                                                                                   'url': 'content/aggregate/parents',
                                                                                                                                   'datasource': {
                                                                                                                                       'source': 'content',
                                                                                                                                       'aggregation': {
                                                                                                                                           'pipeline': [
                                                                                                                                               {
                                                                                                                                                   '$match': {
                                                                                                                                                       '_id': '$start_id',
                                                                                                                                                       'parent': {
                                                                                                                                                           '$ne': None}}},
                                                                                                                                               {
                                                                                                                                                   '$project': {
                                                                                                                                                       '_id': 1,
                                                                                                                                                       'title': 1,
                                                                                                                                                       'slug': 1,
                                                                                                                                                       'space_key': 1,
                                                                                                                                                       'parent': 1}},
                                                                                                                                               {
                                                                                                                                                   '$graphLookup': {
                                                                                                                                                       'from': 'content',
                                                                                                                                                       'startWith': '$parent',
                                                                                                                                                       'connectFromField': 'parent',
                                                                                                                                                       'connectToField': '_id',
                                                                                                                                                       'maxDepth': 3,
                                                                                                                                                       'depthField': 'levelAbove',
                                                                                                                                                       'as': 'parents'}},
                                                                                                                                               {
                                                                                                                                                   '$project': {
                                                                                                                                                       'parents._id': 1,
                                                                                                                                                       'parents.title': 1,
                                                                                                                                                       'parents.slug': 1,
                                                                                                                                                       'parents.space_key': 1,
                                                                                                                                                       'parents.levelAbove': 1}},
                                                                                                                                               {
                                                                                                                                                   '$sort': SON(
                                                                                                                                                       [
                                                                                                                                                           (
                                                                                                                                                               'parents.levelAbove',
                                                                                                                                                               -1)])}],
                                                                                                                                           'options': {}},
                                                                                                                                       'filter': None,
                                                                                                                                       'default_sort': None,
                                                                                                                                       'projection': {
                                                                                                                                           '_id': 1,
                                                                                                                                           '_updated': 1,
                                                                                                                                           '_created': 1,
                                                                                                                                           '_etag': 1}},
                                                                                                                                   'resource_methods': [
                                                                                                                                       'GET'],
                                                                                                                                   'public_methods': [],
                                                                                                                                   'allowed_roles': [],
                                                                                                                                   'allowed_read_roles': [],
                                                                                                                                   'allowed_write_roles': [],
                                                                                                                                   'cache_control': 'max-age=20',
                                                                                                                                   'cache_expires': 20,
                                                                                                                                   'id_field': '_id',
                                                                                                                                   'item_lookup_field': '_id',
                                                                                                                                   'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                                   'resource_title': 'content/aggregate/parents',
                                                                                                                                   'item_lookup': False,
                                                                                                                                   'public_item_methods': [],
                                                                                                                                   'allowed_item_roles': [],
                                                                                                                                   'allowed_item_read_roles': [],
                                                                                                                                   'allowed_item_write_roles': [],
                                                                                                                                   'allowed_filters': [
                                                                                                                                       '*'],
                                                                                                                                   'sorting': True,
                                                                                                                                   'embedding': True,
                                                                                                                                   'embedded_fields': [],
                                                                                                                                   'pagination': True,
                                                                                                                                   'projection': True,
                                                                                                                                   'versioning': False,
                                                                                                                                   'soft_delete': False,
                                                                                                                                   'bulk_enabled': True,
                                                                                                                                   'internal_resource': False,
                                                                                                                                   'etag_ignore_fields': None,
                                                                                                                                   'item_methods': [
                                                                                                                                       'GET',
                                                                                                                                       'PATCH',
                                                                                                                                       'DELETE',
                                                                                                                                       'PUT'],
                                                                                                                                   'auth_field': None,
                                                                                                                                   'allow_unknown': False,
                                                                                                                                   'extra_response_fields': [],
                                                                                                                                   'mongo_write_concern': {
                                                                                                                                       'w': 1},
                                                                                                                                   'mongo_indexes': {},
                                                                                                                                   'hateoas': True,
                                                                                                                                   'authentication'
                                                                                                                                   : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, 'schema': {
    '_id': {'type': 'objectid'}}, '_media': []}, 'content_aggregate_children': {
                                                                                   'item_title': 'Content Children Aggregation',
                                                                                   'url': 'content/aggregate/children',
                                                                                   'datasource': {'source': 'content',
                                                                                                  'aggregation': {
                                                                                                      'pipeline': [{
                                                                                                          '$match': {
                                                                                                              '_id': '$start_id'}},
                                                                                                          {
                                                                                                              '$project': {
                                                                                                                  '_id': 1,
                                                                                                                  'title': 1,
                                                                                                                  'slug': 1,
                                                                                                                  'space_key': 1}},
                                                                                                          {
                                                                                                              '$graphLookup': {
                                                                                                                  'from': 'content',
                                                                                                                  'startWith': '$_id',
                                                                                                                  'connectFromField': '_id',
                                                                                                                  'connectToField': 'parent',
                                                                                                                  'maxDepth': '$max_depth',
                                                                                                                  'depthField': 'levelBelove',
                                                                                                                  'as': 'children'}},
                                                                                                          {
                                                                                                              '$project': {
                                                                                                                  'children._id': 1,
                                                                                                                  'children.title': 1,
                                                                                                                  'children.slug': 1,
                                                                                                                  'children.space_key': 1,
                                                                                                                  'children.levelBelove': 1}},
                                                                                                          {
                                                                                                              '$sort': {
                                                                                                                  'children.leveBelove': 1}}],
                                                                                                      'options': {}},
                                                                                                  'filter': None,
                                                                                                  'default_sort': None,
                                                                                                  'projection': {
                                                                                                      '_id': 1,
                                                                                                      '_updated': 1,
                                                                                                      '_created': 1,
                                                                                                      '_etag': 1}},
                                                                                   'resource_methods': ['GET'],
                                                                                   'public_methods': [],
                                                                                   'allowed_roles': [],
                                                                                   'allowed_read_roles': [],
                                                                                   'allowed_write_roles': [],
                                                                                   'cache_control': 'max-age=20',
                                                                                   'cache_expires': 20,
                                                                                   'id_field': '_id',
                                                                                   'item_lookup_field': '_id',
                                                                                   'item_url': 'regex("[a-f0-9]{24}")',
                                                                                   'resource_title': 'content/aggregate/children',
                                                                                   'item_lookup': False,
                                                                                   'public_item_methods': [],
                                                                                   'allowed_item_roles': [],
                                                                                   'allowed_item_read_roles': [],
                                                                                   'allowed_item_write_roles': [],
                                                                                   'allowed_filters': ['*'],
                                                                                   'sorting': True, 'embedding': True,
                                                                                   'embedded_fields': [],
                                                                                   'pagination': True,
                                                                                   'projection': True,
                                                                                   'versioning': False,
                                                                                   'soft_delete': False,
                                                                                   'bulk_enabled': True,
                                                                                   'internal_resource': False,
                                                                                   'etag_ignore_fields': None,
                                                                                   'item_methods': ['GET', 'PATCH',
                                                                                                    'DELETE', 'PUT'],
                                                                                   'auth_field': None,
                                                                                   'allow_unknown': False,
                                                                                   'extra_response_fields': [],
                                                                                   'mongo_write_concern': {'w': 1},
                                                                                   'mongo_indexes': {}, 'hateoas': True,
                                                                                   'authentication'
                                                                                   : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, 'schema': {
    '_id': {'type': 'objectid'}}, '_media': []}, 'content_aggregate_siblings': {
                                                                                   'item_title': 'Content Siblings Aggregation',
                                                                                   'url': 'content/aggregate/siblings',
                                                                                   'datasource': {'source': 'content',
                                                                                                  'aggregation': {
                                                                                                      'pipeline': [{
                                                                                                          '$match': {
                                                                                                              '_id': '$parent_id'}},
                                                                                                          {
                                                                                                              '$project': {
                                                                                                                  '_id': 1,
                                                                                                                  'title': 1,
                                                                                                                  'slug': 1,
                                                                                                                  'space_key': 1}},
                                                                                                          {
                                                                                                              '$graphLookup': {
                                                                                                                  'from': 'content',
                                                                                                                  'startWith': '$_id',
                                                                                                                  'connectFromField': '_id',
                                                                                                                  'connectToField': 'parent',
                                                                                                                  'maxDepth': 0,
                                                                                                                  'depthField': 'levelBelove',
                                                                                                                  'restrictSearchWithMatch': {
                                                                                                                      '_id': {
                                                                                                                          '$ne': '$current_id'}},
                                                                                                                  'as': 'siblings'}},
                                                                                                          {
                                                                                                              '$project': {
                                                                                                                  'siblings._id': 1,
                                                                                                                  'siblings.title': 1,
                                                                                                                  'siblings.slug': 1,
                                                                                                                  'siblings.space_key': 1,
                                                                                                                  'siblings.levelBelove': 1}},
                                                                                                          {
                                                                                                              '$sort': {
                                                                                                                  'siblings.leveBelove': 1}}],
                                                                                                      'options': {}},
                                                                                                  'filter': None,
                                                                                                  'default_sort': None,
                                                                                                  'projection': {
                                                                                                      '_id': 1,
                                                                                                      '_updated': 1,
                                                                                                      '_created': 1,
                                                                                                      '_etag': 1}},
                                                                                   'resource_methods': ['GET'],
                                                                                   'public_methods': [],
                                                                                   'allowed_roles': [],
                                                                                   'allowed_read_roles': [],
                                                                                   'allowed_write_roles': [],
                                                                                   'cache_control': 'max-age=20',
                                                                                   'cache_expires': 20,
                                                                                   'id_field': '_id',
                                                                                   'item_lookup_field': '_id',
                                                                                   'item_url': 'regex("[a-f0-9]{24}")',
                                                                                   'resource_title': 'content/aggregate/siblings',
                                                                                   'item_lookup': False,
                                                                                   'public_item_methods': [],
                                                                                   'allowed_item_roles': [],
                                                                                   'allowed_item_read_roles': [],
                                                                                   'allowed_item_write_roles': [],
                                                                                   'allowed_filters': ['*'],
                                                                                   'sorting': True, 'embedding': True,
                                                                                   'embedded_fields': [],
                                                                                   'pagination': True,
                                                                                   'projection': True,
                                                                                   'versioning': False,
                                                                                   'soft_delete': False,
                                                                                   'bulk_enabled': True,
                                                                                   'internal_resource': False,
                                                                                   'etag_ignore_fields': None,
                                                                                   'item_methods': ['GET', 'PATCH',
                                                                                                    'DELETE', 'PUT'],
                                                                                   'auth_field': None,
                                                                                   'allow_unknown': False,
                                                                                   'extra_response_fields': [],
                                                                                   'mongo_write_concern': {'w': 1},
                                                                                   'mongo_indexes': {}, 'hateoas': True,
                                                                                   'authentication'
                                                                                   : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, 'schema': {
    '_id': {'type': 'objectid'}}, '_media': []}, 'files': {'item_title': 'Files',
                                                           'description': 'Universal file storage and retrieval',
                                                           'url': 'files',
                                                           'datasource': {'source': 'files', 'filter': None,
                                                                          'default_sort': None,
                                                                          'projection': {'name': 1, 'description': 1,
                                                                                         'tags': 1, 'content_type': 1,
                                                                                         'size': 1, 'owner': 1,
                                                                                         'ref': 1, 'ref_id': 1,
                                                                                         'file': 1, 'acl': 1, '_id': 1,
                                                                                         '_updated': 1, '_created': 1,
                                                                                         '_etag': 1, '_version': 1,
                                                                                         '_id_document': 1},
                                                                          'aggregation': None},
                                                           'resource_methods': ['GET', 'POST'],
                                                           'item_methods': ['GET', 'PATCH'], 'versioning': True,
                                                           'mongo_indexes': {
                                                               'name': ([('slug', 1)], {'background': True}),
                                                               'tags': ([('tags', 1)], {'background': True}),
                                                               'content': ([('content_type', 1)], {'background': True}),
                                                               'ref': (
                                                                   [('ref', 1), ('ref_id', 1)], {'background': True}),
                                                               'owner': ([('owner', 1)], {'background': True}),
                                                               'acl': ([('acl', 1)], {'background': True}), 'descr': (
                                                                   [('description', 'text'), ('name', 'text')],
                                                                   {'background': True})},
                                                           'schema': {'name': {'type': 'string'},
                                                                      'description': {'type': 'string'},
                                                                      'tags': {'type': 'list'},
                                                                      'content_type': {'type': 'string'},
                                                                      'size': {'type': 'integer'},
                                                                      'owner': {'type': 'integer'},
                                                                      'ref': {'type': 'string', 'required': True},
                                                                      'ref_id': {'type': 'objectid', 'required': True},
                                                                      'file': {'type': 'media', 'required': True},
                                                                      'acl': {'type': 'dict', 'readonly': True,
                                                                              'schema': {'read': {'type': 'dict'},
                                                                                         'write': {'type': 'dict'},
                                                                                         'execute': {'type': 'dict'}}},
                                                                      '_id': {'type': 'objectid'}},
                                                           'public_methods': [], 'allowed_roles': [],
                                                           'allowed_read_roles': [], 'allowed_write_roles': [],
                                                           'cache_control': 'max-age=20', 'cache_expires': 20,
                                                           'id_field': '_id', 'item_lookup_field': '_id',
                                                           'item_url': 'regex("[a-f0-9]{24}")',
                                                           'resource_title': 'files', 'item_lookup': True,
                                                           'public_item_methods': [], 'allowed_item_roles': [],
                                                           'allowed_item_read_roles': [],
                                                           'allowed_item_write_roles': [], 'allowed_filters': ['*'],
                                                           'sorting': True, 'embedding': True, 'embedded_fields': [],
                                                           'pagination': True, 'projection': True, 'soft_delete': False,
                                                           'bulk_enabled': True, 'internal_resource': False,
                                                           'etag_ignore_fields': None, 'auth_field': None,
                                                           'allow_unknown': False, 'extra_response_fields': [],
                                                           'mongo_write_concern': {'w': 1}, 'hateoas': True,
                                                           'authentication': < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': ['file']}, 'tags': {
                                                                                                                    'item_title': 'tags',
                                                                                                                    'url': 'tags',
                                                                                                                    'datasource': {
                                                                                                                        'source': 'tags',
                                                                                                                        'default_sort': [
                                                                                                                            (
                                                                                                                                'tag',
                                                                                                                                1),
                                                                                                                            (
                                                                                                                                'group',
                                                                                                                                1)],
                                                                                                                        'filter': None,
                                                                                                                        'projection': {
                                                                                                                            'tag': 1,
                                                                                                                            'group': 1,
                                                                                                                            'freq': 1,
                                                                                                                            'related': 1,
                                                                                                                            '_id': 1,
                                                                                                                            '_updated': 1,
                                                                                                                            '_created': 1,
                                                                                                                            '_etag': 1,
                                                                                                                            '_version': 1,
                                                                                                                            '_id_document': 1},
                                                                                                                        'aggregation': None},
                                                                                                                    'extra_response_fields': [
                                                                                                                        'tag'],
                                                                                                                    'resource_methods': [
                                                                                                                        'GET',
                                                                                                                        'POST'],
                                                                                                                    'item_methods': [
                                                                                                                        'GET',
                                                                                                                        'PATCH'],
                                                                                                                    'versioning': True,
                                                                                                                    'additional_lookup': {
                                                                                                                        'url': 'regex("[\\w{1,20}]+")',
                                                                                                                        'field': 'tag'},
                                                                                                                    'mongo_indexes': {
                                                                                                                        'tags group': (
                                                                                                                            [
                                                                                                                                (
                                                                                                                                    'tag',
                                                                                                                                    'text'),
                                                                                                                                (
                                                                                                                                    'group',
                                                                                                                                    'text')],
                                                                                                                            {
                                                                                                                                'background': True})},
                                                                                                                    'schema': {
                                                                                                                        'tag': {
                                                                                                                            'type': 'string',
                                                                                                                            'required': True},
                                                                                                                        'group': {
                                                                                                                            'type': 'string',
                                                                                                                            'required': True},
                                                                                                                        'freq': {
                                                                                                                            'type': 'integer',
                                                                                                                            'required': False,
                                                                                                                            'readonly': True,
                                                                                                                            'default': 0},
                                                                                                                        'related': {
                                                                                                                            'type': 'list',
                                                                                                                            'default': []},
                                                                                                                        '_id': {
                                                                                                                            'type': 'objectid'}},
                                                                                                                    'public_methods': [],
                                                                                                                    'allowed_roles': [],
                                                                                                                    'allowed_read_roles': [],
                                                                                                                    'allowed_write_roles': [],
                                                                                                                    'cache_control': 'max-age=20',
                                                                                                                    'cache_expires': 20,
                                                                                                                    'id_field': '_id',
                                                                                                                    'item_lookup_field': '_id',
                                                                                                                    'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                    'resource_title': 'tags',
                                                                                                                    'item_lookup': True,
                                                                                                                    'public_item_methods': [],
                                                                                                                    'allowed_item_roles': [],
                                                                                                                    'allowed_item_read_roles': [],
                                                                                                                    'allowed_item_write_roles': [],
                                                                                                                    'allowed_filters': [
                                                                                                                        '*'],
                                                                                                                    'sorting': True,
                                                                                                                    'embedding': True,
                                                                                                                    'embedded_fields': [],
                                                                                                                    'pagination': True,
                                                                                                                    'projection': True,
                                                                                                                    'soft_delete': False,
                                                                                                                    'bulk_enabled': True,
                                                                                                                    'internal_resource': False,
                                                                                                                    'etag_ignore_fields': None,
                                                                                                                    'auth_field': None,
                                                                                                                    'allow_unknown': False,
                                                                                                                    'mongo_write_concern': {
                                                                                                                        'w': 1},
                                                                                                                    'hateoas': True,
                                                                                                                    'authentication'
                                                                                                                    : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'dev': {
                                                                                                             'item_title': 'dev',
                                                                                                             'url': 'dev',
                                                                                                             'versioning': False,
                                                                                                             'resource_methods': [
                                                                                                                 'GET',
                                                                                                                 'POST',
                                                                                                                 'DELETE'],
                                                                                                             'item_methods': [
                                                                                                                 'GET',
                                                                                                                 'PATCH',
                                                                                                                 'PUT',
                                                                                                                 'DELETE'],
                                                                                                             'schema': {
                                                                                                                 'app': {
                                                                                                                     'type': 'string',
                                                                                                                     'required': True},
                                                                                                                 'payload': {
                                                                                                                     'type': 'dict',
                                                                                                                     'required': True},
                                                                                                                 '_id': {
                                                                                                                     'type': 'objectid'}},
                                                                                                             'public_methods': [],
                                                                                                             'allowed_roles': [],
                                                                                                             'allowed_read_roles': [],
                                                                                                             'allowed_write_roles': [],
                                                                                                             'cache_control': 'max-age=20',
                                                                                                             'cache_expires': 20,
                                                                                                             'id_field': '_id',
                                                                                                             'item_lookup_field': '_id',
                                                                                                             'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                             'resource_title': 'dev',
                                                                                                             'item_lookup': True,
                                                                                                             'public_item_methods': [],
                                                                                                             'allowed_item_roles': [],
                                                                                                             'allowed_item_read_roles': [],
                                                                                                             'allowed_item_write_roles': [],
                                                                                                             'allowed_filters': [
                                                                                                                 '*'],
                                                                                                             'sorting': True,
                                                                                                             'embedding': True,
                                                                                                             'embedded_fields': [],
                                                                                                             'pagination': True,
                                                                                                             'projection': True,
                                                                                                             'soft_delete': False,
                                                                                                             'bulk_enabled': True,
                                                                                                             'internal_resource': False,
                                                                                                             'etag_ignore_fields': None,
                                                                                                             'auth_field': None,
                                                                                                             'allow_unknown': False,
                                                                                                             'extra_response_fields': [],
                                                                                                             'mongo_write_concern': {
                                                                                                                 'w': 1},
                                                                                                             'mongo_indexes': {},
                                                                                                             'hateoas': True,
                                                                                                             'authentication'
                                                                                                             : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, 'datasource': {'source': 'dev',
                                                                                                  'filter': None,
                                                                                                  'default_sort': None,
                                                                                                  'projection': {
                                                                                                      'app': 1,
                                                                                                      'payload': 1,
                                                                                                      '_id': 1,
                                                                                                      '_updated': 1,
                                                                                                      '_created': 1,
                                                                                                      '_etag': 1},
                                                                                                  'aggregation': None}, '_media': []}, 'help': {
                                                                                                                                                   'item_title': 'help',
                                                                                                                                                   'url': 'help',
                                                                                                                                                   'datasource': {
                                                                                                                                                       'source': 'help',
                                                                                                                                                       'filter': None,
                                                                                                                                                       'default_sort': None,
                                                                                                                                                       'projection': {
                                                                                                                                                           'key': 1,
                                                                                                                                                           'title': 1,
                                                                                                                                                           'body': 1,
                                                                                                                                                           'owner': 1,
                                                                                                                                                           'acl': 1,
                                                                                                                                                           '_id': 1,
                                                                                                                                                           '_updated': 1,
                                                                                                                                                           '_created': 1,
                                                                                                                                                           '_etag': 1,
                                                                                                                                                           '_version': 1,
                                                                                                                                                           '_id_document': 1},
                                                                                                                                                       'aggregation': None},
                                                                                                                                                   'additional_lookup': {
                                                                                                                                                       'url': 'regex("[a-z-]+")',
                                                                                                                                                       'field': 'key'},
                                                                                                                                                   'extra_response_fields': [
                                                                                                                                                       'key'],
                                                                                                                                                   'versioning': True,
                                                                                                                                                   'resource_methods': [
                                                                                                                                                       'GET',
                                                                                                                                                       'POST'],
                                                                                                                                                   'item_methods': [
                                                                                                                                                       'GET',
                                                                                                                                                       'PATCH',
                                                                                                                                                       'DELETE'],
                                                                                                                                                   'mongo_indexes': {
                                                                                                                                                       'key': (
                                                                                                                                                           [
                                                                                                                                                               (
                                                                                                                                                                   'key',
                                                                                                                                                                   1)],
                                                                                                                                                           {
                                                                                                                                                               'background': True}),
                                                                                                                                                       'owner': (
                                                                                                                                                           [
                                                                                                                                                               (
                                                                                                                                                                   'owner',
                                                                                                                                                                   1)],
                                                                                                                                                           {
                                                                                                                                                               'background': True}),
                                                                                                                                                       'acl': (
                                                                                                                                                           [
                                                                                                                                                               (
                                                                                                                                                                   'acl',
                                                                                                                                                                   1)],
                                                                                                                                                           {
                                                                                                                                                               'background': True}),
                                                                                                                                                       'content': (
                                                                                                                                                           [
                                                                                                                                                               (
                                                                                                                                                                   'title',
                                                                                                                                                                   'text'),
                                                                                                                                                               (
                                                                                                                                                                   'body',
                                                                                                                                                                   'text')],
                                                                                                                                                           {
                                                                                                                                                               'background': True})},
                                                                                                                                                   'schema': {
                                                                                                                                                       'key': {
                                                                                                                                                           'type': 'string',
                                                                                                                                                           'required': True,
                                                                                                                                                           'readonly': False,
                                                                                                                                                           'unique': True},
                                                                                                                                                       'title': {
                                                                                                                                                           'type': 'string',
                                                                                                                                                           'required': True},
                                                                                                                                                       'body': {
                                                                                                                                                           'type': 'string'},
                                                                                                                                                       'owner': {
                                                                                                                                                           'type': 'integer'},
                                                                                                                                                       'acl': {
                                                                                                                                                           'type': 'dict',
                                                                                                                                                           'readonly': True,
                                                                                                                                                           'schema': {
                                                                                                                                                               'read': {
                                                                                                                                                                   'type': 'dict'},
                                                                                                                                                               'write': {
                                                                                                                                                                   'type': 'dict'},
                                                                                                                                                               'execute': {
                                                                                                                                                                   'type': 'dict'}}},
                                                                                                                                                       '_id': {
                                                                                                                                                           'type': 'objectid'}},
                                                                                                                                                   'public_methods': [],
                                                                                                                                                   'allowed_roles': [],
                                                                                                                                                   'allowed_read_roles': [],
                                                                                                                                                   'allowed_write_roles': [],
                                                                                                                                                   'cache_control': 'max-age=20',
                                                                                                                                                   'cache_expires': 20,
                                                                                                                                                   'id_field': '_id',
                                                                                                                                                   'item_lookup_field': '_id',
                                                                                                                                                   'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                                                   'resource_title': 'help',
                                                                                                                                                   'item_lookup': True,
                                                                                                                                                   'public_item_methods': [],
                                                                                                                                                   'allowed_item_roles': [],
                                                                                                                                                   'allowed_item_read_roles': [],
                                                                                                                                                   'allowed_item_write_roles': [],
                                                                                                                                                   'allowed_filters': [
                                                                                                                                                       '*'],
                                                                                                                                                   'sorting': True,
                                                                                                                                                   'embedding': True,
                                                                                                                                                   'embedded_fields': [],
                                                                                                                                                   'pagination': True,
                                                                                                                                                   'projection': True,
                                                                                                                                                   'soft_delete': False,
                                                                                                                                                   'bulk_enabled': True,
                                                                                                                                                   'internal_resource': False,
                                                                                                                                                   'etag_ignore_fields': None,
                                                                                                                                                   'auth_field': None,
                                                                                                                                                   'allow_unknown': False,
                                                                                                                                                   'mongo_write_concern': {
                                                                                                                                                       'w': 1},
                                                                                                                                                   'hateoas': True,
                                                                                                                                                   'authentication'
                                                                                                                                                   : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b80b5f8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'users_versions': {
                                                                                                                        'item_title': 'users',
                                                                                                                        'url': 'users',
                                                                                                                        'datasource': {
                                                                                                                            'source': 'users_versions',
                                                                                                                            'default_sort': [
                                                                                                                                (
                                                                                                                                    'id',
                                                                                                                                    1)],
                                                                                                                            'filter': None,
                                                                                                                            'projection': {
                                                                                                                                'id': 1,
                                                                                                                                'avatar': 1,
                                                                                                                                'settings': 1,
                                                                                                                                'custom': 1,
                                                                                                                                'info': 1,
                                                                                                                                'statistics': 1,
                                                                                                                                'acl': 1,
                                                                                                                                '_id': 1,
                                                                                                                                '_updated': 1,
                                                                                                                                '_created': 1,
                                                                                                                                '_etag': 1,
                                                                                                                                '_version': 1,
                                                                                                                                '_id_document': 1},
                                                                                                                            'aggregation': None},
                                                                                                                        'extra_response_fields': [
                                                                                                                            'id'],
                                                                                                                        'resource_methods': [
                                                                                                                            'POST',
                                                                                                                            'GET'],
                                                                                                                        'item_methods': [
                                                                                                                            'GET',
                                                                                                                            'PATCH'],
                                                                                                                        'auth_field': 'id',
                                                                                                                        'versioning': True,
                                                                                                                        'additional_lookup': {
                                                                                                                            'url': 'regex("[\\d{1,6}]+")',
                                                                                                                            'field': 'id'},
                                                                                                                        'mongo_indexes': {
                                                                                                                            'person id': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'id',
                                                                                                                                        1)],
                                                                                                                                {
                                                                                                                                    'background': True}),
                                                                                                                            'acl': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'acl',
                                                                                                                                        1)],
                                                                                                                                {
                                                                                                                                    'background': True})},
                                                                                                                        'schema': {
                                                                                                                            'id': {
                                                                                                                                'type': 'integer',
                                                                                                                                'required': True,
                                                                                                                                'readonly': True},
                                                                                                                            'avatar': {
                                                                                                                                'type': 'media'},
                                                                                                                            'settings': {
                                                                                                                                'type': 'dict',
                                                                                                                                'default': {}},
                                                                                                                            'custom': {
                                                                                                                                'type': 'dict'},
                                                                                                                            'info': {
                                                                                                                                'type': 'dict'},
                                                                                                                            'statistics': {
                                                                                                                                'type': 'dict',
                                                                                                                                'readonly': True},
                                                                                                                            'acl': {
                                                                                                                                'type': 'dict',
                                                                                                                                'readonly': True,
                                                                                                                                'schema': {
                                                                                                                                    'groups': {
                                                                                                                                        'type': 'list',
                                                                                                                                        'default': [],
                                                                                                                                        'schema': {
                                                                                                                                            'type': 'objectid'}},
                                                                                                                                    'roles': {
                                                                                                                                        'type': 'list',
                                                                                                                                        'default': [],
                                                                                                                                        'schema': {
                                                                                                                                            'type': 'objectid'}}},
                                                                                                                                'default': {
                                                                                                                                    'groups': [],
                                                                                                                                    'roles': []}},
                                                                                                                            '_id': {
                                                                                                                                'type': 'objectid'}},
                                                                                                                        'public_methods': [],
                                                                                                                        'allowed_roles': [],
                                                                                                                        'allowed_read_roles': [],
                                                                                                                        'allowed_write_roles': [],
                                                                                                                        'cache_control': 'max-age=20',
                                                                                                                        'cache_expires': 20,
                                                                                                                        'id_field': '_id',
                                                                                                                        'item_lookup_field': '_id',
                                                                                                                        'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                        'resource_title': 'users',
                                                                                                                        'item_lookup': True,
                                                                                                                        'public_item_methods': [],
                                                                                                                        'allowed_item_roles': [],
                                                                                                                        'allowed_item_read_roles': [],
                                                                                                                        'allowed_item_write_roles': [],
                                                                                                                        'allowed_filters': [
                                                                                                                            '*'],
                                                                                                                        'sorting': True,
                                                                                                                        'embedding': True,
                                                                                                                        'embedded_fields': [],
                                                                                                                        'pagination': True,
                                                                                                                        'projection': True,
                                                                                                                        'soft_delete': False,
                                                                                                                        'bulk_enabled': True,
                                                                                                                        'internal_resource': False,
                                                                                                                        'etag_ignore_fields': None,
                                                                                                                        'allow_unknown': False,
                                                                                                                        'mongo_write_concern': {
                                                                                                                            'w': 1},
                                                                                                                        'hateoas': True,
                                                                                                                        'authentication'
                                                                                                                        : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6b7e51d0 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': [
    'avatar']}, 'f_ors_versions': {'item_title': 'Fallskjerm Observations', 'url': 'f/observations',
                                   'datasource': {'source': 'f_observations_versions',
                                                  'projection': {'acl': 0, 'id': 1, 'type': 1, 'flags': 1, 'ask': 1,
                                                                 'tags': 1, 'club': 1, 'location': 1, 'owner': 1,
                                                                 'reporter': 1, 'when': 1, 'involved': 1,
                                                                 'organization': 1, 'rating': 1, 'weather': 1,
                                                                 'components': 1, 'files': 1, 'related': 1,
                                                                 'actions': 1, 'comments': 1, 'workflow': 1,
                                                                 'watchers': 1, 'audit': 1, '_id': 1, '_updated': 1,
                                                                 '_created': 1, '_etag': 1, '_version': 1,
                                                                 '_id_document': 1}, 'filter': None,
                                                  'default_sort': None, 'aggregation': None},
                                   'additional_lookup': {'url': 'regex("[\\d{1,9}]+")', 'field': 'id'},
                                   'extra_response_fields': ['id'], 'versioning': True,
                                   'resource_methods': ['GET', 'POST'], 'item_methods': ['GET', 'PATCH', 'PUT'],
                                   'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                                                     'persons': ([('owner', 1), ('reporter', 1)], {'background': True}),
                                                     'when': ([('when', 1)], {'background': True}),
                                                     'type': ([('type', 1)], {'background': True}),
                                                     'rating': ([('rating', 1)], {'background': True}),
                                                     'title': ([('tags', 'text')], {'background': True})},
                                   'schema': {'id': {'type': 'integer', 'required': False, 'readonly': True},
                                              'type': {'type': 'string',
                                                       'allowed': ['sharing', 'unsafe_act', 'near_miss', 'incident',
                                                                   'accident']}, 'flags': {'type': 'dict', 'schema': {
                                           'aviation': {'type': 'boolean', 'default': False},
                                           'insurance': {'type': 'boolean', 'default': False}}}, 'ask': {'type': 'dict',
                                                                                                         'schema': {
                                                                                                             'attitude': {
                                                                                                                 'type': 'integer',
                                                                                                                 'default': 0},
                                                                                                             'skills': {
                                                                                                                 'type': 'integer',
                                                                                                                 'default': 0},
                                                                                                             'knowledge': {
                                                                                                                 'type': 'integer',
                                                                                                                 'default': 0},
                                                                                                             'text': {
                                                                                                                 'type': 'dict',
                                                                                                                 'default': {}}}},
                                              'tags': {'type': 'list', 'default': []},
                                              'club': {'type': 'string', 'required': True},
                                              'location': {'type': 'dict', 'default': {}},
                                              'owner': {'type': 'integer', 'readonly': True},
                                              'reporter': {'type': 'integer', 'readonly': True},
                                              'when': {'type': 'datetime',
                                                       'default': datetime.datetime(2019, 1, 6, 14, 11, 28, 728999)},
                                              'involved': {'type': 'list', 'default': []},
                                              'organization': {'type': 'dict', 'default': {}},
                                              'rating': {'type': 'dict',
                                                         'schema': {'actual': {'type': 'integer', 'default': 1},
                                                                    'potential': {'type': 'integer', 'default': 1}}},
                                              'weather': {'type': 'dict', 'schema': {'auto': {'type': 'dict'},
                                                                                     'manual': {'type': 'dict'}}},
                                              'components': {'type': 'list', 'default': []}, 'files': {'type': 'list',
                                                                                                       'schema': {
                                                                                                           'type': 'dict',
                                                                                                           'schema': {
                                                                                                               'f': {
                                                                                                                   'type': 'string'},
                                                                                                               'r': {
                                                                                                                   'type': 'boolean'}}},
                                                                                                       'default': []},
                                              'related': {'type': 'list', 'default': []}, 'actions': {'type': 'dict'},
                                              'comments': {'type': 'list', 'default': [], 'readonly': True,
                                                           'schema': {'type': 'dict',
                                                                      'schema': {'date': {'type': 'datetime'},
                                                                                 'user': {'type': 'integer'},
                                                                                 'comment': {'type': 'string'}}}},
                                              'workflow': {'type': 'dict', 'readonly': True, 'default': {}},
                                              'watchers': {'type': 'list', 'default': [], 'readonly': True},
                                              'audit': {'type': 'list', 'readonly': True, 'default': []},
                                              'acl': {'type': 'dict', 'readonly': True,
                                                      'schema': {'read': {'type': 'dict'}, 'write': {'type': 'dict'},
                                                                 'execute': {'type': 'dict'}}},
                                              '_id': {'type': 'objectid'}}, 'public_methods': [], 'allowed_roles': [],
                                   'allowed_read_roles': [], 'allowed_write_roles': [], 'cache_control': 'max-age=20',
                                   'cache_expires': 20, 'id_field': '_id', 'item_lookup_field': '_id',
                                   'item_url': 'regex("[a-f0-9]{24}")', 'resource_title': 'f/observations',
                                   'item_lookup': True, 'public_item_methods': [], 'allowed_item_roles': [],
                                   'allowed_item_read_roles': [], 'allowed_item_write_roles': [],
                                   'allowed_filters': ['*'], 'sorting': True, 'embedding': True, 'embedded_fields': [],
                                   'pagination': True, 'projection': True, 'soft_delete': False, 'bulk_enabled': True,
                                   'internal_resource': False, 'etag_ignore_fields': None, 'auth_field': None,
                                   'allow_unknown': False, 'mongo_write_concern': {'w': 1}, 'hateoas': True,
                                   'authentication': < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6a5891d0 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'legacy_licenses_versions': {
                                                                                                                                  'item_title': 'licenses',
                                                                                                                                  'description': 'Licenses with added snacks',
                                                                                                                                  'url': 'legacy/licenses',
                                                                                                                                  'datasource': {
                                                                                                                                      'source': 'legacy_licenses_versions',
                                                                                                                                      'default_sort': [
                                                                                                                                          (
                                                                                                                                              'id',
                                                                                                                                              1)],
                                                                                                                                      'filter': None,
                                                                                                                                      'projection': {
                                                                                                                                          'id': 1,
                                                                                                                                          'name': 1,
                                                                                                                                          'active': 1,
                                                                                                                                          'url': 1,
                                                                                                                                          '_id': 1,
                                                                                                                                          '_updated': 1,
                                                                                                                                          '_created': 1,
                                                                                                                                          '_etag': 1,
                                                                                                                                          '_version': 1,
                                                                                                                                          '_id_document': 1},
                                                                                                                                      'aggregation': None},
                                                                                                                                  'extra_response_fields': [
                                                                                                                                      'id'],
                                                                                                                                  'resource_methods': [
                                                                                                                                      'GET',
                                                                                                                                      'POST'],
                                                                                                                                  'item_methods': [
                                                                                                                                      'GET',
                                                                                                                                      'PATCH',
                                                                                                                                      'PUT'],
                                                                                                                                  'versioning': True,
                                                                                                                                  'additional_lookup': {
                                                                                                                                      'url': 'regex("[\\w{1}\\-\\w{1,5}]+")',
                                                                                                                                      'field': 'id'},
                                                                                                                                  'mongo_indexes': {
                                                                                                                                      'id': (
                                                                                                                                          [
                                                                                                                                              (
                                                                                                                                                  'id',
                                                                                                                                                  1)],
                                                                                                                                          {
                                                                                                                                              'background': True}),
                                                                                                                                      'name': (
                                                                                                                                          [
                                                                                                                                              (
                                                                                                                                                  'name',
                                                                                                                                                  1)],
                                                                                                                                          {
                                                                                                                                              'background': True})},
                                                                                                                                  'schema': {
                                                                                                                                      'id': {
                                                                                                                                          'type': 'string',
                                                                                                                                          'required': True,
                                                                                                                                          'readonly': True},
                                                                                                                                      'name': {
                                                                                                                                          'type': 'string'},
                                                                                                                                      'active': {
                                                                                                                                          'type': 'boolean'},
                                                                                                                                      'url': {
                                                                                                                                          'type': 'string',
                                                                                                                                          'required': False},
                                                                                                                                      '_id': {
                                                                                                                                          'type': 'objectid'}},
                                                                                                                                  'public_methods': [],
                                                                                                                                  'allowed_roles': [],
                                                                                                                                  'allowed_read_roles': [],
                                                                                                                                  'allowed_write_roles': [],
                                                                                                                                  'cache_control': 'max-age=20',
                                                                                                                                  'cache_expires': 20,
                                                                                                                                  'id_field': '_id',
                                                                                                                                  'item_lookup_field': '_id',
                                                                                                                                  'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                                  'resource_title': 'legacy/licenses',
                                                                                                                                  'item_lookup': True,
                                                                                                                                  'public_item_methods': [],
                                                                                                                                  'allowed_item_roles': [],
                                                                                                                                  'allowed_item_read_roles': [],
                                                                                                                                  'allowed_item_write_roles': [],
                                                                                                                                  'allowed_filters': [
                                                                                                                                      '*'],
                                                                                                                                  'sorting': True,
                                                                                                                                  'embedding': True,
                                                                                                                                  'embedded_fields': [],
                                                                                                                                  'pagination': True,
                                                                                                                                  'projection': True,
                                                                                                                                  'soft_delete': False,
                                                                                                                                  'bulk_enabled': True,
                                                                                                                                  'internal_resource': False,
                                                                                                                                  'etag_ignore_fields': None,
                                                                                                                                  'auth_field': None,
                                                                                                                                  'allow_unknown': False,
                                                                                                                                  'mongo_write_concern': {
                                                                                                                                      'w': 1},
                                                                                                                                  'hateoas': True,
                                                                                                                                  'authentication'
                                                                                                                                  : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6a589a90 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'legacy_clubs_versions': {
                                                                                                                               'item_title': 'club',
                                                                                                                               'description': 'Legacy clubs with added data',
                                                                                                                               'url': 'legacy/clubs',
                                                                                                                               'datasource': {
                                                                                                                                   'source': 'legacy_clubs_versions',
                                                                                                                                   'default_sort': [
                                                                                                                                       (
                                                                                                                                           'id',
                                                                                                                                           1)],
                                                                                                                                   'filter': None,
                                                                                                                                   'projection': {
                                                                                                                                       'id': 1,
                                                                                                                                       'name': 1,
                                                                                                                                       'active': 1,
                                                                                                                                       'org': 1,
                                                                                                                                       'locations': 1,
                                                                                                                                       'planes': 1,
                                                                                                                                       'roles': 1,
                                                                                                                                       'ot': 1,
                                                                                                                                       'ci': 1,
                                                                                                                                       'logo': 1,
                                                                                                                                       'url': 1,
                                                                                                                                       '_id': 1,
                                                                                                                                       '_updated': 1,
                                                                                                                                       '_created': 1,
                                                                                                                                       '_etag': 1,
                                                                                                                                       '_version': 1,
                                                                                                                                       '_id_document': 1},
                                                                                                                                   'aggregation': None},
                                                                                                                               'extra_response_fields': [
                                                                                                                                   'id'],
                                                                                                                               'resource_methods': [
                                                                                                                                   'GET',
                                                                                                                                   'POST'],
                                                                                                                               'item_methods': [
                                                                                                                                   'GET',
                                                                                                                                   'PATCH',
                                                                                                                                   'PUT'],
                                                                                                                               'versioning': True,
                                                                                                                               'additional_lookup': {
                                                                                                                                   'url': 'regex("[\\d{3}\\-\\w{1}]+")',
                                                                                                                                   'field': 'id'},
                                                                                                                               'mongo_indexes': {
                                                                                                                                   'id': (
                                                                                                                                       [
                                                                                                                                           (
                                                                                                                                               'id',
                                                                                                                                               1)],
                                                                                                                                       {
                                                                                                                                           'background': True}),
                                                                                                                                   'name': (
                                                                                                                                       [
                                                                                                                                           (
                                                                                                                                               'name',
                                                                                                                                               1)],
                                                                                                                                       {
                                                                                                                                           'background': True})},
                                                                                                                               'schema': {
                                                                                                                                   'id': {
                                                                                                                                       'type': 'string',
                                                                                                                                       'required': True,
                                                                                                                                       'readonly': True},
                                                                                                                                   'name': {
                                                                                                                                       'type': 'string'},
                                                                                                                                   'active': {
                                                                                                                                       'type': 'boolean'},
                                                                                                                                   'org': {
                                                                                                                                       'type': 'string'},
                                                                                                                                   'locations': {
                                                                                                                                       'type': 'list'},
                                                                                                                                   'planes': {
                                                                                                                                       'type': 'dict'},
                                                                                                                                   'roles': {
                                                                                                                                       'type': 'dict'},
                                                                                                                                   'ot': {
                                                                                                                                       'type': 'integer',
                                                                                                                                       'required': True,
                                                                                                                                       'allowed': [
                                                                                                                                           1,
                                                                                                                                           2]},
                                                                                                                                   'ci': {
                                                                                                                                       'type': 'integer',
                                                                                                                                       'required': False},
                                                                                                                                   'logo': {
                                                                                                                                       'type': 'media',
                                                                                                                                       'required': False},
                                                                                                                                   'url': {
                                                                                                                                       'type': 'string',
                                                                                                                                       'required': False},
                                                                                                                                   '_id': {
                                                                                                                                       'type': 'objectid'}},
                                                                                                                               'public_methods': [],
                                                                                                                               'allowed_roles': [],
                                                                                                                               'allowed_read_roles': [],
                                                                                                                               'allowed_write_roles': [],
                                                                                                                               'cache_control': 'max-age=20',
                                                                                                                               'cache_expires': 20,
                                                                                                                               'id_field': '_id',
                                                                                                                               'item_lookup_field': '_id',
                                                                                                                               'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                               'resource_title': 'legacy/clubs',
                                                                                                                               'item_lookup': True,
                                                                                                                               'public_item_methods': [],
                                                                                                                               'allowed_item_roles': [],
                                                                                                                               'allowed_item_read_roles': [],
                                                                                                                               'allowed_item_write_roles': [],
                                                                                                                               'allowed_filters': [
                                                                                                                                   '*'],
                                                                                                                               'sorting': True,
                                                                                                                               'embedding': True,
                                                                                                                               'embedded_fields': [],
                                                                                                                               'pagination': True,
                                                                                                                               'projection': True,
                                                                                                                               'soft_delete': False,
                                                                                                                               'bulk_enabled': True,
                                                                                                                               'internal_resource': False,
                                                                                                                               'etag_ignore_fields': None,
                                                                                                                               'auth_field': None,
                                                                                                                               'allow_unknown': False,
                                                                                                                               'mongo_write_concern': {
                                                                                                                                   'w': 1},
                                                                                                                               'hateoas': True,
                                                                                                                               'authentication'
                                                                                                                               : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6a5994e0 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': [
    'logo']}, 'content_versions': {'item_title': 'content', 'url': 'content',
                                   'datasource': {'source': 'content_versions', 'filter': None, 'default_sort': None,
                                                  'projection': {'title': 1, 'slug': 1, 'body': 1, 'space_key': 1,
                                                                 'parent': 1, 'order': 1, 'ref': 1, 'owner': 1,
                                                                 '_id': 1, '_updated': 1, '_created': 1, '_etag': 1,
                                                                 '_version': 1, '_id_document': 1},
                                                  'aggregation': None},
                                   'additional_lookup': {'url': 'regex("[a-z0-9-]+")', 'field': 'slug'},
                                   'extra_response_fields': ['key'], 'versioning': True,
                                   'resource_methods': ['GET', 'POST'], 'item_methods': ['GET', 'PATCH', 'DELETE'],
                                   'mongo_indexes': {'slug': ([('slug', 1)], {'background': True}),
                                                     'space': ([('space_key', 1)], {'background': True}),
                                                     'parent': ([('parent', 1)], {'background': True}),
                                                     'owner': ([('owner', 1)], {'background': True}), 'content': (
                                           [('title', 'text'), ('body', 'text')], {'background': True})},
                                   'schema': {'title': {'type': 'string', 'required': True, 'readonly': False},
                                              'slug': {'type': 'string', 'required': True},
                                              'body': {'type': 'string', 'required': True},
                                              'space_key': {'type': 'string', 'required': True},
                                              'parent': {'type': 'objectid', 'default': None},
                                              'order': {'type': 'integer'}, 'ref': {'type': 'string'},
                                              'owner': {'type': 'integer', 'required': False, 'readonly': True},
                                              '_id': {'type': 'objectid'}}, 'public_methods': [], 'allowed_roles': [],
                                   'allowed_read_roles': [], 'allowed_write_roles': [], 'cache_control': 'max-age=20',
                                   'cache_expires': 20, 'id_field': '_id', 'item_lookup_field': '_id',
                                   'item_url': 'regex("[a-f0-9]{24}")', 'resource_title': 'content',
                                   'item_lookup': True, 'public_item_methods': [], 'allowed_item_roles': [],
                                   'allowed_item_read_roles': [], 'allowed_item_write_roles': [],
                                   'allowed_filters': ['*'], 'sorting': True, 'embedding': True, 'embedded_fields': [],
                                   'pagination': True, 'projection': True, 'soft_delete': False, 'bulk_enabled': True,
                                   'internal_resource': False, 'etag_ignore_fields': None, 'auth_field': None,
                                   'allow_unknown': False, 'mongo_write_concern': {'w': 1}, 'hateoas': True,
                                   'authentication': < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6a5a5c50 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'files_versions': {
                                                                                                                        'item_title': 'Files',
                                                                                                                        'description': 'Universal file storage and retrieval',
                                                                                                                        'url': 'files',
                                                                                                                        'datasource': {
                                                                                                                            'source': 'files_versions',
                                                                                                                            'filter': None,
                                                                                                                            'default_sort': None,
                                                                                                                            'projection': {
                                                                                                                                'name': 1,
                                                                                                                                'description': 1,
                                                                                                                                'tags': 1,
                                                                                                                                'content_type': 1,
                                                                                                                                'size': 1,
                                                                                                                                'owner': 1,
                                                                                                                                'ref': 1,
                                                                                                                                'ref_id': 1,
                                                                                                                                'file': 1,
                                                                                                                                'acl': 1,
                                                                                                                                '_id': 1,
                                                                                                                                '_updated': 1,
                                                                                                                                '_created': 1,
                                                                                                                                '_etag': 1,
                                                                                                                                '_version': 1,
                                                                                                                                '_id_document': 1},
                                                                                                                            'aggregation': None},
                                                                                                                        'resource_methods': [
                                                                                                                            'GET',
                                                                                                                            'POST'],
                                                                                                                        'item_methods': [
                                                                                                                            'GET',
                                                                                                                            'PATCH'],
                                                                                                                        'versioning': True,
                                                                                                                        'mongo_indexes': {
                                                                                                                            'name': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'slug',
                                                                                                                                        1)],
                                                                                                                                {
                                                                                                                                    'background': True}),
                                                                                                                            'tags': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'tags',
                                                                                                                                        1)],
                                                                                                                                {
                                                                                                                                    'background': True}),
                                                                                                                            'content': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'content_type',
                                                                                                                                        1)],
                                                                                                                                {
                                                                                                                                    'background': True}),
                                                                                                                            'ref': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'ref',
                                                                                                                                        1),
                                                                                                                                    (
                                                                                                                                        'ref_id',
                                                                                                                                        1)],
                                                                                                                                {
                                                                                                                                    'background': True}),
                                                                                                                            'owner': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'owner',
                                                                                                                                        1)],
                                                                                                                                {
                                                                                                                                    'background': True}),
                                                                                                                            'acl': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'acl',
                                                                                                                                        1)],
                                                                                                                                {
                                                                                                                                    'background': True}),
                                                                                                                            'descr': (
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        'description',
                                                                                                                                        'text'),
                                                                                                                                    (
                                                                                                                                        'name',
                                                                                                                                        'text')],
                                                                                                                                {
                                                                                                                                    'background': True})},
                                                                                                                        'schema': {
                                                                                                                            'name': {
                                                                                                                                'type': 'string'},
                                                                                                                            'description': {
                                                                                                                                'type': 'string'},
                                                                                                                            'tags': {
                                                                                                                                'type': 'list'},
                                                                                                                            'content_type': {
                                                                                                                                'type': 'string'},
                                                                                                                            'size': {
                                                                                                                                'type': 'integer'},
                                                                                                                            'owner': {
                                                                                                                                'type': 'integer'},
                                                                                                                            'ref': {
                                                                                                                                'type': 'string',
                                                                                                                                'required': True},
                                                                                                                            'ref_id': {
                                                                                                                                'type': 'objectid',
                                                                                                                                'required': True},
                                                                                                                            'file': {
                                                                                                                                'type': 'media',
                                                                                                                                'required': True},
                                                                                                                            'acl': {
                                                                                                                                'type': 'dict',
                                                                                                                                'readonly': True,
                                                                                                                                'schema': {
                                                                                                                                    'read': {
                                                                                                                                        'type': 'dict'},
                                                                                                                                    'write': {
                                                                                                                                        'type': 'dict'},
                                                                                                                                    'execute': {
                                                                                                                                        'type': 'dict'}}},
                                                                                                                            '_id': {
                                                                                                                                'type': 'objectid'}},
                                                                                                                        'public_methods': [],
                                                                                                                        'allowed_roles': [],
                                                                                                                        'allowed_read_roles': [],
                                                                                                                        'allowed_write_roles': [],
                                                                                                                        'cache_control': 'max-age=20',
                                                                                                                        'cache_expires': 20,
                                                                                                                        'id_field': '_id',
                                                                                                                        'item_lookup_field': '_id',
                                                                                                                        'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                        'resource_title': 'files',
                                                                                                                        'item_lookup': True,
                                                                                                                        'public_item_methods': [],
                                                                                                                        'allowed_item_roles': [],
                                                                                                                        'allowed_item_read_roles': [],
                                                                                                                        'allowed_item_write_roles': [],
                                                                                                                        'allowed_filters': [
                                                                                                                            '*'],
                                                                                                                        'sorting': True,
                                                                                                                        'embedding': True,
                                                                                                                        'embedded_fields': [],
                                                                                                                        'pagination': True,
                                                                                                                        'projection': True,
                                                                                                                        'soft_delete': False,
                                                                                                                        'bulk_enabled': True,
                                                                                                                        'internal_resource': False,
                                                                                                                        'etag_ignore_fields': None,
                                                                                                                        'auth_field': None,
                                                                                                                        'allow_unknown': False,
                                                                                                                        'extra_response_fields': [],
                                                                                                                        'mongo_write_concern': {
                                                                                                                            'w': 1},
                                                                                                                        'hateoas': True,
                                                                                                                        'authentication'
                                                                                                                        : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6a5b1898 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': [
    'file']}, 'tags_versions': {'item_title': 'tags', 'url': 'tags',
                                'datasource': {'source': 'tags_versions', 'default_sort': [('tag', 1), ('group', 1)],
                                               'filter': None,
                                               'projection': {'tag': 1, 'group': 1, 'freq': 1, 'related': 1, '_id': 1,
                                                              '_updated': 1, '_created': 1, '_etag': 1, '_version': 1,
                                                              '_id_document': 1}, 'aggregation': None},
                                'extra_response_fields': ['tag'], 'resource_methods': ['GET', 'POST'],
                                'item_methods': ['GET', 'PATCH'], 'versioning': True,
                                'additional_lookup': {'url': 'regex("[\\w{1,20}]+")', 'field': 'tag'},
                                'mongo_indexes': {
                                    'tags group': ([('tag', 'text'), ('group', 'text')], {'background': True})},
                                'schema': {'tag': {'type': 'string', 'required': True},
                                           'group': {'type': 'string', 'required': True},
                                           'freq': {'type': 'integer', 'required': False, 'readonly': True,
                                                    'default': 0}, 'related': {'type': 'list', 'default': []},
                                           '_id': {'type': 'objectid'}}, 'public_methods': [], 'allowed_roles': [],
                                'allowed_read_roles': [], 'allowed_write_roles': [], 'cache_control': 'max-age=20',
                                'cache_expires': 20, 'id_field': '_id', 'item_lookup_field': '_id',
                                'item_url': 'regex("[a-f0-9]{24}")', 'resource_title': 'tags', 'item_lookup': True,
                                'public_item_methods': [], 'allowed_item_roles': [], 'allowed_item_read_roles': [],
                                'allowed_item_write_roles': [], 'allowed_filters': ['*'], 'sorting': True,
                                'embedding': True, 'embedded_fields': [], 'pagination': True, 'projection': True,
                                'soft_delete': False, 'bulk_enabled': True, 'internal_resource': False,
                                'etag_ignore_fields': None, 'auth_field': None, 'allow_unknown': False,
                                'mongo_write_concern': {'w': 1}, 'hateoas': True, 'authentication'
                                : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6a53f0b8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}, 'help_versions': {
                                                                                                                       'item_title': 'help',
                                                                                                                       'url': 'help',
                                                                                                                       'datasource': {
                                                                                                                           'source': 'help_versions',
                                                                                                                           'filter': None,
                                                                                                                           'default_sort': None,
                                                                                                                           'projection': {
                                                                                                                               'key': 1,
                                                                                                                               'title': 1,
                                                                                                                               'body': 1,
                                                                                                                               'owner': 1,
                                                                                                                               'acl': 1,
                                                                                                                               '_id': 1,
                                                                                                                               '_updated': 1,
                                                                                                                               '_created': 1,
                                                                                                                               '_etag': 1,
                                                                                                                               '_version': 1,
                                                                                                                               '_id_document': 1},
                                                                                                                           'aggregation': None},
                                                                                                                       'additional_lookup': {
                                                                                                                           'url': 'regex("[a-z-]+")',
                                                                                                                           'field': 'key'},
                                                                                                                       'extra_response_fields': [
                                                                                                                           'key'],
                                                                                                                       'versioning': True,
                                                                                                                       'resource_methods': [
                                                                                                                           'GET',
                                                                                                                           'POST'],
                                                                                                                       'item_methods': [
                                                                                                                           'GET',
                                                                                                                           'PATCH',
                                                                                                                           'DELETE'],
                                                                                                                       'mongo_indexes': {
                                                                                                                           'key': (
                                                                                                                               [
                                                                                                                                   (
                                                                                                                                       'key',
                                                                                                                                       1)],
                                                                                                                               {
                                                                                                                                   'background': True}),
                                                                                                                           'owner': (
                                                                                                                               [
                                                                                                                                   (
                                                                                                                                       'owner',
                                                                                                                                       1)],
                                                                                                                               {
                                                                                                                                   'background': True}),
                                                                                                                           'acl': (
                                                                                                                               [
                                                                                                                                   (
                                                                                                                                       'acl',
                                                                                                                                       1)],
                                                                                                                               {
                                                                                                                                   'background': True}),
                                                                                                                           'content': (
                                                                                                                               [
                                                                                                                                   (
                                                                                                                                       'title',
                                                                                                                                       'text'),
                                                                                                                                   (
                                                                                                                                       'body',
                                                                                                                                       'text')],
                                                                                                                               {
                                                                                                                                   'background': True})},
                                                                                                                       'schema': {
                                                                                                                           'key': {
                                                                                                                               'type': 'string',
                                                                                                                               'required': True,
                                                                                                                               'readonly': False,
                                                                                                                               'unique': True},
                                                                                                                           'title': {
                                                                                                                               'type': 'string',
                                                                                                                               'required': True},
                                                                                                                           'body': {
                                                                                                                               'type': 'string'},
                                                                                                                           'owner': {
                                                                                                                               'type': 'integer'},
                                                                                                                           'acl': {
                                                                                                                               'type': 'dict',
                                                                                                                               'readonly': True,
                                                                                                                               'schema': {
                                                                                                                                   'read': {
                                                                                                                                       'type': 'dict'},
                                                                                                                                   'write': {
                                                                                                                                       'type': 'dict'},
                                                                                                                                   'execute': {
                                                                                                                                       'type': 'dict'}}},
                                                                                                                           '_id': {
                                                                                                                               'type': 'objectid'}},
                                                                                                                       'public_methods': [],
                                                                                                                       'allowed_roles': [],
                                                                                                                       'allowed_read_roles': [],
                                                                                                                       'allowed_write_roles': [],
                                                                                                                       'cache_control': 'max-age=20',
                                                                                                                       'cache_expires': 20,
                                                                                                                       'id_field': '_id',
                                                                                                                       'item_lookup_field': '_id',
                                                                                                                       'item_url': 'regex("[a-f0-9]{24}")',
                                                                                                                       'resource_title': 'help',
                                                                                                                       'item_lookup': True,
                                                                                                                       'public_item_methods': [],
                                                                                                                       'allowed_item_roles': [],
                                                                                                                       'allowed_item_read_roles': [],
                                                                                                                       'allowed_item_write_roles': [],
                                                                                                                       'allowed_filters': [
                                                                                                                           '*'],
                                                                                                                       'sorting': True,
                                                                                                                       'embedding': True,
                                                                                                                       'embedded_fields': [],
                                                                                                                       'pagination': True,
                                                                                                                       'projection': True,
                                                                                                                       'soft_delete': False,
                                                                                                                       'bulk_enabled': True,
                                                                                                                       'internal_resource': False,
                                                                                                                       'etag_ignore_fields': None,
                                                                                                                       'auth_field': None,
                                                                                                                       'allow_unknown': False,
                                                                                                                       'mongo_write_concern': {
                                                                                                                           'w': 1},
                                                                                                                       'hateoas': True,
                                                                                                                       'authentication'
                                                                                                                       : < ext.auth.tokenauth.TokenAuth
object
at
0x7fdc6a53fdd8 >, 'merge_nested_documents': True, 'normalize_dotted_fields': True, '_media': []}}, 'MONGO_CONNECT_TIMEOUT_MS': 200, 'MONGO_DBNAME': 'nlf-dev', 'MONGO_HOST': 'localhost', 'MONGO_PASSWORD': '', 'MONGO_PORT': 27017, 'MONGO_USERNAME': '', 'SWAGGER_INFO': {
    'title': 'NLF API', 'version': '0.1.0', 'description': 'RESTful API for the NLF application framework',
    'termsOfService': 'See www.nlf.no',
    'contact': {'name': 'Norges Luftsportforbund', 'email': 'post@nlf.no', 'url': 'http://www.nlf.no'},
    'license': {'name': 'GPLV1', 'url': 'https://github.com/FNLF/nlf-backend/'}}, 'MONGO_CONNECT': True, 'URLS': {
    'users': 'users', 'users_versions': 'users', 'users_acl': 'users/acl', 'acl_groups': 'acl/groups',
    'acl_roles': 'acl/roles', 'f_ors': 'f/observations', 'f_ors_versions': 'f/observations',
    'f_ors_agg': 'f/observations/aggregate', 'legacy_licenses': 'legacy/licenses',
    'legacy_licenses_versions': 'legacy/licenses', 'legacy_clubs': 'legacy/clubs',
    'legacy_clubs_versions': 'legacy/clubs', 'legacy_melwin_licenses': 'legacy/melwin/licenses',
    'legacy_melwin_membership': 'legacy/melwin/membership', 'legacy_melwin_clubs': 'legacy/melwin/clubs',
    'legacy_melwin_users': 'legacy/melwin/users', 'content': 'content', 'content_versions': 'content',
    'content_aggregate_parents': 'content/aggregate/parents',
    'content_aggregate_children': 'content/aggregate/children',
    'content_aggregate_siblings': 'content/aggregate/siblings', 'files': 'files', 'files_versions': 'files',
    'tags': 'tags', 'tags_versions': 'tags', 'dev': 'dev', 'help': 'help', 'help_versions': 'help'}, 'SOURCES': {
    'users': {'source': 'users', 'default_sort': [('id', 1)], 'filter': None,
              'projection': {'id': 1, 'avatar': 1, 'settings': 1, 'custom': 1, 'info': 1, 'statistics': 1, 'acl': 1,
                             '_id': 1, '_updated': 1, '_created': 1, '_etag': 1, '_version': 1, '_id_document': 1},
              'aggregation': None},
    'users_versions': {'source': 'users_versions', 'default_sort': [('id', 1)], 'filter': None,
                       'projection': {'id': 1, 'avatar': 1, 'settings': 1, 'custom': 1, 'info': 1, 'statistics': 1,
                                      'acl': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1, '_version': 1,
                                      '_id_document': 1}, 'aggregation': None},
    'users_acl': {'source': 'users', 'default_sort': [('id', 1)], 'filter': None,
                  'projection': {'id': 1, 'acl': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1},
                  'aggregation': None},
    'users_auth': {'source': 'users_auth', 'default_sort': [('id', 1)], 'filter': None,
                   'projection': {'id': 1, 'acl': 1, 'auth': 1, 'user': 1, '_id': 1, '_updated': 1, '_created': 1,
                                  '_etag': 1}, 'aggregation': None},
    'acl_groups': {'source': 'acl_groups', 'filter': None, 'default_sort': None,
                   'projection': {'name': 1, 'description': 1, 'ref': 1, '_id': 1, '_updated': 1, '_created': 1,
                                  '_etag': 1}, 'aggregation': None},
    'acl_roles': {'source': 'acl_roles', 'filter': None, 'default_sort': None,
                  'projection': {'name': 1, 'description': 1, 'ref': 1, 'group': 1, '_id': 1, '_updated': 1,
                                 '_created': 1, '_etag': 1}, 'aggregation': None}, 'f_ors': {'source': 'f_observations',
                                                                                             'projection': {'acl': 0,
                                                                                                            'id': 1,
                                                                                                            'type': 1,
                                                                                                            'flags': 1,
                                                                                                            'ask': 1,
                                                                                                            'tags': 1,
                                                                                                            'club': 1,
                                                                                                            'location': 1,
                                                                                                            'owner': 1,
                                                                                                            'reporter': 1,
                                                                                                            'when': 1,
                                                                                                            'involved': 1,
                                                                                                            'organization': 1,
                                                                                                            'rating': 1,
                                                                                                            'weather': 1,
                                                                                                            'components': 1,
                                                                                                            'files': 1,
                                                                                                            'related': 1,
                                                                                                            'actions': 1,
                                                                                                            'comments': 1,
                                                                                                            'workflow': 1,
                                                                                                            'watchers': 1,
                                                                                                            'audit': 1,
                                                                                                            '_id': 1,
                                                                                                            '_updated': 1,
                                                                                                            '_created': 1,
                                                                                                            '_etag': 1,
                                                                                                            '_version': 1,
                                                                                                            '_id_document': 1},
                                                                                             'filter': None,
                                                                                             'default_sort': None,
                                                                                             'aggregation': None},
    'f_ors_versions': {'source': 'f_observations_versions',
                       'projection': {'acl': 0, 'id': 1, 'type': 1, 'flags': 1, 'ask': 1, 'tags': 1, 'club': 1,
                                      'location': 1, 'owner': 1, 'reporter': 1, 'when': 1, 'involved': 1,
                                      'organization': 1, 'rating': 1, 'weather': 1, 'components': 1, 'files': 1,
                                      'related': 1, 'actions': 1, 'comments': 1, 'workflow': 1, 'watchers': 1,
                                      'audit': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1, '_version': 1,
                                      '_id_document': 1}, 'filter': None, 'default_sort': None, 'aggregation': None},
    'f_ors_agg': {'source': 'f_observations', 'aggregation': {'pipeline': [{'$unwind': '$type'}, {
        '$match': {'when': {'$gte': '$from', '$lte': '$to'}, 'workflow.state': '$state'}}, {'$group': {'_id': '$type',
                                                                                                       'count': {
                                                                                                           '$sum': 1}}},
                                                                           {'$sort': SON([('count', -1)])}],
                                                              'options': {}}, 'filter': None, 'default_sort': None,
                  'projection': {'_id': 1, '_updated': 1, '_created': 1, '_etag': 1}},
    'legacy_licenses': {'source': 'legacy_licenses', 'default_sort': [('id', 1)], 'filter': None,
                        'projection': {'id': 1, 'name': 1, 'active': 1, 'url': 1, '_id': 1, '_updated': 1,
                                       '_created': 1, '_etag': 1, '_version': 1, '_id_document': 1},
                        'aggregation': None},
    'legacy_licenses_versions': {'source': 'legacy_licenses_versions', 'default_sort': [('id', 1)], 'filter': None,
                                 'projection': {'id': 1, 'name': 1, 'active': 1, 'url': 1, '_id': 1, '_updated': 1,
                                                '_created': 1, '_etag': 1, '_version': 1, '_id_document': 1},
                                 'aggregation': None},
    'legacy_clubs': {'source': 'legacy_clubs', 'default_sort': [('id', 1)], 'filter': None,
                     'projection': {'id': 1, 'name': 1, 'active': 1, 'org': 1, 'locations': 1, 'planes': 1, 'roles': 1,
                                    'ot': 1, 'ci': 1, 'logo': 1, 'url': 1, '_id': 1, '_updated': 1, '_created': 1,
                                    '_etag': 1, '_version': 1, '_id_document': 1}, 'aggregation': None},
    'legacy_clubs_versions': {'source': 'legacy_clubs_versions', 'default_sort': [('id', 1)], 'filter': None,
                              'projection': {'id': 1, 'name': 1, 'active': 1, 'org': 1, 'locations': 1, 'planes': 1,
                                             'roles': 1, 'ot': 1, 'ci': 1, 'logo': 1, 'url': 1, '_id': 1, '_updated': 1,
                                             '_created': 1, '_etag': 1, '_version': 1, '_id_document': 1},
                              'aggregation': None},
    'legacy_melwin_licenses': {'source': 'legacy_melwin_licenses', 'default_sort': [('id', 1)], 'filter': None,
                               'projection': {'id': 1, 'name': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1},
                               'aggregation': None},
    'legacy_melwin_membership': {'source': 'legacy_melwin_membership', 'default_sort': [('id', 1)], 'filter': None,
                                 'projection': {'id': 1, 'name': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1},
                                 'aggregation': None},
    'legacy_melwin_clubs': {'source': 'legacy_melwin_clubs', 'default_sort': [('id', 1)], 'filter': None,
                            'projection': {'id': 1, 'name': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1},
                            'aggregation': None},
    'legacy_melwin_users': {'source': 'legacy_melwin_users', 'default_sort': [('id', 1)], 'filter': None,
                            'projection': {'id': 1, 'active': 1, 'updated': 1, 'firstname': 1, 'lastname': 1,
                                           'fullname': 1, 'birthdate': 1, 'gender': 1, 'email': 1, 'phone': 1,
                                           'location': 1, 'membership': 1, 'licenses': 1, '_id': 1, '_updated': 1,
                                           '_created': 1, '_etag': 1}, 'aggregation': None},
    'content': {'source': 'content', 'filter': None, 'default_sort': None,
                'projection': {'title': 1, 'slug': 1, 'body': 1, 'space_key': 1, 'parent': 1, 'order': 1, 'ref': 1,
                               'owner': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1, '_version': 1,
                               '_id_document': 1}, 'aggregation': None},
    'content_versions': {'source': 'content_versions', 'filter': None, 'default_sort': None,
                         'projection': {'title': 1, 'slug': 1, 'body': 1, 'space_key': 1, 'parent': 1, 'order': 1,
                                        'ref': 1, 'owner': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1,
                                        '_version': 1, '_id_document': 1}, 'aggregation': None},
    'content_aggregate_parents': {'source': 'content', 'aggregation': {
        'pipeline': [{'$match': {'_id': '$start_id', 'parent': {'$ne': None}}},
                     {'$project': {'_id': 1, 'title': 1, 'slug': 1, 'space_key': 1, 'parent': 1}}, {
                         '$graphLookup': {'from': 'content', 'startWith': '$parent', 'connectFromField': 'parent',
                                          'connectToField': '_id', 'maxDepth': 3, 'depthField': 'levelAbove',
                                          'as': 'parents'}}, {
                         '$project': {'parents._id': 1, 'parents.title': 1, 'parents.slug': 1, 'parents.space_key': 1,
                                      'parents.levelAbove': 1}}, {'$sort': SON([('parents.levelAbove', -1)])}],
        'options': {}}, 'filter': None, 'default_sort': None,
                                  'projection': {'_id': 1, '_updated': 1, '_created': 1, '_etag': 1}},
    'content_aggregate_children': {'source': 'content', 'aggregation': {
        'pipeline': [{'$match': {'_id': '$start_id'}}, {'$project': {'_id': 1, 'title': 1, 'slug': 1, 'space_key': 1}},
                     {'$graphLookup': {'from': 'content', 'startWith': '$_id', 'connectFromField': '_id',
                                       'connectToField': 'parent', 'maxDepth': '$max_depth',
                                       'depthField': 'levelBelove', 'as': 'children'}}, {
                         '$project': {'children._id': 1, 'children.title': 1, 'children.slug': 1,
                                      'children.space_key': 1, 'children.levelBelove': 1}},
                     {'$sort': {'children.leveBelove': 1}}], 'options': {}}, 'filter': None, 'default_sort': None,
                                   'projection': {'_id': 1, '_updated': 1, '_created': 1, '_etag': 1}},
    'content_aggregate_siblings': {'source': 'content', 'aggregation': {
        'pipeline': [{'$match': {'_id': '$parent_id'}}, {'$project': {'_id': 1, 'title': 1, 'slug': 1, 'space_key': 1}},
                     {'$graphLookup': {'from': 'content', 'startWith': '$_id', 'connectFromField': '_id',
                                       'connectToField': 'parent', 'maxDepth': 0, 'depthField': 'levelBelove',
                                       'restrictSearchWithMatch': {'_id': {'$ne': '$current_id'}}, 'as': 'siblings'}}, {
                         '$project': {'siblings._id': 1, 'siblings.title': 1, 'siblings.slug': 1,
                                      'siblings.space_key': 1, 'siblings.levelBelove': 1}},
                     {'$sort': {'siblings.leveBelove': 1}}], 'options': {}}, 'filter': None, 'default_sort': None,
                                   'projection': {'_id': 1, '_updated': 1, '_created': 1, '_etag': 1}},
    'files': {'source': 'files', 'filter': None, 'default_sort': None,
              'projection': {'name': 1, 'description': 1, 'tags': 1, 'content_type': 1, 'size': 1, 'owner': 1, 'ref': 1,
                             'ref_id': 1, 'file': 1, 'acl': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1,
                             '_version': 1, '_id_document': 1}, 'aggregation': None},
    'files_versions': {'source': 'files_versions', 'filter': None, 'default_sort': None,
                       'projection': {'name': 1, 'description': 1, 'tags': 1, 'content_type': 1, 'size': 1, 'owner': 1,
                                      'ref': 1, 'ref_id': 1, 'file': 1, 'acl': 1, '_id': 1, '_updated': 1,
                                      '_created': 1, '_etag': 1, '_version': 1, '_id_document': 1},
                       'aggregation': None},
    'tags': {'source': 'tags', 'default_sort': [('tag', 1), ('group', 1)], 'filter': None,
             'projection': {'tag': 1, 'group': 1, 'freq': 1, 'related': 1, '_id': 1, '_updated': 1, '_created': 1,
                            '_etag': 1, '_version': 1, '_id_document': 1}, 'aggregation': None},
    'tags_versions': {'source': 'tags_versions', 'default_sort': [('tag', 1), ('group', 1)], 'filter': None,
                      'projection': {'tag': 1, 'group': 1, 'freq': 1, 'related': 1, '_id': 1, '_updated': 1,
                                     '_created': 1, '_etag': 1, '_version': 1, '_id_document': 1}, 'aggregation': None},
    'dev': {'source': 'dev', 'filter': None, 'default_sort': None,
            'projection': {'app': 1, 'payload': 1, '_id': 1, '_updated': 1, '_created': 1, '_etag': 1},
            'aggregation': None}, 'help': {'source': 'help', 'filter': None, 'default_sort': None,
                                           'projection': {'key': 1, 'title': 1, 'body': 1, 'owner': 1, 'acl': 1,
                                                          '_id': 1, '_updated': 1, '_created': 1, '_etag': 1,
                                                          '_version': 1, '_id_document': 1}, 'aggregation': None},
    'help_versions': {'source': 'help_versions', 'filter': None, 'default_sort': None,
                      'projection': {'key': 1, 'title': 1, 'body': 1, 'owner': 1, 'acl': 1, '_id': 1, '_updated': 1,
                                     '_created': 1, '_etag': 1, '_version': 1, '_id_document': 1},
                      'aggregation': None}}}
