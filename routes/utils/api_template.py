from flask.views import MethodView
from flask import current_app as app
from models import Model, Schema
from routes.utils.http_methods.get_request import GetRequest
from routes.utils.http_methods.post_request import PostRequest
from routes.utils.http_methods.put_request import PutRequest
from routes.utils.http_methods.delete_request import DeleteRequest
from config.login_config import LoginConfig


class MethodsApi(MethodView, GetRequest, PostRequest, PutRequest, DeleteRequest):
    """ Class for control to endpoints """

    def __init__(
        self, table_model: Model, table_schema: Schema, login_config: LoginConfig = None
    ):
        """Class for http methods

        Args:
            table_model (Model): sqlalchemy model
            table_schema (Schema): marshmallow schema
            login_config (LoginConfig): login config
        """
        result = table_schema()
        results = table_schema(many=True)
        if not login_config.key:
            login_config.key = app.config["SECRET_KEY"]
        GetRequest.__init__(self, table_model, result, results)
        PostRequest.__init__(self, table_model, result, login_config)
        PutRequest.__init__(self, table_model, result)
        DeleteRequest.__init__(self, table_model, result)
