from flask import Blueprint, request, current_app as app
import requests
from ext.app.eve_helper import eve_abort, eve_response
import kml2geojson
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from ext.app.decorators import require_token
import base64
from bs4 import BeautifulSoup
from io import StringIO
import re
Flightlog = Blueprint('Flightlog Blueprint', __name__, )

"""

    Flightlog API
    
    This API is used to fetch data from flightlog.org
    
    l: language (1 Norwegian, 2 English, 3 Swedish)
    a: 
    Start:
    a: 1 Frontpage starts
    a: 2 => takeoffs per country + top ten
    a: 3 => takeoffs per country
    a: 4=> links?
    a: 21 => top ten
    a: 22 => start!
    a: 25 => medlemmer per klubb!!!
    POST https://flightlog.org/fl.html?l=1&a=21&country_id=160 => liste over 
    fl.html?l=1&a=21&country_id=160&gm=2 => alle starter per land i KML fil!
    Trip:
    a=34 + trip id
    
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
            new_url = urlunparse([newqs if i == 4 else x for i, x in enumerate(url_parts)])
            return new_url
    except:
        pass
    return None

def _get_and_parse_flight_stats_regex(url) -> dict:
    r = requests.get(base64.b64decode(url).decode('utf-8'))
    soup = BeautifulSoup(r.text, 'html.parser')
    pre = soup.find('pre')
    print(pre)
    stats = {}
    if pre and len(pre)>0:
        lines = str(pre).strip().split('\n')[1:]  # Skip header
        patterns = {
            "date": r"Date\s+([\d-]+)",
            "start_finish": r"Start/finish\s+([\d:]+)\s+-\s+([\d:]+)",
            "duration": r"Duration\s+([\d\s:]+)",
            "pair": r"(\w+(?:\.\s\w+)?)\s*\((max/min|10s/60s)\)\s+([\d.-]+)\s*/\s*([\d.-]+)\s*(\w+)"
        }
        for line in lines:
            line = line.strip()
            match1 = re.match(patterns["date"], line)
            match2 = re.match(patterns["start_finish"], line)
            match3 = re.match(patterns["duration"], line)
            match4 = re.match(patterns["pair"], line)
            if match1:
                stats["date"] = match1.group(1)
            elif match2:
                stats["start_time"] = match2.group(1)
                stats["finish_time"] = match2.group(2)
            elif match3:
                stats["duration"] = match3.group(1).replace(" : ", ":")
            elif match4:
                label, pair_type, val1, val2, unit = match4.groups()
                key = label.lower().replace(" ", "_").replace(".", "")
                if pair_type == "max/min":
                    stats[key] = {"max": float(val1), "min": float(val2), "unit": unit}
                elif pair_type == "10s/60s":
                    stats[key] = {"10s": float(val1), "60s": float(val2), "unit": unit}
        print(stats)
    return stats

def _parse_coordinates(text) -> dict:
    regres = re.search(r"N\s*(\d+)°\s*(\d+)'?\s*(\d+)''\s*E\s*(\d+)°\s*(\d+)'?\s*(\d+)''", text)
    dms_string = "".join(regres[0].strip().split(" ")).replace('\xa0', '')

    # Regex to extract components
    pattern = r"N(\d+)°(\d+)'(\d+)''E(\d+)°(\d+)'(\d+)''"
    match = re.match(pattern, dms_string)

    if match:
        # Extract latitude components
        lat_deg = int(match.group(1))  # 60
        lat_min = int(match.group(2))  # 42
        lat_sec = int(match.group(3))  # 34

        # Extract longitude components
        lon_deg = int(match.group(4))  # 8
        lon_min = int(match.group(5))  # 53
        lon_sec = int(match.group(6))  # 12

        # Convert to decimal degrees
        return {'lat': lat_deg + (lat_min / 60) + (lat_sec / 3600), 'lng': lon_deg + (lon_min / 60) + (lon_sec / 3600)}
@Flightlog.route("/", methods=['GET'])
@require_token()
def test():
    return eve_response('Flightlog API')


@Flightlog.route("/kml", methods=['GET'])
def get_kml():
    url = request.args.get('url')
    trip_url = _verify_and_modify_flightlog_url(url, 'kml')
    print(trip_url)
    if trip_url is not None:
        r = requests.get(trip_url)
        return eve_response(kml2geojson.convert(StringIO(r.text)))
    eve_abort(400, 'Invalid URL')


@Flightlog.route("/trip", methods=['GET'])
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
        # Extract header (snake_case keys)
        header = [th.text.strip() for th in table.find_all('th')]
        # Extract row data
        row = [td.text.strip() for td in table.find_all('td')]
        # Create a dictionary by zipping header and row
        flight_dict = dict(zip(header, row))

        if 'description' in flight_dict and len(flight_dict['description']) > 0:

            flight_dict['flight_stats'] = _get_and_parse_flight_stats_regex(url)

        return eve_response(flight_dict)

    eve_abort(400, 'Invalid URL')

@Flightlog.route("/start/<int:country_id>/<int:start_id>", methods=['GET'])
@require_token()
def get_start(country_id, start_id):
    r = requests.get(f'https://flightlog.org/fl.html?l=1&a=22&country_id={country_id}&start_id={start_id}')
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.findAll('table')
    table = tables[-1]

    # Extract row data
    row = [td.text.strip() for td in table.find_all('td')]

    labels = ['region', 'altitude', 'Description', 'Coordinates', 'Siterecord', 'created', 'Updated']
    row = [x for x in row if x.startswith('Map with Holfuy weather') is False]
    data = {}
    for index, item in enumerate(row):
        if item in labels:
            data.update({item.lower(): row[index + 1] or ''})

    if 'coordinates' in data:
        data['coordinates'] = _parse_coordinates(data['coordinates'])

            
    return eve_response(data)