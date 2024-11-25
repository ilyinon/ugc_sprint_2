from functools import lru_cache

from core.config import ugc2_settings
from core.logger import fastapi_logger
from db.mongo import get_db
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.base import Film


class FilmService:
    def __init__(self, db_client: AsyncIOMotorClient, database_name: str):
        self.db = db_client[database_name]
        self.collection = self.db[ugc2_settings.mongo_collection_film]

    async def rate_film(self, user_id, film_id, rating):

        film_rating = await self.collection.find_one({"_id": film_id})
        fastapi_logger.info(f"film_rating: {film_rating}")
        if film_rating:
            if user_id not in film_rating["ratings"]:
                film_rating["ratings"][user_id] = rating

                all_amount = len(film_rating["ratings"].keys())
                all_rating = 0
                for user in film_rating["ratings"].keys():
                    all_rating += film_rating["ratings"][user]

                average_rating = all_rating / all_amount
                await self.collection.update_one(
                    {"_id": film_id},
                    {
                        "$set": {
                            "ratings": film_rating["ratings"],
                            "rating": average_rating,
                        }
                    },
                )
            else:
                return False
        else:
            fastapi_logger.info(f"film_id: {film_id}, ratings: {rating}")
            film_rating = Film(film_id=film_id, ratings={user_id: rating})
            await self.collection.insert_one(
                {"_id": film_id, "ratings": {user_id: rating}, "rating": rating}
            )

        return True

    async def get_film_rate(self, film_id):

        film_rating = await self.collection.find_one({"_id": film_id})
        fastapi_logger.info(f"film_rating: {film_rating}")
        if film_rating:
            if film_rating.get("rating"):
                return film_rating["rating"]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film doesn't have rating yet",
        )


@lru_cache()
def get_films_service(db: AsyncIOMotorClient = Depends(get_db)) -> FilmService:
    return FilmService(db, ugc2_settings.mongo_db_name)
