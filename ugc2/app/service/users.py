from functools import lru_cache
from db.mongo import get_db
from fastapi import HTTPException, status, Depends
from schemas.base import UserBookmark, UserLike
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import ugc2_settings


class UserService:
    def __init__(self, db_client: AsyncIOMotorClient, database_name: str):
        self.db = db_client[database_name]

    async def add_bookmark(self, user_id, film_id):
        collection = self.db[ugc2_settings.mongo_collection_bookmark]
        user_bookmark = await collection.find_one({"user_id": user_id})

        if user_bookmark:
            if film_id not in user_bookmark["film_ids"]:
                user_bookmark["film_ids"].append(film_id)
                await collection.update_one(
                    {"user_id": user_id},
                    {"$set": {"film_ids": user_bookmark["film_ids"]}},
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Film already bookmarked.",
                )
        else:
            user_bookmark = UserBookmark(user_id=user_id, film_ids=[film_id])
            await collection.insert_one(user_bookmark.dict())

        return {"message": "Bookmark added successfully."}

    async def delete_bookmark(self, user_id, film_id):
        collection = self.db[ugc2_settings.mongo_collection_bookmark]

        user_bookmark = await collection.find_one({"user_id": user_id})

        if user_bookmark and film_id in user_bookmark["film_ids"]:
            user_bookmark["film_ids"].remove(film_id)
            await collection.update_one(
                {"user_id": user_id}, {"$set": {"film_ids": user_bookmark["film_ids"]}}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found."
            )

    async def like_film(self, user_id, film_id):
        collection = self.db[ugc2_settings.mongo_collection_like]

        user_like = await collection.find_one({"user_id": user_id})

        if user_like:
            if film_id not in user_like["film_ids"]:
                user_like["film_ids"].append(film_id)
                await collection.update_one(
                    {"user_id": user_id}, {"$set": {"film_ids": user_like["film_ids"]}}
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Film already likeed.",
                )
        else:
            user_like = UserLike(user_id=user_id, film_ids=[film_id])
            await collection.insert_one(user_like.dict())

        return {"message": "Like added successfully."}

    async def remove_like_film(self, user_id, film_id):
        collection = self.db[ugc2_settings.mongo_collection_like]

        user_like = await collection.find_one({"user_id": user_id})

        if user_like and film_id in user_like["film_ids"]:
            user_like["film_ids"].remove(film_id)
            await collection.update_one(
                {"user_id": user_id}, {"$set": {"film_ids": user_like["film_ids"]}}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like not found."
            )


@lru_cache()
def get_users_service(db: AsyncIOMotorClient = Depends(get_db)) -> UserService:
    return UserService(db, ugc2_settings.mongo_db_name)
