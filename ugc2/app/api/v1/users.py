import json

import jwt
from fastapi import APIRouter, Depends, Security
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from schemas.base import Bookmark, UserBookmark, Like, UserLike
from service.users import UserService, get_users_service

security = HTTPBearer()


router = APIRouter()


# async def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
#     """
#     Verify user's token and get its payload.
#     """
#     try:
#         payload = jwt.decode(
#             credentials.credentials,
#             ugc_settings2.authjwt_secret_key,
#             algorithms=[ugc2_settings.authjwt_algorithm],
#         )
#         return payload
#     except jwt.exceptions.DecodeError:
#         raise HTTPException(status_code=401, detail="Invalid JWT token")
#     except jwt.exceptions.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="JWT token expired")


@router.post(
    "/users/{user_id}/bookmarks/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add film to bookmarks",
    tags=["Bookmarks"],
)
async def add_bookmark(
    user_id: str, film_id: str, user_service: UserService = Depends(get_users_service)
):
    return await user_service.add_bookmark(user_id, film_id)


@router.delete(
    "/users/{user_id}/bookmarks/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove film from bookmarks",
    tags=["Bookmarks"],
)
async def remove_bookmark(
    user_id: str, film_id: str, user_service: UserService = Depends(get_users_service)
):
    return await user_service.delete_bookmark(user_id, film_id)


@router.post(
    "/users/{user_id}/likes/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add film to user's liked",
    tags=["User liked films"],
)
async def add_like(
    user_id: str,
    film_id: str,
    user_service: UserService = Depends(get_users_service),
    #    payload: dict = Depends(verify_jwt),
):
    return await user_service.like_film(user_id, film_id)


@router.delete(
    "/users/{user_id}/likes/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove film from user's liked",
    tags=["User liked films"],
)
async def remove_like(
    user_id: str, film_id: str, user_service: UserService = Depends(get_users_service)
):
    return await user_service.remove_like_film(user_id, film_id)
