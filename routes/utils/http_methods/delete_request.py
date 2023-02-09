from helpers.validations import token_required
from helpers.output import response


class DeleteRequest:
    def __init__(self, table_model, result):
        self.__table_model = table_model
        self.__result = result

    @token_required()
    @response
    def delete(self, current_user, id):
        """Delete record

        Args:
            current_user (object): Contains the data of the logged in user
            id (int, optional): ID registration

        Returns:
            json: deleted record
        """
        registry_delete = self.__table_model.get_by_id(id, current_user)
        registry_delete.delete(current_user)
        return self.__result.dump(registry_delete), 200
