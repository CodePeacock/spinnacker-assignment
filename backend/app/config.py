"""Configuration class for the application."""

import os

# load the environment variables using python-dotenv
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")


class Config:
    """
    Configuration class for the application.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): The URI for the database connection.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to enable or disable modification tracking.
        SECRET_KEY (str): The secret key used for encryption.
        JWT_ACCESS_LIFESPAN (dict): The lifespan of the access token.
        JWT_REFRESH_LIFESPAN (dict): The lifespan of the refresh token.
        SQLALCHEMY_ENGINE_OPTIONS (dict): Additional options for the SQLAlchemy engine.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://username:password@localhost/db_name"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    JWT_ACCESS_LIFESPAN = {"hours": 2}
    JWT_REFRESH_LIFESPAN = {"hours": 2}
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_timeout": 30,
        "pool_recycle": 1800,
        "max_overflow": 20,
    }
