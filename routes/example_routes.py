from . import example
from models.table_example import TableExample, TableExample_Schema
from routes.utils.create_routes import create_endpoints

create_endpoints(
    example,
    "example",
    TableExample,
    TableExample_Schema,
    login_endpoint=True
)
