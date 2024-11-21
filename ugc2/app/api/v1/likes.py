import logging

import jwt
from core.config import ugc2_settings
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from service.users import UserService, get_users_service
from service.auth import AuthService, get_auth_service
from utils.token import verify_jwt

get_token = HTTPBearer(auto_error=False)

router = APIRouter()


@router.post(
    "/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add like to film",
)
async def add_like(
    film_id: str,
    access_token: str = Depends(get_token),
    user_service: UserService = Depends(get_users_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await user_service.add_like(await auth_service.verify_jwt(access_token), film_id)


@router.delete(
    "/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove like from film",
)
async def remove_like(
    film_id: str,
    access_token: str = Depends(get_token),
    user_service: UserService = Depends(get_users_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await user_service.delete_like(await auth_service.verify_jwt(access_token), film_id)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get likes of user",
)
async def get_likes(
    access_token: str = Depends(get_token),
    user_service: UserService = Depends(get_users_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await user_service.get_likes(await auth_service.verify_jwt(access_token))
