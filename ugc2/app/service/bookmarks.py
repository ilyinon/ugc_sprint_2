from functools import lru_cache

from core.config import ugc2_settings
from core.logger import fastapi_logger
from db.mongo import get_db
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.base import UserBookmark, UserLike


class BookmarkService:
    def __init__(self, db_client: AsyncIOMotorClient, database_name: str):
        self.db = db_client[database_name]
        self.collection = self.db[ugc2_settings.mongo_collection_users]

    async def add_bookmark(self, user_id, film_id):

        user_bookmark = await self.collection.find_one({"_id": user_id})
        fastapi_logger.info(f"user_bookmark: {user_bookmark}")
        if user_bookmark.get("bookmarks"):
            if film_id not in user_bookmark["bookmarks"]:
                user_bookmark["bookmarks"].append(film_id)
                await self.collection.update_one(
                    {"_id": user_id},
                    {"$set": {"bookmarks": user_bookmark["bookmarks"]}},
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Film already bookmarked.",
                )
        else:
            user_bookmark = UserBookmark(user_id=user_id, bookmarks=[film_id])
            await self.collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "bookmarks": [
                            film_id,
                        ]
                    }
                },
            )

        return {"message": "Bookmark added successfully."}

    async def delete_bookmark(self, user_id, film_id):

        user_bookmark = await self.collection.find_one({"_id": user_id})

        if user_bookmark and film_id in user_bookmark["bookmarks"]:
            user_bookmark["bookmarks"].remove(film_id)
            await self.collection.update_one(
                {"_id": user_id}, {"$set": {"bookmarks": user_bookmark["bookmarks"]}}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found."
            )

    async def get_bookmark(self, user_id):

        user_bookmark = await self.collection.find_one({"_id": user_id})
        fastapi_logger.info(f"user_bookmark: {user_bookmark}")
        if user_bookmark:
            if user_bookmark["bookmarks"]:
                return user_bookmark["bookmarks"]

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found bookmarks.",
        )

    async def like_film(self, user_id, film_id):

        user_like = await self.collection.find_one({"_id": user_id})

        if user_like:
            if film_id not in user_like["film_ids"]:
                user_like["film_ids"].append(film_id)
                await self.collection.update_one(
                    {"_id": user_id}, {"$set": {"film_ids": user_like["film_ids"]}}
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Film already liked.",
                )
        else:
            user_like = UserLike(user_id=user_id, film_ids=[film_id])
            await self.collection.insert_one(user_like.dict())

        return {"message": "Like added successfully."}

    async def remove_like_film(self, user_id, film_id):

        user_like = await self.collection.find_one({"_id": user_id})

        if user_like and film_id in user_like["film_ids"]:
            user_like["film_ids"].remove(film_id)
            await self.collection.update_one(
                {"_id": user_id}, {"$set": {"film_ids": user_like["film_ids"]}}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like not found."
            )


@lru_cache()
def get_bookmarks_service(db: AsyncIOMotorClient = Depends(get_db)) -> BookmarkService:
    return BookmarkService(db, ugc2_settings.mongo_db_name)
