from core.logger import fastapi_logger


from core.config import ugc2_settings
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from service.bookmarks import BookmarkService, get_bookmarks_service
from utils.token import verify_jwt
from service.auth import AuthService, get_auth_service

get_token = HTTPBearer(auto_error=False)


router = APIRouter()



@router.post(
    "/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add film to bookmarks",
)
async def add_bookmark(
    film_id: str,
    access_token: str = Depends(get_token),
    user_service: BookmarkService = Depends(get_bookmarks_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    fastapi_logger.info(f"get the following {access_token}")
    user_id = await auth_service.verify_jwt(access_token)


    return await user_service.add_bookmark(user_id, film_id)


@router.delete(
    "/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove film from bookmarks",
)
async def remove_bookmark(
    film_id: str,
    access_token: str = Depends(get_token),
    user_service: BookmarkService = Depends(get_bookmarks_service),
    auth_service: AuthService = Depends(get_auth_service),

):
    user_id = await auth_service.verify_jwt(access_token)
    fastapi_logger.info(f"{user_id} removes {film_id} from bookmarks")
    return await user_service.delete_bookmark(user_id, film_id)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get list of bookmarks",
)
async def get_bookmark(
    access_token: str = Depends(get_token),
    user_service: BookmarkService = Depends(get_bookmarks_service),
    payload: dict = Depends(verify_jwt),
    auth_service: AuthService = Depends(get_auth_service),

):
    user_id = await auth_service.verify_jwt(access_token)
    fastapi_logger.info(f"Get list of {user_id} bookmarks")
    return await user_service.get_bookmark(user_id)
