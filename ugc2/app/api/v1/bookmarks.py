import logging

import jwt
from core.config import ugc2_settings
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from service.bookmarks import BookmarkService, get_bookmarks_service

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
    "/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add film to bookmarks",
)
async def add_bookmark(
    film_id: str,
    user_service: BookmarkService = Depends(get_bookmarks_service),
    payload: dict = Depends(verify_jwt),
):
    user_id = payload["user_id"]
    logging.info(f"{user_id} is adding {film_id} to bookmarks")

    return await user_service.add_bookmark(user_id, film_id)


@router.delete(
    "/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove film from bookmarks",
)
async def remove_bookmark(
    film_id: str,
    user_service: BookmarkService = Depends(get_bookmarks_service),
    payload: dict = Depends(verify_jwt),
):
    user_id = payload["user_id"]
    logging.info(f"{user_id} is deleting {film_id} to bookmarks")
    return await user_service.delete_bookmark(payload["user_id"], film_id)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get list of bookmarks",
)
async def get_bookmark(
    user_service: BookmarkService = Depends(get_bookmarks_service),
    payload: dict = Depends(verify_jwt),
):
    user_id = payload["user_id"]
    logging.info(f"Get list of {user_id} bookmarks")
    return await user_service.get_bookmark(payload["user_id"])
