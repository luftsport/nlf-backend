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

LOCATIONS_URL = 'https://ws.geonorge.no/stedsnavn/v1/sted'
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
                     params={'sok': q}, #, 'utkoordsys': epgs, 'fuzzy': True, 'treffPerSide': max},
                     headers={'Accept-Encoding': 'gzip, deflate, br', 'Charset': 'utf-8'})
    if r.status_code == 200:
        print(r.encoding)
        r.encoding = 'UTF-8'
        p = r.json()  # xmltodict.parse(r.text)
        print(p)
        final = {}

        """
        p.get('sokRes').get('sokStatus').get('ok') true|false
        p.get('sokRes').get('sokStatus').get('melding') error message!
        
        """

        final.update({'_meta': {"page": 1, "total": 1, "max_results": p.get('metadata').get('totaltAntallTreff')}})
        final.update({'_links': {"self": {"title": "locations for %s" % q, "href": "locations/search?q=%s" % q},
                                 "parent": {"title": "locations", "href": "locations"}
                                 }
                      })

        places = []

        if final['_meta']['max_results'] == 0:
            final.update({'_items': places})
            return jsonify(**final)

        if isinstance(p.get('navn'), list):
            for i in p.get('navn'):

                # if i.get('geojson', {}).get('geometry', {}).get('type', None) == 'Point':
                places.append(transform(i))

        else:
            places = [transform(p.get('sokRes').get('stedsnavn'))]

        final.update({'_items': places})

        return jsonify(**final)


def transform(item):
    """ Transform item returned from kartverket's xml response
    """
    p = {}
    coordinates = [item['representasjonspunkt']['nord'], item['representasjonspunkt']['øst']]
       # "øst": 8.55186,
        #"nord": 63.24222,item['geojson']['geometry']['coordinates'][::-1]  # .reverse()
    p.update({'geo':
        {
            'coordinates': coordinates,
            'type': item['geojson']['geometry']['type']
        }
    })
    p.update({'geo_type': item.get('navneobjekttype')})
    p.update({'county': item.get('fylker', [{'fylkesnavn': 'Ukjent Fylke'}])[0]['fylkesnavn']})
    p.update({'municipality': item.get('kommuner', [{'kommunenavn': 'Ukjent Kommune'}])[0]['kommunenavn']})
    p.update({'name': item.get('stedsnavn', [{'skrivemåte': 'Ukjent Navn'}])[0]['skrivemåte']})
    print('P', p)
    return p
