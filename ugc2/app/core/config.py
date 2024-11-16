import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))

logging_config.dictConfig(LOGGING)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UgcSettings2(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    project_name: str = "ugc2"

    mongo_user: str = "root"
    mongo_pass: str = "example"
    mongo_port: int = 27017
    mongo_host: str = "mongodb"

    mongo_db_name: str = "ugc"
    mongo_collection_bookmark: str = "user_bookmark"
    mongo_collection_like: str = "user_likes"
    mongo_collection_film: str = "film"

    authjwt_secret_key: str = "example"
    authjwt_algorithm: str = "HS256"

    log_level: bool = False

    @property
    def mongo_dsn(self):
        return f"mongodb://{self.mongo_user}:{self.mongo_pass}@{self.mongo_host}:{self.mongo_port}"


ugc2_settings = UgcSettings2()


def get_config():
    return UgcSettings2()
