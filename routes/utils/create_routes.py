from routes.utils.api_template import MethodsApi
from config.login_config import LoginConfig


def create_endpoints(
    blueprint,
    noun,
    table_model,
    table_schema,
    login_endpoint=False,
    login_config=LoginConfig(),
    endpoints=[],
):
    """Create routes standars

    Args:
        blueprint (object): blueprint or object flask app
        noun (str): noun to create endpoints and method view name.
        table_model (Model): sqlalchemy model.
        table_schema (Schema): marshmallow schema.
        login_endpoint (bool, optional): Create login endpoint. Defaullt to False.
        login_config (dict, optional): receives configuration parameters to login.
        endpoints (list, optional): List to endpoints ([['/url', ['GET']]]). Default generate endpoints with noun.
    Examples:
        basic usage:
            create_endpoints(
                table_model=SomeModel,
                table_schema=SomeSchema,
                blueprint=some_blueprint,
                noun="v1/somenoun",
                login_endpoint=True)

        customize endpoints:
            create_endpoints(
                table_model=SomeModel,
                table_schema=SomeSchema,
                blueprint=some_blueprint,
                noun="v1/somenoun",
                endpoints=[['/api/v1/somenoun', ['GET','POST']])
    """
    view_func = MethodsApi.as_view(f"{noun}_api", table_model, table_schema, login_config)

    endpoint_list = endpoints if endpoints else get_endpoints(noun, login_endpoint)
    for i in endpoint_list:
        blueprint.add_url_rule(i[0], methods=i[1], view_func=view_func)


def get_endpoints(noun: str, login: bool) -> list:
    endpoint_list = [
        [f"/api/{noun}/", ["POST", "GET"]],
        [f"/api/{noun}/<int:id>", ["GET", "PUT", "DELETE"]],
    ]
    if login:
        endpoint_list.insert(0, [f"/api/{noun}/login", ["POST"]])
    return endpoint_list

