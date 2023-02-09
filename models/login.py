from . import ma, Schema
from marshmallow import validate


class LoginSchema(Schema):
    email = ma.Email(required=True)
    password = ma.Str(validate=validate.Length(min=8), required=True)
