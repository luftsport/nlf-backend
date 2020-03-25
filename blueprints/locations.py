"""
    Locations vi Kartverket
    =======================
    
    Using kartverket's stedsnavn REST api [GET] to retrieve geographical names in Norway
    
"""

from flask import Blueprint, current_app as app, request, Response, abort, jsonify

from urllib import request as http
import urllib.parse
import requests

import xmltodict

from ext.app.decorators import require_token

LOCATIONS_URL = 'https://ws.geonorge.no/SKWS3Index/ssr/sok'
Locations = Blueprint('Location service via kartverket', __name__, )


@Locations.route("/search", methods=['GET'])
@require_token()
def search(name=None, max=10, epgs=4326):
    """ Search via kartverket's REST service
    - Response is xml, convert to dict with xmltodict
    - Transform each item to our format including geojson for coordinates
    - Transform items into list even if only one result
    
    @todo: need some length don't we? Well we have places like Å so maybe not.
    @todo: verify before http
    """

    if name != None:
        q = name
    else:
        q = request.args.get('q', default='', type=str)

    # query = urllib.parse.urlencode({'navn': q, 'epsgKode': epgs, 'eksakteForst': True, 'maxAnt': max})
    # r = http.urlopen("?%s" % query, timeout=5)
    # xml = r.read().decode('utf-8')

    r = requests.get(LOCATIONS_URL,
                     params={'navn': q, 'epsgKode': epgs, 'eksakteForst': True, 'maxAnt': max},
                     headers={'Accept-Encoding': 'gzip, deflate, br', 'Charset': 'utf-8'})
    if r.status_code == 200:
        print(r.encoding)
        r.encoding = 'UTF-8'
        p = xmltodict.parse(r.text)

        final = {}

        """
        p.get('sokRes').get('sokStatus').get('ok') true|false
        p.get('sokRes').get('sokStatus').get('melding') error message!
        
        """

        final.update({'_meta': {"page": 1, "total": 1, "max_results": p.get('sokRes').get('totaltAntallTreff')}})
        final.update({'_links': {"self": {"title": "locations for %s" % q, "href": "locations/search?q=%s" % q},
                                 "parent": {"title": "locations", "href": "locations"}
                                 }
                      })

        places = []

        if p.get('sokRes').get('sokStatus').get('ok') == 'false' or p.get('sokRes').get('totaltAntallTreff') == '0':
            final.update({'_items': places})
            return jsonify(**final)

        if isinstance(p.get('sokRes').get('stedsnavn'), list):
            for i in p.get('sokRes').get('stedsnavn'):
                places.append(transform(i))

        else:
            places = [transform(p.get('sokRes').get('stedsnavn'))]

        final.update({'_items': places})

        return jsonify(**final)


def transform(item):
    """ Transform item returned from kartverket's xml response
    """
    p = {}

    p.update({'geo': {'coordinates': [item.get('nord'), item.get('aust')], 'type': 'Point'}})
    p.update({'geo_type': item.get('navnetype')})
    p.update({'county': item.get('fylkesnavn')})
    p.update({'municipality': item.get('kommunenavn')})
    p.update({'name': item.get('stedsnavn')})

    return p

@Locations.route("/google", methods=['GET'])
@require_token()
def google():
    # enter your api key here
    api_key = 'AIzaSyCt7ni1T6AtGNlx-45DVirffvav8l7hlMw'

    # url variable store url
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    # The text string on which to search
    # query = input('Search query: ')

    # get method of requests module
    # return response object
    query = request.args.get('q', default='', type=str)
    r = requests.get(url, params={'query': query, 'key': api_key})

    # json method of response object convert
    #  json format data into python format data
    x = r.json()

    # now x contains list of nested dictionaries
    # we know dictionary contain key value pair
    # store the value of result key in variable y
    y = x['results']

    # keep looping upto length of y
    for i in range(len(y)):
        # Print value corresponding to the
        # 'name' key at the ith index of y
        print(y[i])

    return jsonify(**x)
