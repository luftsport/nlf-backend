# from _base import acl_item_schema

from bson import SON

RESOURCE_COLLECTION = 'fallskjerm_quarter_report'

_schema = {
    'org_id': {
        'type': 'integer',
        'required': True
    },
    'year': {
        'type': 'integer',
        'required': True
    },
    'quarter': {
        'type': 'integer',
        'required': True
    },
    'date_from': {
        'type': 'datetime',
        'required': False

    },
    'date_to': {
        'type': 'datetime',
        'required': False

    },
    'ulg': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'ulu': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'ulmg': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'ulmu': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'ultg': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'ultu': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'ffg': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'ffu': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'affg': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'affu': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'demo': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'konkurranse': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'tandem': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'trening': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    'sum': {
        'type': 'integer',
        'required': True,
        'default': 0
    },
    # 'acl': acl_item_schema,
    'owner': {
        'type': 'integer',
        'required': True
    },
}

definition = {
    'item_title': 'Quarterly jump reports',
    'url': 'fallskjerm/report/quarter',
    'description': 'Jump numbers quarterly',

    'datasource': {'source': RESOURCE_COLLECTION,
                   'default_sort': [('year', 1), ('quarter', 1)],
                   },
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],

    'versioning': False,
    'mongo_indexes': {'dates': ([('date_to', 1), ('date_from', 1), ('quarter', 1), ('year', 1)], {'background': True}),
                      'org': ([('org_id', 1)], {'background': True}),
                      },
    'schema': _schema,
}

# Aggregations

# Sum per år for en organisasjon!
agg_sum_year = {
    'url': 'fallskjerm/report/year',
    'item_title': 'Jump numbers yearly',
    'pagination': False,
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {
                    "$match": {
                        "org_id": "$org_id",
                        # "year": {"$in": "$years"}
                    }
                },
                {
                    '$group':
                        {
                            '_id': '$year',  # '{'report_year': '$year'},
                            "ulg": {'$sum': '$ulg'},
                            "ulu": {'$sum': '$ulu'},
                            "ulmg": {'$sum': '$ulmg'},
                            "ulmu": {'$sum': '$ulmu'},
                            "ultg": {'$sum': '$ultg'},
                            "ultu": {'$sum': '$ultu'},
                            "ffg": {'$sum': '$ffg'},
                            "ffu": {'$sum': '$ffu'},
                            "affg": {'$sum': '$affg'},
                            "affu": {'$sum': '$affu'},
                            "trening": {'$sum': '$trening'},
                            "konkurranse": {'$sum': '$konkurranse'},
                            "demo": {'$sum': '$demo'},
                            "tandem": {'$sum': '$tandem'},
                            "students": {
                                "$sum": {
                                    '$add': ["$ulg", "$ulu", "$ulmg", "$ulmu", "$ultg", "$ultu", "$ffg", "$ffu",
                                             "$affg", "$affu"]
                                }
                            },
                            "senior": {
                                "$sum": {
                                    '$add': ["$trening", "$konkurranse", "$demo", "$tandem"]
                                }
                            },
                            "sum": {'$sum': '$sum'},

                        }
                }
            ]
        }
    }
}
