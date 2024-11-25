from functools import lru_cache

from core.config import ugc2_settings
from core.logger import fastapi_logger
from db.mongo import get_db
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.base import UserLike


class UserService:
    def __init__(self, db_client: AsyncIOMotorClient, database_name: str):
        self.db = db_client[database_name]
        self.collection = self.db[ugc2_settings.mongo_collection_users]

    async def add_like(self, user_id, film_id):
        user_like = await self.collection.find_one({"_id": user_id})

        if user_like.get("likes"):
            if film_id not in user_like["likes"]:

                user_like["likes"].append(film_id)

                await self.collection.update_one(
                    {"_id": user_id},
                    {"$set": {"likes": user_like["likes"]}},
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Film is already liked.",
                )
        else:
            user_like = UserLike(user_id=user_id, likes=[film_id])
            await self.collection.update_one(
                {"_id": user_id},
                {"$set": {"_id": user_id, "likes": [film_id]}},
                upsert=True,
            )
        return {"message": "Film liked successfully."}

    async def delete_like(self, user_id, film_id):

        user_like = await self.collection.find_one({"_id": user_id})

        if user_like and film_id in user_like["likes"]:
            user_like["likes"].remove(film_id)
            await self.collection.update_one(
                {"_id": user_id}, {"$set": {"likes": user_like["likes"]}}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="likes not found."
            )

    async def get_likes(self, user_id):

        user_like = await self.collection.find_one({"_id": user_id})
        fastapi_logger.info(f"user_like: {user_like}")
        if user_like:
            if user_like["likes"]:
                return user_like["likes"]

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found likes.",
        )

    async def rate_film(self, user_id, film_id, rating):
        user_rate = await self.collection.find_one({"_id": user_id})
        fastapi_logger.info(f"user_rate: {user_rate}")
        if user_rate:
            if film_id not in user_rate["ratings"]:
                user_rate["ratings"][film_id] = rating

                await self.collection.update_one(
                    {"_id": user_id},
                    {
                        "$set": {
                            "ratings": user_rate["ratings"],
                        }
                    },
                )
            else:
                return False
        else:
            fastapi_logger.info(f"film_id: {film_id}, ratings: {rating}")
            await self.collection.insert_one(
                {
                    "_id": user_id,
                    "ratings": {film_id: rating},
                }
            )
        return True


@lru_cache()
def get_users_service(db: AsyncIOMotorClient = Depends(get_db)) -> UserService:
    return UserService(db, ugc2_settings.mongo_db_name)
