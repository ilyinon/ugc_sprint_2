from typing import Dict, List, Optional

import orjson
from pydantic import UUID4, BaseModel, Field, PositiveFloat


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(BaseModel):
    film_id: UUID4 = Field(...)
    rating: Optional[PositiveFloat] = None
    ratings: Optional[Dict[str, int]] = None


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
