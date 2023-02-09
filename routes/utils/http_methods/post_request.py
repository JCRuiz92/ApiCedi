import jwt
import datetime
from flask import request, abort
from flask import current_app as app
from helpers.validations import token_required, validate_json
from helpers.output import response


class PostRequest:
    def __init__(self, table_model, result, login_config):
        self.login_config = login_config
        self.__table_model = table_model
        self.login = validate_json(login_config.schema())(self.login)
        self.add = validate_json(result)(self.add)
        self.__result = result

    def post(self):
        """ Method http GET """
        rute = str(request.url_rule)
        if rute.find("login") != -1:
            return self.login()
        return self.add()

    @response
    def login(self):
        """Create new session and execute post action(optional)

        Returns:
            token (json): jwt
        """
        return self.login_config.create_token(self.__table_model, request.json)

    @token_required()
    @response
    def add(self, current_user):
        """Add new record

        Args:
            current_user (object): Contains the data of the logged in user

        Returns:
            json: registry created
        """
        new_registry = self.__table_model(request.json, current_user)
        new_registry.save()
        return self.__result.dump(new_registry), 201
