from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from service.auth import AuthService, get_auth_service
from service.films import FilmService, get_films_service
from service.users import UserService, get_users_service

get_token = HTTPBearer(auto_error=False)

router = APIRouter()


@router.post(
    "/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Rate film",
)
async def rate_film(
    film_id: str,
    rating: int,
    access_token: str = Depends(get_token),
    user_service: UserService = Depends(get_users_service),
    auth_service: AuthService = Depends(get_auth_service),
    film_service: FilmService = Depends(get_films_service),
):
    if await user_service.rate_film(
        await auth_service.verify_jwt(access_token), film_id, rating
    ) and await film_service.rate_film(
        await auth_service.verify_jwt(access_token), film_id, rating
    ):
        return {"message": "Film rated successfully."}


@router.get(
    "/{film_id}",
    status_code=status.HTTP_200_OK,
    summary="Get film's rate",
)
async def get_film_rate(
    film_id: str, film_service: FilmService = Depends(get_films_service)
):
    return await film_service.get_film_rate(film_id)
