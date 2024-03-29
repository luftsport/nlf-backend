

"""
    Custom info route
    =================
    
    @todo: clean up url's those are only correct when base url is accessed

"""

from flask import Blueprint, current_app as app, request, Response, abort, jsonify


Info = Blueprint('Custom info resource', __name__,)

@Info.route("/", methods=['GET'])
def api_info():
    # Build a dictionary
    dict = {'api': 'NLF Platform',
            'version': '0.1.0', 
            'contact': 'NLF',
            'email': 'NLF <post@nlf.no>',
            'api_url': request.base_url, 
            'doc_url': request.base_url + '/docs',
            'base_url': request.base_url,
            }
    
    # Jsonify the dictionary and return it
    return jsonify(**dict)