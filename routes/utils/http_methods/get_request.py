from helpers.validations import token_required
from helpers.output import response
from flask import request


class GetRequest:
    def __init__(self, table_model, result, results):
        self.__table_model = table_model
        self.__result = result
        self.__results = results

    @token_required()
    @response
    def get(self, current_user, id=None):
        """Method http GET

        Args:
            current_user (object): Contains the data of the logged in user
            id (int, optional): ID registration. Defaults to None.

        Returns:
            json: many or one registry
            http error: corresponding code http error
        """
        if id:
            return self.get_by_id(current_user, id)

        elif "page" in request.args.keys():
            page = int(request.args.get("page", type=int, default=1))
            per_page = int(request.args.get("size", type=int, default=10))
            return self.get_pagination(page, per_page, current_user)

        return self.get_all(current_user)

    def get_all(self, current_user: object):
        registrys_list = self.__table_model.all(current_user)
        return {"results": self.__results.dump(registrys_list)}, 200

    def get_by_id(self, current_user: object, id: int):
        one_registry = self.__table_model.get_by_id(id, current_user)
        return self.__result.dump(one_registry), 200

    def get_pagination(self, page: int, per_page: int, current_user: object):
        paginar = self.__table_model.paginate(page, per_page, current_user)
        return {
            "results": self.__results.dump(paginar.items),
            "total-pages": paginar.pages,
        }, 200
