import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UgcSettings2(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    project_name: str = "ugc2"

    mongo_user: str = "root"
    mongo_pass: str = "example"
    mongo_port: int = 27017
    mongo_host: str = "mongodb"

    mongo_db_name: str = "ugc"
    mongo_collection_film: str = "films"
    mongo_collection_users: str = "users"

    authjwt_secret_key: str = "example"
    authjwt_algorithm: str = "HS256"

    log_level: bool = False

    sentry_enable: bool = True
    sentry_dsn: str = "https://c6e15651de424b3321b89771c9ec00bb@o4508310740598784.ingest.de.sentry.io/4508310743941200"
    sentry_traces_sample_rate: float = 1.0
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.

    @property
    def mongo_dsn(self):
        return f"mongodb://{self.mongo_user}:{self.mongo_pass}@{self.mongo_host}:{self.mongo_port}"


ugc2_settings = UgcSettings2()


def get_config():
    return UgcSettings2()
