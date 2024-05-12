import datetime
import traceback

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.auth.auth_exceptions import InvalidToken, TokenExpired
from app.core.env_settings import env_settings
from app.models.user_model import User
from app.routes.user.user_dao import UserDAO


class AuthHandler:
    # security = HTTPBearer()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd: str, hashed_pwd: str):
        try:
            return self.pwd_context.verify(pwd, hashed_pwd)
        except Exception:
            print(traceback.format_exc())
            return False

    def encode_token(
        self,
        user_id: str,
        issued_at: datetime.datetime,
        expires_at: datetime.datetime,
    ) -> str:
        payload = {
            "iat": issued_at,
            "exp": expires_at,
            "user_id": user_id,
        }
        # print(payload)
        return jwt.encode(
            payload,
            env_settings.JWT_SECRET,
            algorithm=env_settings.JWT_ALG,
        )

    # This is useful when we don't storing any tokens into database
    def generate_access_token(
        self,
        user_id: str,
        issued_at: datetime.datetime = datetime.datetime.now(datetime.UTC),
        expires_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(minutes=env_settings.JWT_EXP),
    ):
        return self.encode_token(
            user_id=user_id,
            issued_at=issued_at,
            expires_at=expires_at,
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
            return payload
        except ExpiredSignatureError:
            # print("ExpiredSignatureError")
            raise TokenExpired()

        except JWTError:
            # print("JWTError")
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
        # Annotated[str, Depends(oauth2_scheme)
        user_dao: UserDAO = Depends(),
    ) -> User:
        # print("get_current_user called and token is ", token)
        decoded = self.decode_token(token)
        user_id: int | None = decoded.get("user_id")

        if user_id is None:
            raise InvalidToken()
        user = await user_dao.select_one(user_id=user_id)
        if user is None:
            raise InvalidToken()

        return user


auth_handler = AuthHandler()
