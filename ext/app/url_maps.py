"""
    Custom url route mappings
    =========================
    
    This is a collection of url maps for Flask applications.
    Flask do not have any native map for mongodb ObjectId (Eve uses regex)
    
    
    Usage:
    
    app.url_map.converters['objectid'] = ObjectIDConverter
    then you can
    @app.route('/users/<objectid:user_id>')
    
"""
from flask import Flask
from werkzeug.routing import BaseConverter, ValidationError
from itsdangerous import base64_encode, base64_decode
from bson.objectid import ObjectId
from bson.errors import InvalidId


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(value)

        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return str(value)


class Base64ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(base64_decode(value))

        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return base64_encode(value.binary).decode('utf-8')


class RegexConverter(BaseConverter):
    """ Enable standard regex on flask endpoints
        Already registered on eve, so should work on flask endpoints
    """

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
