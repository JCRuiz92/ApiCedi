
"""Application configuration."""
import os
from models.table_example import TableExample


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("APP_SECRET", "secret-key")  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
    EGINE_URI = "mysql://root:" + os.environ["PASSMARIA"] + "@localhost"
    # * EGINE_URI = 'mysql://root:@localhost'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TABLE_VALIDATE_TOKEN = TableExample
    CORS_ORIGIN_WHITELIST = [
        "http://0.0.0.0:4100",
        "http://localhost:4100",
        "http://0.0.0.0:8000",
        "http://localhost:8000",
        "http://0.0.0.0:4200",
        "http://localhost:4200",
        "http://0.0.0.0:4000",
        "http://localhost:4000",
        "http://0.0.0.0:5000",
        "http://localhost:5000",
    ]


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"
    DEBUG = False
    DB_NAME = "example"
    SQLALCHEMY_DATABASE_URI = f"{Config.EGINE_URI}/{DB_NAME}"


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True
    DB_NAME = "example"
    SQLALCHEMY_DATABASE_URI = f"{Config.EGINE_URI}/{DB_NAME}"
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    DB_NAME = "TestExample"
    SQLALCHEMY_DATABASE_URI = f"{Config.EGINE_URI}/{DB_NAME}"
