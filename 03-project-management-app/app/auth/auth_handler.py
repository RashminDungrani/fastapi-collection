import datetime

from fastapi import HTTPException, Security
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.auth.auth_exceptions import InvalidToken, TokenExpired
from app.core.env_settings import env_settings
from app.data.data import users
from app.models.user_model import User


class AuthHandler:
    # security = HTTPBearer()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(
        self, username: str, issued_at: datetime.datetime, expires_at: datetime.datetime
    ) -> str:
        payload = {
            "iat": issued_at,
            "exp": expires_at,
            "username": username,
        }
        return jwt.encode(
            payload,
            env_settings.JWT_SECRET,
            algorithm=env_settings.JWT_ALG,
        )

    def decode_token(self, token: str):
        try:
            # print(f"TOKEN :: {token}")
            payload = jwt.decode(
                token=token,
                key=env_settings.JWT_SECRET,
                algorithms=[env_settings.JWT_ALG],
            )
            # print(payload) # {'exp': 1674022037, 'iat': 1673417237, 'user_id': 1} # Where 1 is user_id
            return payload["username"]
        except ExpiredSignatureError:
            print("ExpiredSignatureError")
            raise TokenExpired()

        except JWTError:
            print("JWTError")
            raise InvalidToken()
        except Exception as e:
            raise HTTPException(
                status_code=401, detail=f"Exception in decode token: {e}"
            )

    def auth_wrapper(self, token: str = Security(oauth2_scheme)):
        return self.decode_token(token)

    async def get_current_user(
        self,
        token: str = Security(oauth2_scheme),
    ) -> User:
        # print("get_current_user called and token is {}", token)
        username = self.decode_token(token)

        if username is None:
            raise InvalidToken()

        user: User | None = next(
            (u for u in users if u.username == username),
            None,
        )

        if user is None:
            raise InvalidToken()

        return user
