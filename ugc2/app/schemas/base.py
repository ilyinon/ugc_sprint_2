from typing import List, Optional

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(BaseModel):
    film_id: str = Field(..., example="36eab1fb-47b3-4866-bc07-7db766e8de3e")
    likes: int = 0
    dislikes: int = 0
    ratings: Optional[List[str]] = None


class FilmRating(BaseModel):
    rating: float


class Bookmark(BaseModel):
    film_id: str = Field(..., example="film_123")


class UserBookmark(BaseModel):
    user_id: str
    film_ids: List[str] = []


class Like(BaseModel):
    film_id: str = Field(..., example="film_123")


class UserLike(BaseModel):
    user_id: str
    film_ids: List[str] = []
