import jwt
from core.config import ugc2_settings
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.base import FilmRating
from service.films import FilmService, get_films_service

security = HTTPBearer()


router = APIRouter()


async def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify user's token and get its payload.
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            ugc2_settings.authjwt_secret_key,
            algorithms=[ugc2_settings.authjwt_algorithm],
        )
        return payload
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token expired")


# Увеличение количества лайков
@router.post(
    "/films/{film_id}/like",
    status_code=status.HTTP_200_OK,
    summary="Update amount of likes to film",
    tags=["Films"],
)
async def like_film(
    film_id: str,
    film_service: FilmService = Depends(get_films_service),
    payload: dict = Depends(verify_jwt),
):
    return await film_service.like_film(film_id)


# Увеличение количества дизлайков
@router.post(
    "/films/{film_id}/dislike",
    status_code=status.HTTP_200_OK,
    summary="Update amount of dislikes to film",
    tags=["Films"],
)
async def dislike_film(
    film_id: str,
    film_service: FilmService = Depends(get_films_service),
    payload: dict = Depends(verify_jwt),
):
    return await film_service.dislike_film(film_id)


# Добавление пользовательской оценки
@router.post(
    "/films/{film_id}/rate",
    status_code=status.HTTP_200_OK,
    summary="Rate film",
    tags=["Films"],
)
async def rate_film(
    film_id: str,
    rating: int,
    film_service: FilmService = Depends(get_films_service),
    payload: dict = Depends(verify_jwt),
):
    return await film_service.rate_film(film_id, rating)


# Получение информации о фильме с средней оценкой
@router.get(
    "/films/{film_id}",
    response_model=FilmRating,
    summary="Get average film rate",
    tags=["Films"],
)
async def get_film(
    film_id: str,
    film_service: FilmService = Depends(get_films_service),
    payload: dict = Depends(verify_jwt),
):
    return await film_service.get_film_rate(film_id)
