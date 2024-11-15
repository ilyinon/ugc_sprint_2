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
from schemas.base import Film, Rating

security = HTTPBearer()


client = AsyncIOMotorClient()

db = client.bookmark_db
collection = db.films


router = APIRouter()


# Увеличение количества лайков
@router.post(
    "/films/{film_id}/like",
    status_code=status.HTTP_200_OK,
    summary="Update amount of likes to film",
    tags=["Films likes"],
)
async def like_film(film_id: str):
    return like_film(film_id)


# Увеличение количества дизлайков
@router.post(
    "/films/{film_id}/dislike",
    status_code=status.HTTP_200_OK,
    summary="Update amount of dislikes to film",
    tags=["Films dislikes"],
)
async def dislike_film(film_id: str):
    return dislike_film(film_id)


# Получение информации о фильме
@router.get(
    "/films/{film_id}",
    response_model=Film,
    summary="Get details about film",
    tags=["Film details"],
)
async def get_film(film_id: str):
    return get_film_detail(film_id)


# Добавление пользовательской оценки
@router.post(
    "/films/{film_id}/rate",
    status_code=status.HTTP_200_OK,
    summary="Rate film",
    tags=["Film's rating"],
)
async def rate_film(film_id: str, rating: Rating):
    return rate_film(film_id, rating)


# Получение информации о фильме с средней оценкой
@router.get(
    "/films/{film_id}",
    response_model=Film,
    summary="Get average film rate",
    tags=["Film's rating"],
)
async def get_film(film_id: str):
    return get_film_rate(film_id)
