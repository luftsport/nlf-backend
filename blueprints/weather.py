"""
    Weather
    ~~~~~~~

    Blueprint for accessing weather resources,


"""
from flask import Blueprint, current_app as app, request, Response, abort, jsonify
from bson import json_util
import simplejson as json

# Need custom decorators
from ext.app.decorators import *

from yr.libyr import Yr  # This should not be here
from ext.weather.aeromet import Aeromet
from ext.app.eve_helper import eve_abort, eve_response

import requests
from metar import Metar
import pytaf
import datetime

MET_URL = 'https://api.met.no/weatherapi'
TAFMETAR_URL = '{}/tafmetar/1.0/'.format(MET_URL)

Weather = Blueprint('Weather', __name__, )


def get_taf_metar(icao, date=datetime.datetime.now().strftime('%Y-%m-%d')):
    print('{}tafmetar.txt?icao={}&date={}'.format(TAFMETAR_URL, icao, date))
    resp = requests.get('{}tafmetar.txt?icao={}&date={}'.format(TAFMETAR_URL, icao, date))
    if resp.status_code == 200:
        try:
            tmp = resp.text.rstrip('=\n\n').replace('///', '').split('\n\n')
            taf = []
            metar = []

            if len(tmp) > 0:
                m = tmp[0]
                metar = [_m.lstrip('\n') for _m in m.split('=') if len(_m) > 4]
            if len(tmp) > 1:
                t = tmp[1]
                taf = [_t for _t in t.replace('\n', '').strip().split('=') if len(_t) > 4]

            return True, taf, metar
        except:
            pass
    return False, [], []


def get_metar_as_dict(metar):
    m = {}
    if 'metar.Metar.Metar' in '{}'.format(type(metar)):

        try:
            for k in metar.__dict__.keys():
                if k == 'sky':
                    tmp = []
                    for sky in metar.__dict__[k]:
                        if 'metar.Datatypes' in '{}'.format(type(sky[1])):
                            tmp.append([sky[0], sky[1].__dict__, sky[2]])
                        else:
                            tmp.append([sky[0], sky[1], sky[2]])
                    m[k] = tmp
                elif k == '_utcdelta':
                    m[k] = '{}'.format(metar.__dict__[k])
                elif k == 'time' or k == '_now':
                    m[k] = '{}Z'.format(metar.__dict__[k].isoformat())
                elif 'metar.Datatypes' in '{}'.format(type(metar.__dict__[k])):
                    m[k] = metar.__dict__[k].__dict__
                else:
                    m[k] = metar.__dict__[k]
        except:
            pass

    return m


def get_metar(icao, date=datetime.datetime.now().strftime('%Y-%m-%d')):
    resp = requests.get('{}tafmetar.txt?icao={}&date={}'.format(TAFMETAR_URL, icao, date))
    if resp.status_code == 200:
        return True, resp.text.strip().rstrip('=').split('=\n')


def get_taf(icao, date=datetime.datetime.now().strftime('%Y-%m-%d')):
    resp = requests.get('{}taf.txt?icao={}&date={}'.format(TAFMETAR_URL, icao, date))
    if resp.status_code == 200:
        return True, [t for t in resp.text.strip().replace('\n', '').split('=') if
                      len(t) > 4]  # [m for m in resp.text.lstrip('\n').split('=\n')]


def parse_metar(metar):
    try:
        return Metar.Metar(metar)
    except:
        pass

    return None


def parse_taf(taf):
    try:
        msg = pytaf.TAF(taf)
        decoder = pytaf.Decoder(msg)
        return decoder.decode_taf()
    except:
        pass

    return None


def get_nearest_metar(metars, target_time):
    if len(metars) == 0:
        return ''
    target_stamp = target_time.timestamp()
    mint = None
    index = 0
    for idx, m in enumerate(metars):
        mtime = target_stamp - datetime.datetime(target_time.year, target_time.month, target_time.day, int(m[7:9]),
                                                 int(m[9:11])).timestamp()
        if mint is None or mint > abs(mtime):
            mint = abs(mtime)
            index = idx

    return metars[index]


@Weather.route("/", methods=['GET'])
@require_token()
def index():
    return jsonify(**{'message': 'Use yr or aero resources'})


@Weather.route("/yr/<string:county>/<string:municipality>/<string:name>/<regex('(now|forecast|wind)'):what>",
               methods=['GET'])
@require_token()
def yr(what, county, municipality, name):
    """ Downloads data from yr.no
    @todo: Should fix units
    @todo: Should be based on locations and/or clubs default location in clubs '/yr/wind/375-F'
    """

    yrpath = ("Norge/%s/%s/%s" % (county, municipality, name))
    weather = Yr(location_name=yrpath)

    if what == 'now':

        return weather.now(as_json=True)

    elif what == 'forecast':
        return jsonify(**weather.dictionary['weatherdata']['forecast'])

    elif what == 'wind':
        wind_speed = dict()
        wind_speed['wind_forecast'] = [{'from': forecast['@from'], 'to': forecast['@to'], 'unit': 'knots',
                                        'speed': round(float(forecast['windSpeed']['@mps']) * 1.943844, 2)} for forecast
                                       in
                                       weather.forecast()]
        return jsonify(**wind_speed)


@Weather.route("/aero/<regex('[aA-zZ]{4}'):icao>/<regex('(metar|taf|shorttaf)'):what>", methods=['GET'])
@require_token()
def aero(what, icao):
    """ Aero resource retrieves metar and taf for given icao code
    @todo: support switches for raw and decoded messages
    @todo: support for historical data
    """

    w = Aeromet(icao.upper())

    if what == 'metar':
        return jsonify(**{'metar': w.metar()})
    elif what == 'taf':
        return jsonify(**{'taf': w.taf()})
    elif what == 'shorttaf':
        return jsonify(**{'shorttaf': w.shorttaf()})


@Weather.route("/tafmetar/<regex('[aA-zZ]{4}'):icao>/<regex('(metar|taf|tafmetar)'):what>", methods=['GET'])
@require_token()
def tafmetar(what, icao):
    """ Aero resource retrieves metar and taf for given icao code
    @todo: support switches for raw and decoded messages
    @todo: support for historical data
    """
    ret = ''
    w = Aeromet(icao.upper())
    taf, metar = w.tafmetar()
    if what == 'taf':
        return jsonify(**{'taf': taf})
    elif what == 'metar':
        return jsonify(**{'metar': metar})
    else:
        return jsonify(**{'metar': metar, 'taf': taf})


"""
New metar methods using api.met.no
"""


@Weather.route("/met/<regex('[aA-zZ]{4}'):icao>/<regex('[0-9]{4}-[0-9]{2}-[0-9]{2}'):date>", methods=['GET'])
@require_token()
def met_tafmetar(icao, date):
    try:
        # print(icao, date)
        status, taf, metar = get_taf_metar(icao, date)

        if status is True:
            return eve_response({'taf': taf, 'metar': metar}, 200)
        else:
            # print(get_taf_metar(icao, date))
            pass
    except Exception as e:
        app.logger.error(e)

    return eve_abort(500, 'Could not process')


@Weather.route("/met/parse/<regex('(metar|taf)'):what>/<string:msg>", methods=['GET'])
@require_token()
def met_parse(what, msg):
    try:
        if what == 'metar':
            resp = parse_metar(msg)
        elif what == 'taf':
            resp = parse_taf(msg)

        return eve_response({'decoded': resp, 'msg': msg}, 200)
    except:
        return eve_abort(404, 'Could not process')


@Weather.route("/met/metar/<regex('[aA-zZ]{4}'):icao>", methods=['GET'])
@require_token()
def met_get_metar_dict(icao):
    try:
        status, taf, metar = get_taf_metar(icao)
        if len(metar) > 0:
            resp = get_metar_as_dict(Metar.Metar(metar[-1]))
        else:
            status, metar = get_metar(icao)
            if len(metar) > 0:
                resp = get_metar_as_dict(Metar.Metar(metar[-1]))
            else:
                resp = {}

        return eve_response({'icao': icao, 'metar': resp})
    except Exception as e:
        app.logger.error(e)
        return eve_abort(404, 'Could not process')


@Weather.route("/met/metar/nearest/<regex('[aA-zZ]{4}'):icao>/<string:date>", methods=['GET'])
@require_token()
def met_nearest_metar(icao, date):
    try:
        target_time = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
        status, tafs, metars = get_taf_metar(icao, target_time.strftime('%Y-%m-%d'))
        metar = get_nearest_metar(metars, target_time)
        parsed = parse_metar(metar)
        return eve_response({'metar': metar, 'parsed': '{}'.format(parsed)}, 200)
    except Exception as e:
        ppp.logger.error(e)
        return eve_abort(404, 'Could not process {}'.format(e))
