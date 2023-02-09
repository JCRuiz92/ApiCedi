from flask import request
from helpers.validations import token_required, validate_json
from helpers.output import response


class PutRequest:
    def __init__(self, table_model, result):
        self.__result = result
        self.__table_model = table_model
        self.put = validate_json(result)(self.put)

    @token_required()
    @response
    def put(self, current_user, id):
        """Edit record

        Args:
            current_user (object): Contains the data of the logged in user
            id (int, optional): ID registration

        Returns:
            json: edited record
        """
        registry_update = self.__table_model.get_by_id(id, current_user)
        registry_update.changes(request.json, current_user)
        registry_update.save()
        return self.__result.dump(registry_update), 200
