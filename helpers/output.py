from flask import jsonify
from functools import wraps


def response(f):
    """ encrypt response """

    @wraps(f)
    def wrapper(*args, **kwargs):
        plain_json, error_code = f(*args, **kwargs)
        return jsonify(plain_json), error_code

    return wrapper

