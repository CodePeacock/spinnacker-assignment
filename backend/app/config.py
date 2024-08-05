import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://username:password@localhost/db_name"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    JWT_ACCESS_LIFESPAN = {"hours": 24}
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_timeout": 30,
        "pool_recycle": 1800,
        "max_overflow": 20,
    }
    JWT_REFRESH_LIFESPAN = {"days": 30}
