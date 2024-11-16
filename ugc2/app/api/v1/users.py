import jwt
from core.config import ugc2_settings
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from service.users import UserService, get_users_service

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


@router.post(
    "/users/bookmarks/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add film to bookmarks",
    tags=["Users"],
)
async def add_bookmark(
    film_id: str,
    user_service: UserService = Depends(get_users_service),
    payload: dict = Depends(verify_jwt),
):
    return await user_service.add_bookmark(payload["user_id"], film_id)


@router.delete(
    "/users/bookmarks/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove film from bookmarks",
    tags=["Users"],
)
async def remove_bookmark(
    film_id: str,
    user_service: UserService = Depends(get_users_service),
    payload: dict = Depends(verify_jwt),
):
    return await user_service.delete_bookmark(payload["user_id"], film_id)


@router.post(
    "/users/likes/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add film to user's liked",
    tags=["Users"],
)
async def add_like(
    film_id: str,
    user_service: UserService = Depends(get_users_service),
    payload: dict = Depends(verify_jwt),
    #    payload: dict = Depends(verify_jwt),
):
    return await user_service.like_film(payload["user_id"], film_id)


@router.delete(
    "/users/likes/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove film from user's liked",
    tags=["Users"],
)
async def remove_like(
    film_id: str,
    user_service: UserService = Depends(get_users_service),
    payload: dict = Depends(verify_jwt),
):
    return await user_service.remove_like_film(payload["user_id"], film_id)
