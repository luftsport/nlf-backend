# geojson point [longitude, latitude, elevation]
# Eve "location": {"type":"Point","coordinates":[100.0,10.0]}}
# changing:
# 0) USE location: "$exists": false to filter new entries! And/or longitude_deg...
# 1) db.airports.updateMany({}, {$set: {"location": {"type":"Point","coordinates":[]}}})
# 2) db.airports.updateMany({}, {$rename: {'longitude_deg': 'location.coordinate.0', 'latitude_deg': 'location.coordinate.1', 'elevation_ft': 'location.coordinate.2'}}, false, true)
# 3) db.airports.updateMany({}, {$rename: {'location.coordinate': 'location.coordinates'}}, false, true)
# 4) var convert = function(document){var  intValue = parseFloat(document.location.coordinates[0], 10); db.airports.update({_id:document._id},{$set: {"location.coordinates.0": intValue}});}
# 5) db.airports.find({}).forEach(convert)
# 6) var convert = function(document){var intValue = parseFloat(document.location.coordinates[1], 10); db.airports.update({_id:document._id},{$set: {"location.coordinates.1": intValue}});}
# 7) db.airports.find({}).forEach(convert)
# 8) var convert = function(document){var intValue = parseInt(document.location.coordinates[2], 10); db.airports.update({_id:document._id},{$set: {"location.coordinates.2" : intValue}});}
# 9) db.airports.find({}).forEach(convert)
# 10) var covert = function(document) {db.airports.update({_id:document._id},{$set: {"location.coordinates.2" : null}});}
# 11) db.airports.find({"location.coordinates.2": NaN}).forEach(covert)
# 12) Examples
# ?where={"location": {"$near": {"$geometry": {"type":"Point", "coordinates": [10.258600235, 59.1866989136]}, "$maxDistance": 100000}}}
# sort=[("location.coordinates.2", -1)]&where={"iso_country": "NO","location.coordinates.2": {"$gte":0}}
# ?sort=[("location.coordinates.2", -1)]&where={"location.coordinates.2": {"$gt": 12500}}

RESOURCE_COLLECTION = 'aip_airports'
BASE_URL = 'aip/airports'

_schema = {'id': {'type': 'integer',
                  'required': True,
                  'readonly': True,
                  'unique': True
                  },
           'icao': {'type': 'string'},
           'type': {'type': 'string'},
           'name': {'type': 'string'},
           'continent': {'type': 'string'},
           'iso_country': {'type': 'string'},
           'iso_region': {'type': 'string'},
           'municipality': {'type': 'string'},
           'scheduled_service': {'type': 'string'},
           'gps_code': {'type': 'string'},
           'iata_code': {'type': 'string'},
           'local_code': {'type': 'string'},
           'home_link': {'type': 'string'},
           'wikipedia_link': {'type': 'string'},
           'keywords': {'type': 'string'},
           'location': {'type': 'point'}
           }

definition = {
    'item_title': 'Airports',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },
    'allow_unknown': True, # For text search meta
    'additional_lookup': {
        'url': 'regex("[A-Za-z]+")',
        'field': 'icao',
    },
    'extra_response_fields': ['icao'],
    'versioning': False,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'pagination_strategy': 'none',
    'mongo_indexes': {'icao': ([('icao', 1)], {'background': True}),
                      'codes': ([('iata_code', 1), ('gps_code', 1)], {'background': True}),
                      'iso': ([('iso_country', 1), ('iso_continent', 1)], {'background': True}),
                      'location': ([('location', '2dsphere')], {'background': True}),
                      'name': ([('icao', 'text'), ('name', 'text'), ('municipality', 'text'), ('keywords', 'text')], {'background': True})
                      },

    'schema': _schema

}
