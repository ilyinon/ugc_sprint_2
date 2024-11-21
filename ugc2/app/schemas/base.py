from typing import List, Optional

import orjson
from pydantic import BaseModel, Field, UUID4


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(BaseModel):
    film_id: UUID4 = Field(...)
    likes: int = 0
    dislikes: int = 0
    ratings: Optional[List[str]] = None


class FilmRating(BaseModel):
    rating: float


class Bookmark(BaseModel):
    film_id: UUID4 = Field(...)


class UserBookmark(BaseModel):
    user_id: UUID4
    bookmarks: List[UUID4] = []

class UserLike(BaseModel):
    user_id: UUID4
    likes: List[UUID4] = []

class Like(BaseModel):
    film_id: UUID4 = Field(...)


class UserLike(BaseModel):
    user_id: UUID4
    film_ids: List[UUID4] = []
