import jwt
from core.config import ugc2_settings
from fastapi.exceptions import HTTPException
from functools import lru_cache



class AuthService:
    def __init__(self):
        pass


    async def verify_jwt(self, token):
        """
        Verify user's token and get its payload.
        """
        try:
            payload = jwt.decode(
                token.credentials,
                ugc2_settings.authjwt_secret_key,
                algorithms=[ugc2_settings.authjwt_algorithm],
            )
            return payload["user_id"]
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid JWT token")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="JWT token expired")



@lru_cache()
def get_auth_service() -> AuthService:

    return AuthService()