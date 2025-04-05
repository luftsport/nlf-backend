from flask import Blueprint, request, current_app as app
import requests
from ext.app.eve_helper import eve_abort, eve_response
import kml2geojson
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from ext.app.decorators import require_token
import base64
from bs4 import BeautifulSoup
Flightlog = Blueprint('Flightlog Blueprint', __name__, )

"""

    Flightlog API
    
    This API is used to fetch data from flightlog.org
    
    rqtid (request id?)
    1 list of pilots and their flights
    2 *table of this trip
    3 *image of this trip
    4 None
    5 Utc xml document
    6 Error
    7 None
    8 Empty table
    9 Table of countries
    10 Empty table
    11 Empty table
    12 Table of starts
    13 Empty table
    14 Empty table
    15 Empty table
    16 Empty table
    17 Image with errors
    18 Flightlog graphs
    19 *KML file
    20 Html google map
    21 All tracklogs json, ts parameter how?
    22 ts for tracklog given a trip id for a trip with tracklog


url = "http://stackoverflow.com/search?q=question"
params = {'lang':'en','tag':'python'}
url_parts = list(urlparse(url))
query = dict(parse_qs(url_parts[4]))
query.update(params)
url_parts[4] = urlencode(query)
print(urlunparse(url_parts))
    
    GET /flightlog/<string:url>
    Fetches a trip from flightlog.org
    
    Parameters: 
        url: The URL to the trip on flightlog.org
    Returns:
        A JSON object with the trip data
        
    GET /flightlog/kml/<string:url>
    Fetches a trip from flightlog.org and converts it to KML
            
    Parameters:
        url: The URL to the trip on flightlog.org
    Returns:
        A KML file with the trip data
        
"""

REQUESTS = {
    'trip': 2,
    'image': 3,
    'kml': 19
}


def _verify_and_modify_flightlog_url(url, request_type='trip'):
    try:
        url = base64.b64decode(url).decode('utf-8')
        print('decoded', url)
        if url.startswith('https://flightlog.org/fl.html?') is True:
            url_parts = list(urlparse(url))
            query = dict(parse_qs(url_parts[4]))
            query.update({'rqtid': REQUESTS[request_type]})
            newqs = urlencode(query, doseq=1)
            new_url = urlunparse([newqs if i == 4 else x for i,x in enumerate(url_parts)])
            return new_url
    except:
        pass
    return None


@Flightlog.route("/", methods=['GET'])
@require_token()
def test():
    return eve_response('Flightlog API')


@Flightlog.route("/kml/<string:url>", methods=['GET'])
def get_kml(url):
    r = requests.get('https://flightlog.org/fl.html?rqtid=19&trip_id=891473&20240422143946')
    return eve_response(kml2geojson.convert(StringIO(r.text)))


@Flightlog.route("trip", methods=['GET'])
@require_token()
def get_trip():
    url = request.args.get('url')
    trip_url = _verify_and_modify_flightlog_url(url, 'trip')
    print(trip_url)
    if trip_url is not None:
        r = requests.get(trip_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Find the table (assuming it's the only one or has a specific class/id)
        table = soup.find('table')
        # Extract header
        header = [th.text.strip() for th in table.find_all('th')]
        # Extract header (snake_case keys)
        header = [th.text.strip() for th in table.find_all('th')]
        # Extract row data
        row = [td.text.strip() for td in table.find_all('td')]
        # Create a dictionary by zipping header and row
        flight_dict = dict(zip(header, row))
        return eve_response(flight_dict)

    eve_abort(400, 'Invalid URL')
