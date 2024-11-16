from functools import lru_cache

from core.config import ugc2_settings
from motor.motor_asyncio import AsyncIOMotorClient


@lru_cache()
def get_db():
    db_client = AsyncIOMotorClient(ugc2_settings.mongo_dsn)
    return db_client
