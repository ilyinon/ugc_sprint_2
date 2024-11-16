from functools import lru_cache

from core.config import ugc2_settings
from db.mongo import get_db
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.base import Film


class FilmService:
    def __init__(self, db_client: AsyncIOMotorClient, database_name: str):
        self.db = db_client[database_name]
        self.collection = self.db[ugc2_settings.mongo_collection_film]

    async def _create_film_if_not_exist(self, film_id):
        if not await self.collection.find_one({"film_id": film_id}):
            film = Film(film_id=film_id)
            await self.collection.insert_one(film.dict())

    async def like_film(self, film_id):
        await self._create_film_if_not_exist(film_id)

        result = await self.collection.update_one(
            {"film_id": film_id}, {"$inc": {"likes": 1}}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )
        return {"message": "Like added."}

    async def dislike_film(self, film_id):
        await self._create_film_if_not_exist(film_id)

        result = await self.collection.update_one(
            {"film_id": film_id}, {"$inc": {"dislikes": 1}}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )
        return {"message": "Dislike added."}

    async def rate_film(self, film_id, rating):
        await self._create_film_if_not_exist(film_id)

        result = await self.collection.update_one(
            {"film_id": film_id}, {"$push": {"ratings": rating}}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )
        return {"message": "Rating added."}

    async def get_film_rate(self, film_id):
        film = await self.collection.find_one({"film_id": film_id})
        if not film:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Film not found."
            )

        # Вычисление средней оценки
        ratings = film.get("ratings", [])
        if ratings:
            return {"rating": sum(ratings) / len(ratings)}
        return None


@lru_cache()
def get_films_service(db: AsyncIOMotorClient = Depends(get_db)) -> FilmService:
    return FilmService(db, ugc2_settings.mongo_db_name)
