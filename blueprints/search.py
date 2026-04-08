import requests
from settings import APP_INSTANCE
from eve.methods.get import get_internal
from ext.scf import LUNGO_HEADERS, LUNGO_URL
from flask import g, Blueprint, current_app as app, request, Response, abort, jsonify
from ext.app.eve_helper import eve_abort, eve_response
from ext.app.decorators import require_token
from blueprints.distinct import _get_field_contents, COLLECTIONS_WHITELIST

Search = Blueprint('Search binding to query builder', __name__, )

SEARCH_DEFINITION = {}
SEARCH_DEFINITION['fallskjerm_observations'] = {
    'sections': {
        'observation': {
            'label': 'Observasjon',
            'fields': {
                'type': {
                    'name': 'Type',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'fallskjerm.observation.types'},
                    '_default': True,
                    'options': []
                },
                'workflow.state': {
                    'name': 'Status',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'fallskjerm.observation.state'},
                    '_default': True,
                    'options': []
                },
                'when': {
                    'name': 'Når',
                    'type': 'date',
                    '_default': True
                },
                'discipline': {
                    'name': 'Klubb',
                    'type': 'category',
                    '_resolve_name': {'type': 'lungo',
                                      'path': 'organizations',
                                      'label_field': 'name'},  # description
                    '_default': True,
                    'options': []
                },
                # FLAGS
                'flags.insurance': {
                    'name': 'Forsikring flagget',
                    '_default': True,
                    'type': 'boolean'
                },
                'flags.aviation': {
                    'name': 'Fly involvert',
                    '_default': True,
                    'type': 'boolean'
                },
            }
        },
        'attributes': {
            'label': 'Attributter',
            'fields': {
                'components.attributes.reserve_ride': {
                    'name': 'Reservetrekk',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.aad_fire': {
                    'name': 'Nødåpner fyring',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.aad_rescue': {
                    'name': 'Nødåpner redning',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.packing_error': {
                    'name': 'Pakkefeil',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.gear_malfunction': {
                    'name': 'Feilfunksjon',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.damage': {
                    'name': 'Materiell skade',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.gear_failure': {
                    'name': 'Utstyrssvikt',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.rigger_error': {
                    'name': 'MK/MR feil',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.violation': {
                    'name': 'Regelbrudd',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.willful_violation': {
                    'name': 'Med vitende vilje',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.injury': {
                    'name': 'Personskade',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.death': {
                    'name': 'Død',
                    '_default': True,
                    'type': 'boolean'
                },
            },
        },
        'components': {
            'label': 'Forløpet',
            'fields': {

                'components.what': {
                    'name': 'Hva skjedde',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'components.where.at': {
                    'name': 'Hvor skjedde det',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'components.where.altitude': {
                    'name': 'I hvilken høyde skjedde det',
                    'type': 'number',
                    '_default': True
                }
            }
        },
        'involved': {
            'label': 'Involverte',
            'fields': {
                'involved.data.competences.type_id': {
                    'name': 'Kompetanser',
                    'type': 'category',
                    '_resolve_name': {'type': 'lungo',
                                      'path': 'competences/types',
                                      'label_field': 'title'},  # description
                    '_default': True,
                    'options': []
                },
                'involved.data.years_of_experience': {
                    'name': 'Erfaring i år',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.total_jumps': {
                    'name': 'Totalt antall hopp',
                    'type': 'number',
                    '_default': True
                },
                'involved.fu': {
                    'name': 'Farlig ukontrollert',
                    '_default': True,
                    'type': 'boolean'
                },
                'involved.ph': {
                    'name': 'Permanent hoppforbud',
                    '_default': True,
                    'type': 'boolean'
                },
                'involved.age': {
                    'name': 'Alder',
                    '_default': True,
                    'type': 'number'
                },
            }
        },
        'jump': {
            'label': 'Hoppet',
            'fields': {
                'involved.data.jump_type': {
                    'name': 'Hopptype',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'involved.data.activity': {
                    'name': 'Aktivitet',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'involved.data.altitude': {
                    'name': 'Utsprangshøyde',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.aircraft': {
                    'name': 'Fly',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
            }
        },
        'equipment': {
            'label': 'Utstyr',
            'fields': {
                'involved.data.gear.harness': {
                    'name': 'Seletøy',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    'options': []
                },
                'involved.data.gear.harness_experience': {
                    'name': 'Seletøy erfaring ',
                    'type': 'number',
                    '_resolve_name': {'type': 'value'},
                },
                'involved.data.gear.main_canopy': {
                    'name': 'Hovedskjerm',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'involved.data.gear.main_canopy_experience': {
                    'name': 'Hovedskjerm erfaring',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.gear.main_canopy_size': {
                    'name': 'Hoveskjerm størrelse',
                    'type': 'number',
                    '_default': True,
                },
                'involved.data.gear.reserve_canopy': {
                    'name': 'Reserve',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'involved.data.gear.reserve_canopy_size': {
                    'name': 'Reserve størrelse',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.gear.aad': {
                    'name': 'Nødåpner',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'involved.data.gear.other': {
                    'name': 'Annet',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
            },
        },
        'rating': {
            'label': 'Alvorlighetsgrad',
            'fields': {
                'rating.actual': {
                    'name': 'Faktisk alvorlighetsgrad',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'fallskjerm.observation.rating'},
                    '_default': True,
                    'options': []
                },
                'rating.potential': {
                    'name': 'Potensiell alvorlighetsgrad',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'fallskjerm.observation.rating'},
                    '_default': True,
                    'options': []
                },
                'rating._rating': {
                    'name': 'Kalkulert alvorlighetsgrad',
                    'type': 'number',
                    '_default': True
                },
            }
        },
        'weather': {
            'label': 'Været',
            'fields': {
                'weather.manual.clouds.base': {
                    'name': 'Skybase i fot',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.clouds.fog': {
                    'name': 'Tåke',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.hail': {
                    'name': 'Hagl',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.rain': {
                    'name': 'Regn',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.snow': {
                    'name': 'Snø',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.thunder': {
                    'name': 'Torden eller lyn',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.temp.altitude': {
                    'name': 'Temperatur i høyden',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.temp.ground': {
                    'name': 'Temperatur bakke',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.avg': {
                    'name': 'Middelvind',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.dir': {
                    'name': 'Vindretning',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.max': {
                    'name': 'Vind gusting',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.min': {
                    'name': 'Vind minimum',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.turbulence': {
                    'name': 'Turbulens',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.wind.gusting': {
                    'name': 'Vind guster',
                    '_default': True,
                    'type': 'boolean'
                },
            }
        }

    }

}
SEARCH_DEFINITION['hps_observations'] = {
    'sections': {
        'observation': {
            'label': 'Observasjon',
            'fields': {
                'type': {
                    'name': 'Type',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'hps.observation.types'},
                    '_default': True,
                    'options': []
                },
                'workflow.state': {
                    'name': 'Status',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'hps.observation.state'},
                    '_default': True,
                    'options': []
                },
                'when': {
                    'name': 'Når',
                    'type': 'date',
                    '_default': True
                },
                'discipline': {
                    'name': 'Klubb',
                    'type': 'category',
                    '_resolve_name': {'type': 'lungo',
                                      'path': 'organizations',
                                      'label_field': 'name'},  # description
                    '_default': True,
                    'options': []
                },
                # FLAGS
                'flags.insurance': {
                    'name': 'Forsikring flagget',
                    '_default': True,
                    'type': 'boolean'
                },
                'flags.aviation': {
                    'name': 'Fly involvert',
                    '_default': True,
                    'type': 'boolean'
                },
            }
        },
        'attributes': {
            'label': 'Attributter',
            'fields': {
                'eccairs2.attributes.highestDamage.value': {
                    '_resolve_name': {'type': 'e5x_choices', 'key': 'Occurrence.HighestDamage', 'label_field': 'label'},
                    'name': 'Occurrence HighestDamage',
                    '_default': True,
                    'type': 'category',
                    'options': []
                },
                'components.attributes.aad_fire': {
                    'name': 'Nødåpner fyring',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.aad_rescue': {
                    'name': 'Nødåpner redning',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.packing_error': {
                    'name': 'Pakkefeil',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.gear_malfunction': {
                    'name': 'Feilfunksjon',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.damage': {
                    'name': 'Materiell skade',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.gear_failure': {
                    'name': 'Utstyrssvikt',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.rigger_error': {
                    'name': 'MK/MR feil',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.violation': {
                    'name': 'Regelbrudd',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.willful_violation': {
                    'name': 'Med vitende vilje',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.injury': {
                    'name': 'Personskade',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.death': {
                    'name': 'Død',
                    '_default': True,
                    'type': 'boolean'
                },
            },
        },
        'components': {
            'label': 'Forløpet',
            'fields': {

                'components.what': {
                    'name': 'Hva skjedde',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'components.where.at': {
                    'name': 'Hvor skjedde det',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'components.where.altitude': {
                    'name': 'I hvilken høyde skjedde det',
                    'type': 'number',
                    '_default': True
                }
            }
        },
        'involved': {
            'label': 'Involverte',
            'fields': {
                'involved.data.competences.type_id': {
                    'name': 'Kompetanser',
                    'type': 'category',
                    '_resolve_name': {'type': 'lungo',
                                      'path': 'competences/types',
                                      'label_field': 'title'},  # description
                    '_default': True,
                    'options': []
                },
                'involved.data.years_of_experience': {
                    'name': 'Erfaring i år',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.total_flights': {
                    'name': 'Totalt antall turer',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.total_hours': {
                    'name': 'Totalt antall timer',
                    'type': 'number',
                    '_default': True
                },
                'involved.age': {
                    'name': 'Alder',
                    '_default': True,
                    'type': 'number'
                },
            }
        },
        'flight': {
            'label': 'Flyturen',
            'fields': {}
        },
        'equipment': {
            'label': 'Utstyr',
        },
        'rating': {
            'label': 'Alvorlighetsgrad',
            'fields': {
                'rating.actual': {
                    'name': 'Faktisk alvorlighetsgrad',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'hps.observation.rating'},
                    '_default': True,
                    'options': []
                },
                'rating.potential': {
                    'name': 'Potensiell alvorlighetsgrad',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'hps.observation.rating'},
                    '_default': True,
                    'options': []
                },
                'rating._rating': {
                    'name': 'Kalkulert alvorlighetsgrad',
                    'type': 'number',
                    '_default': True
                },
            }
        },
        'weather': {
            'label': 'Været',
            'fields': {
                'weather.manual.clouds.base': {
                    'name': 'Skybase i fot',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.clouds.fog': {
                    'name': 'Tåke',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.hail': {
                    'name': 'Hagl',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.rain': {
                    'name': 'Regn',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.snow': {
                    'name': 'Snø',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.thunder': {
                    'name': 'Torden eller lyn',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.temp.altitude': {
                    'name': 'Temperatur i høyden',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.temp.ground': {
                    'name': 'Temperatur bakke',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.avg': {
                    'name': 'Middelvind',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.dir': {
                    'name': 'Vindretning',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.max': {
                    'name': 'Vind gusting',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.min': {
                    'name': 'Vind minimum',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.turbulence': {
                    'name': 'Turbulens',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.wind.gusting': {
                    'name': 'Vind guster',
                    '_default': True,
                    'type': 'boolean'
                },
            }
        }

    }

}

SEARCH_DEFINITION['motorfly_observations'] = {
    'sections': {
        'observation': {
            'label': 'Observasjon',
            'fields': {
                'type': {
                    'name': 'Type',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'motorfly.observation.types'},
                    '_default': True,
                    'options': []
                },
                'workflow.state': {
                    'name': 'Status',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'motorfly.observation.state'},
                    '_default': True,
                    'options': []
                },
                'when': {
                    'name': 'Når',
                    'type': 'date',
                    '_default': True
                },
                'discipline': {
                    'name': 'Klubb',
                    'type': 'category',
                    '_resolve_name': {'type': 'lungo',
                                      'path': 'organizations',
                                      'label_field': 'name'},  # description
                    '_default': True,
                    'options': []
                },
                # FLAGS
                'flags.insurance': {
                    'name': 'Forsikring flagget',
                    '_default': True,
                    'type': 'boolean'
                },
                'flags.aviation': {
                    'name': 'Fly involvert',
                    '_default': True,
                    'type': 'boolean'
                },
            }
        },
        'attributes': {
            'label': 'Attributter',

            'fields': {
                'occurrence.attributes.occurrenceCategory.value': {
                    '_resolve_name': {'type': 'e5x_choices', 'key': 'Occurrence.OccurrenceCategory', 'label_field': 'label'},
                    'name': 'Occurrence Category',
                    '_default': True,
                    'type': 'category',
                    'options': []
                },
                'components.attributes.violation': {
                    'name': 'Regelbrudd',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.willful_violation': {
                    'name': 'Med vitende vilje',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.injury': {
                    'name': 'Personskade',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.death': {
                    'name': 'Død',
                    '_default': True,
                    'type': 'boolean'
                },
            },
        },
        'components': {
            'label': 'Forløpet',
            'fields': {
                'components.what': {
                    'name': 'Hva skjedde',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'components.where.at': {
                    'name': 'Hvor skjedde det',
                    'type': 'category',
                    '_resolve_name': {'type': 'value'},
                    '_default': True,
                    'options': []
                },
                'components.where.altitude': {
                    'name': 'I hvilken høyde skjedde det',
                    'type': 'number',
                    '_default': True
                }
            }
        },
        'involved': {
            'label': 'Involverte',
            'fields': {
                'involved.data.competences.type_id': {
                    'name': 'Kompetanser',
                    'type': 'category',
                    '_resolve_name': {'type': 'lungo',
                                      'path': 'competences/types',
                                      'label_field': 'title'},  # description
                    '_default': True,
                    'options': []
                },
                'involved.data.years_of_experience': {
                    'name': 'Erfaring i år',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.total_flights': {
                    'name': 'Totalt antall turer',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.total_hours': {
                    'name': 'Totalt antall timer',
                    'type': 'number',
                    '_default': True
                },
                'involved.age': {
                    'name': 'Alder',
                    '_default': True,
                    'type': 'number'
                },
            }
        },
        'flight': {
            'label': 'Flyturen',
            'fields': {}
        },
        'equipment': {
            'label': 'Utstyr',
        },
        'rating': {
            'label': 'Alvorlighetsgrad',
            'fields': {
                'rating.actual': {
                    'name': 'Faktisk alvorlighetsgrad',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'motorfly.observation.rating'},
                    '_default': True,
                    'options': []
                },
                'rating.potential': {
                    'name': 'Potensiell alvorlighetsgrad',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'motorfly.observation.rating'},
                    '_default': True,
                    'options': []
                },
                'rating._rating': {
                    'name': 'Kalkulert alvorlighetsgrad',
                    'type': 'number',
                    '_default': True
                },
            }
        },
        'weather': {
            'label': 'Været',
            'fields': {
                'weather.manual.clouds.base': {
                    'name': 'Skybase i fot',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.clouds.fog': {
                    'name': 'Tåke',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.hail': {
                    'name': 'Hagl',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.rain': {
                    'name': 'Regn',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.snow': {
                    'name': 'Snø',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.thunder': {
                    'name': 'Torden eller lyn',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.temp.altitude': {
                    'name': 'Temperatur i høyden',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.temp.ground': {
                    'name': 'Temperatur bakke',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.avg': {
                    'name': 'Middelvind',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.dir': {
                    'name': 'Vindretning',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.max': {
                    'name': 'Vind gusting',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.min': {
                    'name': 'Vind minimum',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.turbulence': {
                    'name': 'Turbulens',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.wind.gusting': {
                    'name': 'Vind guster',
                    '_default': True,
                    'type': 'boolean'
                },
            }
        }

    }
}

SEARCH_DEFINITION['modellfly_observations'] = {
    'sections': {
        'observation': {
            'label': 'Observasjon',
            'fields': {
                'type': {
                    'name': 'Type',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'modellfly.observation.types'},
                    '_default': True,
                    'options': []
                },
                'workflow.state': {
                    'name': 'Status',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'modellfly.observation.state'},
                    '_default': True,
                    'options': []
                },
                'when': {
                    'name': 'Når',
                    'type': 'date',
                    '_default': True
                },
                'discipline': {
                    'name': 'Klubb',
                    'type': 'category',
                    '_resolve_name': {'type': 'lungo',
                                      'path': 'organizations',
                                      'label_field': 'name'},  # description
                    '_default': True,
                    'options': []
                },
                # FLAGS
                'flags.insurance': {
                    'name': 'Forsikring flagget',
                    '_default': True,
                    'type': 'boolean'
                },
                'flags.aviation': {
                    'name': 'Fly involvert',
                    '_default': True,
                    'type': 'boolean'
                },
            }
        },
        'attributes': {
            'label': 'Attributter',
            'fields': {
                'eccairs2.attributes.highestDamage.value': {
                    '_resolve_name': {'type': 'e5x_choices', 'key': 'Occurrence.HighestDamage', 'label_field': 'label'},
                    'name': 'Occurrence HighestDamage',
                    '_default': True,
                    'type': 'category',
                    'options': []

                },
                'eccairs2.attributes.occurrenceCategory.value': {
                    '_resolve_name': {'type': 'e5x_choices', 'key': 'Occurrence.OccurrenceCategory', 'label_field': 'label'},
                    'name': 'Occurrence Category',
                    '_default': True,
                    'type': 'category',
                    'options': []
                },
                'components.attributes.damage': {
                    'name': 'Materiell skade',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.violation': {
                    'name': 'Regelbrudd',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.willful_violation': {
                    'name': 'Med vitende vilje',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.injury': {
                    'name': 'Personskade',
                    '_default': True,
                    'type': 'boolean'
                },
                'components.attributes.death': {
                    'name': 'Død',
                    '_default': True,
                    'type': 'boolean'
                },
            },
        },
        'involved': {
            'label': 'Involverte',
            'fields': {
                'involved.data.competences.type_id': {
                    'name': 'Kompetanser',
                    'type': 'category',
                    '_resolve_name': {'type': 'lungo',
                                      'path': 'competences/types',
                                      'label_field': 'title'},  # description
                    '_default': True,
                    'options': []
                },
                'involved.data.years_of_experience': {
                    'name': 'Erfaring i år',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.total_flights': {
                    'name': 'Totalt antall turer',
                    'type': 'number',
                    '_default': True
                },
                'involved.data.total_hours': {
                    'name': 'Totalt antall timer',
                    'type': 'number',
                    '_default': True
                },
                'involved.age': {
                    'name': 'Alder',
                    '_default': True,
                    'type': 'number'
                },
            }
        },
        'flight': {
            'label': 'Flyturen',
            'fields': {}
        },
        'equipment': {
            'label': 'Utstyr',
        },
        'rating': {
            'label': 'Alvorlighetsgrad',
            'fields': {
                'rating.actual': {
                    'name': 'Faktisk alvorlighetsgrad',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'hps.observation.rating'},
                    '_default': True,
                    'options': []
                },
                'rating.potential': {
                    'name': 'Potensiell alvorlighetsgrad',
                    'type': 'category',
                    '_resolve_name': {'type': 'config', 'path': 'hps.observation.rating'},
                    '_default': True,
                    'options': []
                },
                'rating._rating': {
                    'name': 'Kalkulert alvorlighetsgrad',
                    'type': 'number',
                    '_default': True
                },
            }
        },
        'weather': {
            'label': 'Været',
            'fields': {
                'weather.manual.clouds.base': {
                    'name': 'Skybase i fot',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.clouds.fog': {
                    'name': 'Tåke',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.hail': {
                    'name': 'Hagl',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.rain': {
                    'name': 'Regn',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.snow': {
                    'name': 'Snø',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.clouds.thunder': {
                    'name': 'Torden eller lyn',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.temp.altitude': {
                    'name': 'Temperatur i høyden',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.temp.ground': {
                    'name': 'Temperatur bakke',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.avg': {
                    'name': 'Middelvind',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.dir': {
                    'name': 'Vindretning',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.max': {
                    'name': 'Vind gusting',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.min': {
                    'name': 'Vind minimum',
                    'type': 'number',
                    '_default': True
                },
                'weather.manual.wind.turbulence': {
                    'name': 'Turbulens',
                    '_default': True,
                    'type': 'boolean'
                },
                'weather.manual.wind.gusting': {
                    'name': 'Vind guster',
                    '_default': True,
                    'type': 'boolean'
                },
            }
        }

    }
}
"""
    # Flags
    'flags',
    # Rating
    'rating',
        # Location
    'location',
        # Været,
    'weather',
        # Tiltak
    'actions.local',
    'actions.central',
        # Root
    'id',
    '_id',
    'when',
    'club',
    'discipline',
    'tags',
    'type',
    """


def _resolve_names_from_collection(collection, field):
    pass


def _get_value_by_dot_path(d, path):
    out = path.split('.', 1)
    key = out[0]
    if len(out) > 1:
        path = out[1]
        return _get_value_by_dot_path(d[key], path)
    else:
        try:
            # default return key if not resolved!
            app.logger.debug(f'Just err now {key} {type(key)}, {d}')
            # app.logger.debug('Dict', key, d.get(key, {}).get('label', 'Ukjent felt {}'.format(key)))

            if isinstance(d, list):
                app.logger.debug(f'Lista {[x.get('label', path) for x in d if x.get('value', 0) == int(key) - 1]}')  # if x.get('value', None) == key])
                return [x.get('label', path) for x in d if x.get('value', 0) == int(key) - 1][0]
                # if x.get('label', None) not in [None, ''] [x.get('label', path) for x in d if x.get('value', None) == key][0]

            return d.get(key, {}).get('label', 'Ukjent felt {}'.format(key))
        except:
            pass

    return 'Ukjent'


def _get_options_from_config(path, values):
    options = []
    # get config!
    result, _, _, status, _ = get_internal('app_config', **{'environment': APP_INSTANCE})
    app.logger.debug(f'CONFIG RESULT {result}, {status}')
    if status == 200 and '_items' in result and len(result['_items']) == 1:
        for value in values:

            if value not in [None, 'null']:
                app.logger.debug(f'Value {value}')
                options.append({
                    'name': _get_value_by_dot_path(result['_items'][0], '{}.{}'.format(path, value)),
                    'value': value
                })
        app.logger.debug(options)
        return options
    return []


def _get_options_from_collection(collection, query_field, name_field, values):
    app.logger.debug(f'---> {collection}, {query_field}, {name_field}, {values}')
    options = []
    for value in values:
        r, _, _, status, _ = get_internal(collection, **{query_field: value})
        app.logger.debug(f'[[[[[[[[[[[]]]]]]]]]]]]] {r}')
        if status == 200:
            options.append({'name': r[name_field], 'value': value})

    return options


def _get_options_from_e5x_choices(key, values):
    options = []
    query = {'rit_version': '4.1.0.3', 'key': key, 'id': {'$in': values}}
    r, _, _, status, _ = get_internal('e5x_choices', **query)
    if status == 200:
        app.logger.debug(r)
        for item in r.get('_items', []):
            options.append({'name': item['label'], 'value': item['id']})

    return options


def _lungo_item(path, item_id, name_field):
    resp = requests.get('{}/{}/{}'.format(LUNGO_URL, path, item_id),
                        # params={'projection': projection},
                        headers=LUNGO_HEADERS,
                        verify=app.config.get('REQUESTS_VERIFY', True))
    if resp.status_code == 200:
        return 200, resp.json()
    else:
        app.logger.debug(resp.text)
    return resp.status_code, None


def _get_options_from_lungo(path, query_field, name_field, values):
    options = []
    for value in values:
        status, item = _lungo_item(path, value, name_field)
        if status == 200:
            options.append({'name': item[name_field], 'value': value})

    return options


@Search.route("/definition/sections/<string:collection>", methods=['GET'])
@require_token()
def get_query_builder_definition_sections(collection):
    if collection in COLLECTIONS_WHITELIST:
        sections = [{'section': key, 'label': SEARCH_DEFINITION[collection]['sections'][key]['label']} for key in
                    SEARCH_DEFINITION[collection]['sections'].keys()]

        return eve_response(sections, 200)

    return abort(403)


@Search.route("/definition/<string:collection>", methods=['GET'])
@Search.route("/definition/<string:collection>/<string:section>", methods=['GET'])
@require_token()
def get_query_builder_definition(collection, section=None):
    # get from search_definition
    # iterate and fill
    # get all types from distinct if type == 'category' => {options: []}
    # resolve names for all categories (from config?) {name, value}

    if collection in COLLECTIONS_WHITELIST:
        try:
            if section is not None:
                fields = SEARCH_DEFINITION[collection]['sections'][section]['fields']
            else:
                fields = SEARCH_DEFINITION[collection]['fields']
        except Exception as e:
            app.logger.debug(f'ERROR {e}')
            abort(403)

        for field, definition in fields.items():
            app.logger.debug(f'FIELD {field}')
            if definition['type'] == 'category' and '_resolve_name' in definition and len(definition['options']) == 0:
                # Resolve from client config file by path
                if definition['_resolve_name']['type'] == 'config':
                    app.logger.debug('CONFIG!')
                    status, values = _get_field_contents(collection, field)
                    app.logger.debug(f'[[[[ {collection}, {field}, {status}, {values}')
                    if status == 200:
                        fields[field]['options'] = _get_options_from_config(definition['_resolve_name']['path'], values)
                # From resolving manually to a collection type
                elif definition['_resolve_name']['type'] == 'e5x_choices':
                    # '_resolve_name': {'type': 'e5x_choices', 'key': 'Occurrence.OccurrenceCategory', 'label_field': 'label'},
                    # Get all values used in the collection for this field, then query the e5x_choices collection for each value to get the label
                    status, values = _get_field_contents(collection, field)
                    app.logger.debug(f'[[[[ E5X {collection}, {field}, {status}, {values}')
                    if status == 200:
                        values = [int(float(x)) for x in values]
                        fields[field]['options'] = _get_options_from_e5x_choices(definition['_resolve_name']['key'], values)
                elif definition['_resolve_name']['type'] == 'collection':
                    status, values = _get_field_contents(collection, field)
                    app.logger.debug(f'[[[[ {field}, {status}, {values}')
                    if status == 200:
                        fields[field]['options'] = _get_options_from_collection(
                            definition['_resolve_name']['collection'],
                            field.rpartition(',')[-1] or field,
                            definition['_resolve_name']['label_field'],
                            values
                        )
                elif definition['_resolve_name']['type'] == 'lungo':
                    status, values = _get_field_contents(collection, field)
                    app.logger.debug(f'[[[[ {field}, {status}, {values}')
                    if status == 200:
                        fields[field]['options'] = _get_options_from_lungo(
                            definition['_resolve_name']['path'],
                            field.rpartition(',')[-1] or field,
                            definition['_resolve_name']['label_field'],
                            values
                        )

                else:  # definition['_resolve_name']['type'] == 'value':
                    status, values = _get_field_contents(collection, field)
                    if status == 200:
                        for value in values:
                            try:
                                value = value.strip()
                                if value == '':
                                    continue
                            except:
                                pass

                            if value is None:
                                continue

                            fields[field]['options'].append({'name': value, 'value': value})

        default = {
            'condition': 'and',
            'rules': [{'field': x, 'operator': 'in' if fields[x]['type'] == 'category' else '='} for x in fields.keys()
                      if
                      fields[x].get('_default', False) is True]
        }

        return eve_response({'definition': {'fields': fields}, 'default': default}, 200)

    return abort(403)
