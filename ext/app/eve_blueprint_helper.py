from flask import current_app as app, Blueprint, Request, request, jsonify, Response, make_response
import json
from datetime import datetime
from typing import Dict, Any, Optional, Union, List
from cerberus import Validator
from werkzeug.exceptions import HTTPException
from eve.io.mongo import Mongo
from eve.utils import config
from hashlib import md5
from pymongo.errors import PyMongoError
import functools
from typing import Dict, Optional, List, Union, Any, Callable, Tuple
from pymongo import ASCENDING, DESCENDING
from math import inf
# Global registry for Swagger specs
_SWAGGER_SPEC_REGISTRY = {}


class EveBlueprintError(HTTPException):
    """Custom exception for Eve-style error responses."""

    def __init__(self, code: int, description: str):
        super().__init__(description=description)
        self.code = code
        self.response = jsonify({
            "_status": "ERR",
            "_error": {
                "code": code,
                "message": description
            }
        })
        self.response.status_code = code


class SwaggerBlueprint(Blueprint):
    """Custom Blueprint that generates Swagger specs with automatic prefix."""

    def route(self, rule: str, **options) -> Callable:
        """Override route method to generate Swagger spec with Blueprint name as prefix."""
        methods = options.get('methods', ['GET'])
        resource = options.get('resource', None)

        # Normalize path for Swagger (e.g., convert <string:_id> to {_id})
        swagger_path = rule.replace('<string:_id>', '{_id}')

        # Use Blueprint name in lowercase as default prefix, override with url_prefix if set
        default_prefix = f"/{self.name.lower()}"
        url_prefix = f"/{self.url_prefix or default_prefix}"
        if url_prefix:
            swagger_path = f"{url_prefix.rstrip('/')}/{swagger_path.lstrip('/')}"

        # Initialize Swagger spec for this path
        _SWAGGER_SPEC_REGISTRY[swagger_path] = {}

        for method in methods:
            method_lower = method.lower()
            operation = {
                'summary': f"{method.upper()} {swagger_path}",
                'description': f"Custom {method.upper()} endpoint for {resource or 'resource'}",
                'responses': {
                    str(200 if method_lower != 'post' else 201): {
                        'description': 'Successful response',
                        'content': {'application/json': {'schema': {'type': 'object'}}}
                    },
                    '204': {'description': 'No content'} if method_lower == 'delete' else None,
                    '400': {'description': 'Bad request'},
                    '401': {'description': 'Unauthorized'},
                    '404': {'description': 'Resource or item not found'},
                    '412': {'description': 'Precondition failed (ETag mismatch)'},
                    '422': {'description': 'Validation error'},
                    '503': {'description': 'Database error'}
                }
            }

            # Add path parameters (e.g., _id)
            if '{_id}' in swagger_path:
                operation['parameters'] = operation.get('parameters', []) + [
                    {
                        'name': '_id',
                        'in': 'path',
                        'description': 'MongoDB ObjectId',
                        'required': True,
                        'schema': {'type': 'string', 'format': 'objectid'}
                    }
                ]

            # Add query parameters for GET (if collection endpoint)
            if method_lower == 'get' and '{_id}' not in swagger_path:
                operation['parameters'] = operation.get('parameters', []) + [
                    {'name': 'where', 'in': 'query', 'description': 'JSON query filter', 'required': False, 'schema': {'type': 'string'}},
                    {'name': 'sort', 'in': 'query', 'description': 'Sort fields', 'required': False, 'schema': {'type': 'string'}},
                    {'name': 'embedded', 'in': 'query', 'description': 'Fields to embed', 'required': False, 'schema': {'type': 'string'}},
                    {'name': 'projection', 'in': 'query', 'description': 'Fields to include/exclude', 'required': False, 'schema': {'type': 'string'}},
                    {'name': 'page', 'in': 'query', 'description': 'Page number', 'required': False, 'schema': {'type': 'integer', 'default': 1}},
                    {'name': 'max_results', 'in': 'query', 'description': 'Items per page', 'required': False, 'schema': {'type': 'integer', 'default': 25}}
                ]

            # Add request body for POST, PUT, PATCH
            if method_lower in ['post', 'put', 'patch']:
                operation['requestBody'] = {
                    'content': {'application/json': {'schema': {'type': 'object'}}},
                    'required': True
                }

            # Add If-Match header for endpoints requiring ETag
            # if app.config.get('IF_MATCH') and method_lower in ['get', 'put', 'patch', 'delete'] and '{_id}' in swagger_path:
            #    operation['parameters'] = operation.get('parameters', []) + [
            #        {'name': 'If-Match', 'in': 'header', 'description': 'ETag for concurrency control', 'required': True, 'schema': {'type': 'string'}}
            #    ]

            _SWAGGER_SPEC_REGISTRY[swagger_path][method_lower] = operation

        # Call parent Blueprint's route method
        def decorator(f):
            return super(SwaggerBlueprint, self).route(rule, **options)(f)

        return decorator


def get_swagger_blueprint_spec(blueprint: Blueprint, resource: str = None) -> Dict:
    """Return collected Swagger specs for the Blueprint."""
    return _SWAGGER_SPEC_REGISTRY


def get_data_driver(collection_name: str):
    """Get Eve's data driver for the given collection."""
    if not 'DOMAIN' in app.config or collection_name not in app.config['DOMAIN']:
        raise EveBlueprintError(404, f"Collection resource '{collection_name}' not found")
    driver = app.data.driver
    if not driver:
        raise EveBlueprintError(500, "No data driver configured in Eve app")
    if isinstance(driver, Mongo):
        if collection_name not in driver.db.list_collection_names():
            raise EveBlueprintError(404, f"Collection '{collection_name}' not found in database")
    return driver.db[collection_name]


def trigger_hooks(resource: str, hook_type: str, method: str = None,
                  request: Request = None, lookup: Dict = None,
                  items: Union[List[Dict], Dict] = None, response: Any = None) -> None:
    """Trigger Eve's request or data layer hooks."""
    if not 'DOMAIN' in app.config or resource not in app.config['DOMAIN']:
        raise EveBlueprintError(404, f"Resource '{resource}' not found for hooks")
    hooks = []
    if hook_type in ['pre', 'post']:
        hook_name = f"on_{hook_type}_{method}"
        resource_hook_name = f"{hook_name}_{resource}"
        if hasattr(app, hook_name):
            hooks.append(getattr(app, hook_name))
        if hasattr(app, resource_hook_name):
            hooks.append(getattr(app, resource_hook_name))
        hooks.extend(app.config['DOMAIN'][resource].get('hooks', {}).get(f"{hook_type}_{method}", []))
    else:
        hook_name = f"on_{hook_type}"
        resource_hook_name = f"{hook_name}_{resource}"
        if hasattr(app, hook_name):
            hooks.append(getattr(app, hook_name))
        if hasattr(app, resource_hook_name):
            hooks.append(getattr(app, resource_hook_name))
        hooks.extend(app.config['DOMAIN'][resource].get('hooks', {}).get(hook_type, []))
    for hook in hooks:
        try:
            if hook_type == 'pre':
                hook(request, lookup)
            elif hook_type == 'post':
                hook(request, lookup, response)
            elif hook_type in ['insert', 'update', 'delete', 'replace']:
                hook(resource, items)
            elif hook_type in ['inserted', 'updated', 'deleted', 'replaced']:
                hook(resource, items)
        except Exception as e:
            raise EveBlueprintError(500, f"Hook {hook_name} failed: {str(e)}")


def parse_request(resource: str = None, document_id: str = None, is_blueprint=False, trigger_hooks=True) -> Dict[str, Any]:
    """Parse Flask request args/body in Eve style with ETag and hook support."""
    args = request.args
    parsed = {}

    if resource and 'DOMAIN' in app.config and (resource not in app.config['DOMAIN'] and is_blueprint is False):
        raise EveBlueprintError(404, f"Resource '{resource}' not found")

    if 'where' in args:
        try:
            parsed['where'] = json.loads(args['where'])
            if not isinstance(parsed['where'], dict):
                raise EveBlueprintError(400, "'where' must be a JSON object")
        except json.JSONDecodeError:
            raise EveBlueprintError(400, "Invalid 'where' JSON syntax")

    if 'sort' in args:
        try:
            parsed['sort'] = [s.strip() for s in args['sort'].split(',')]
            for s in parsed['sort']:
                if not s.lstrip('-'):
                    raise EveBlueprintError(400, "Invalid 'sort' field")
        except Exception:
            raise EveBlueprintError(400, "Invalid 'sort' syntax")

    if 'embedded' in args:
        try:
            parsed['embedded'] = json.loads(args['embedded'])
            if not isinstance(parsed['embedded'], list):
                raise EveBlueprintError(400, "'embedded' must be a JSON array")
        except json.JSONDecodeError:
            raise EveBlueprintError(400, "Invalid 'embedded' JSON syntax")

    if 'projection' in args:
        try:
            parsed['projection'] = json.loads(args['projection'])
            if not isinstance(parsed['projection'], dict):
                raise EveBlueprintError(400, "'projection' must be a JSON object")
        except json.JSONDecodeError:
            raise EveBlueprintError(400, "Invalid 'projection' JSON syntax")

    try:
        parsed['page'] = int(args.get('page', 1))
        if parsed['page'] < 1:
            raise ValueError
    except ValueError:
        raise EveBlueprintError(400, "'page' must be a positive integer")

    try:
        parsed['max_results'] = int(args.get('max_results', app.config.get('PAGINATION_DEFAULT', 25)))
        if parsed['max_results'] < 0:
            raise ValueError
    except ValueError:
        raise EveBlueprintError(400, "'max_results' must be a non-negative integer")

    if resource and 'DOMAIN' in app.config and resource in app.config['DOMAIN']:
        domain = app.config['DOMAIN'][resource]
        max_limit = domain.get('max_results', app.config.get('PAGINATION_LIMIT', 50))  # PAGINATION_DEFAULT
        if parsed['max_results'] > max_limit:
            raise EveBlueprintError(400, f"'max_results' exceeds limit of {max_limit}")
        if parsed['max_results'] == 0:
            parsed['page'] = 1

    # ETag validation via If-Match header
    if app.config.get('IF_MATCH') and 'If-Match' in request.headers:
        parsed['if_match'] = request.headers['If-Match']
        if resource and document_id:
            try:
                driver = get_data_driver(resource)
                item = driver.find_one(resource, {'_id': document_id})
                if item:
                    stored_etag = item.get('_etag')
                    if stored_etag and parsed['if_match'] != stored_etag:
                        raise EveBlueprintError(412, "ETag mismatch")
                else:
                    raise EveBlueprintError(404, f"Item {document_id} not found for ETag validation")
            except Exception as e:
                if isinstance(e, EveBlueprintError):
                    raise
                raise EveBlueprintError(500, f"ETag validation failed: {str(e)}")

    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            body = request.get_json()
            if body is None:
                raise EveBlueprintError(400, "Missing or invalid JSON body")
            if resource and 'DOMAIN' in app.config and resource in app.config['DOMAIN']:
                schema = app.config['DOMAIN'][resource].get('schema', {})
                v = Validator(schema, allow_unknown=True)
                if not v.validate(body):
                    raise EveBlueprintError(422, f"Validation failed: {v.errors}")
            parsed['body'] = body
        except Exception as e:
            if isinstance(e, EveBlueprintError):
                raise
            raise EveBlueprintError(400, "Invalid JSON body")

    if trigger_hooks and resource and request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        try:
            trigger_hooks(resource, 'pre', request.method, request, parsed.get('where', {}))
        except EveBlueprintError as e:
            pass
        except Exception as e:
            print('Failed trigering hooks but thats ok')

    return parsed


def parsed_to_pymongo(
        parsed: Dict[str, Any],
        collection=None,  # optional: if you want to execute immediately
        default_sort: List = None
) -> Tuple[Dict, List, Dict, int, int]:
    """
    Convert parsed Eve-style request into PyMongo query components.
    Returns: (query, sort_list, projection, skip, limit)
    """
    # 1. Base query (Eve 'where' is already MongoDB syntax)
    query = parsed.get('where') or {}

    # 2. Sort
    sort_list = []
    if parsed.get('sort'):
        for field in parsed['sort']:
            if field.startswith('-'):
                sort_list.append((field[1:], DESCENDING))
            else:
                sort_list.append((field, ASCENDING))
    elif default_sort:
        sort_list = default_sort

    # 3. Projection
    projection = parsed.get('projection') or None

    # 4. Pagination
    page = parsed.get('page', 1)
    max_results = parsed.get('max_results', 25)

    if max_results == 0:  # Eve behavior: return all
        skip = 0
        limit = 0  # 0 means no limit in PyMongo
    else:
        skip = (page - 1) * max_results
        limit = max_results

    if collection is not None:
        cursor = collection.find(
            filter=query,
            projection=projection,
            sort=sort_list if sort_list else None,
            skip=skip,
            limit=limit
        )
        return cursor

    return query, sort_list, projection, skip, limit


def execute_parsed_query(collection, parsed: dict, **extra_find_kwargs):
    query, sort, proj, skip, limit = parsed_to_pymongo(parsed)
    print(f"Executing query: {query}, sort: {sort}, projection: {proj}, skip: {skip}, limit: {limit}")
    result = collection.find(
        filter=query,
        projection=proj,
        sort=sort,
        skip=skip,
        limit=limit,
        **extra_find_kwargs
    )

    count = collection.count_documents(query)
    return list(result), count, skip, limit


def format_response(items: Union[List[Dict], Dict], total: Optional[int] = None, resource: str = None,
                    status_code: int = 200, is_collection: bool = False) -> Response:
    """Format response in Eve style with ETag and hook support."""
    try:
        is_collection_response = is_collection or isinstance(items, list)
        items = [items] if not isinstance(items, list) else items
        if is_collection_response and total is None:
            # raise EveBlueprintError(500, "'total' must be provided for collection responses")
            total = len(items)
        if is_collection_response and (not isinstance(total, int) or total < 0):
            raise EveBlueprintError(500, "'total' must be a non-negative integer")

        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    if '_updated' not in item:
                        item['_updated'] = datetime.utcnow().isoformat()
                    if '_id' not in item:
                        item['_id'] = item.get('id', str(hash(str(item))))
                    if app.config.get('IF_MATCH') and '_etag' not in item:
                        item_str = json.dumps(item, sort_keys=True)
                        item['_etag'] = md5(item_str.encode('utf-8')).hexdigest()
        if is_collection_response:
            max_results = int(request.args.get('max_results', len(items)))  # app.config.get('PAGINATION_DEFAULT', 25)))
            page = int(request.args.get('page', 1))
            response_data = {
                "_items": items if len(items) <= max_results or max_results is None else items[max_results * (page - 1):max_results * page],
                "_meta": {
                    "page": 1 if max_results == total else page,
                    "max_results": max_results,
                    "total": total
                    # "max_pages": (total + max_results - 1) // max_results if total is not None and max_results > 0 else 1
                }
            }
        else:
            response_data = items[0]
        if resource and request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            try:
                trigger_hooks(resource, 'post', request.method, request,
                              lookup={'_id': {'$in': [item['_id'] for item in items]}},
                              response=response_data)
            except Exception as e:
                pass
        resp = make_response(jsonify(response_data), status_code)
        # resp.status_code = status_code
        print(resp, type(resp))
        return resp  # , status_code # Response(resp, status=status_code, mimetype='application/json')
    except Exception as e:
        if isinstance(e, EveBlueprintError):
            raise
        raise EveBlueprintError(500, f"Response formatting failed: {str(e)}")


def handle_get(resource: str, document_id: Optional[str] = None,
               where: Dict = None, sort: List[str] = None, page: int = 1, max_results: int = 0) -> Response:
    """Handle GET requests for collections or single items."""
    try:
        driver = get_data_driver(resource)
        where = where or {}
        sort = sort or ['-_created']
        if document_id:
            item = driver.find_one(resource, {'_id': document_id})
            if not item:
                raise EveBlueprintError(404, f"Item {document_id} not found")
            return format_response(item, total=1, resource=resource, status_code=200)
        try:
            skip = (page - 1) * max_results
            if isinstance(driver, Mongo):
                cursor = driver.db[resource].find(where)
                if sort:
                    cursor = cursor.sort([(s.lstrip('-'), -1 if s.startswith('-') else 1) for s in sort])
                total = driver.db[resource].count_documents(where)
                cursor = cursor.skip(skip).limit(max_results)
                items = list(cursor)
            else:
                items, total = driver.find(where, sort=sort, skip=skip, limit=max_results)
            return format_response(items, total, resource=resource, status_code=200, is_collection=True)
        except PyMongoError as e:
            raise EveBlueprintError(503, f"Database error: {str(e)}")
    except EveBlueprintError:
        raise
    except Exception as e:
        raise EveBlueprintError(500, f"Unexpected error: {str(e)}")


def handle_post(resource: str, document: Union[Dict, List[Dict]]) -> Response:
    """Handle POST requests with batch support."""
    try:
        driver = get_data_driver(resource)
        documents = [document] if isinstance(document, dict) else document
        trigger_hooks(resource, 'insert', items=documents)
        try:
            if isinstance(driver, Mongo):
                result = driver.db[resource].insert_many(documents)
                inserted_ids = result.inserted_ids
                items = list(driver.db[resource].find({'_id': {'$in': inserted_ids}}))
            else:
                items = driver.insert(resource, documents)
        except PyMongoError as e:
            raise EveBlueprintError(503, f"Database error: {str(e)}")
        trigger_hooks(resource, 'inserted', items=items)
        response_data = items[0] if len(items) == 1 else items
        return format_response(response_data, total=len(items), resource=resource, status_code=201)
    except EveBlueprintError:
        raise
    except Exception as e:
        raise EveBlueprintError(500, f"Unexpected error: {str(e)}")


def handle_put(resource: str, document_id: str, document: Dict) -> Response:
    """Handle PUT requests for item replacement."""
    try:
        driver = get_data_driver(resource)
        trigger_hooks(resource, 'replace', items=[document])
        try:
            if isinstance(driver, Mongo):
                result = driver.db[resource].replace_one({'_id': document_id}, document)
                if result.matched_count == 0:
                    raise EveBlueprintError(404, f"Item {document_id} not found")
                items = [driver.db[resource].find_one({'_id': document_id})]
            else:
                items = driver.replace(resource, document_id, document)
                if not items:
                    raise EveBlueprintError(404, f"Item {document_id} not found")
        except PyMongoError as e:
            raise EveBlueprintError(503, f"Database error: {str(e)}")
        trigger_hooks(resource, 'replaced', items=items)
        return format_response(items[0], total=1, resource=resource, status_code=200)
    except EveBlueprintError:
        raise
    except Exception as e:
        raise EveBlueprintError(500, f"Unexpected error: {str(e)}")


def handle_patch(resource: str, document_id: str, updates: Dict) -> Response:
    """Handle PATCH requests for partial updates."""
    try:
        driver = get_data_driver(resource)
        trigger_hooks(resource, 'update', items=[updates])
        try:
            if isinstance(driver, Mongo):
                result = driver.db[resource].update_one({'_id': document_id}, {'$set': updates})
                if result.matched_count == 0:
                    raise EveBlueprintError(404, f"Item {document_id} not found")
                items = [driver.db[resource].find_one({'_id': document_id})]
            else:
                items = driver.update(resource, document_id, updates)
                if not items:
                    raise EveBlueprintError(404, f"Item {document_id} not found")
        except PyMongoError as e:
            raise EveBlueprintError(503, f"Database error: {str(e)}")
        trigger_hooks(resource, 'updated', items=items)
        return format_response(items[0], total=1, resource=resource, status_code=200)
    except EveBlueprintError:
        raise
    except Exception as e:
        raise EveBlueprintError(500, f"Unexpected error: {str(e)}")


def handle_delete(resource: str, document_id: str) -> Response:
    """Handle DELETE requests."""
    try:
        driver = get_data_driver(resource)
        item = driver.find_one(resource, {'_id': document_id})
        if not item:
            raise EveBlueprintError(404, f"Item {document_id} not found")
        trigger_hooks(resource, 'delete', items=[item])
        try:
            if isinstance(driver, Mongo):
                result = driver.db[resource].delete_one({'_id': document_id})
                if result.deleted_count == 0:
                    raise EveBlueprintError(404, f"Item {document_id} not found")
            else:
                driver.delete(resource, document_id)
        except PyMongoError as e:
            raise EveBlueprintError(503, f"Database error: {str(e)}")
        trigger_hooks(resource, 'deleted', items=[item])
        return make_response('', 204)
    except EveBlueprintError:
        raise
    except Exception as e:
        raise EveBlueprintError(500, f"Unexpected error: {str(e)}")
