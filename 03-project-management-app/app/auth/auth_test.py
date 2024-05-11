# %%
import datetime

# from exceptions import InvalidToken, TokenExpired
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.env_settings import env_settings


def encode_token(
    user_id: int, issued_at: datetime.datetime, expires_at: datetime.datetime
) -> str:
    payload = {
        "iat": issued_at,
        "exp": expires_at,
        "user_id": user_id,
    }
    return jwt.encode(payload, env_settings.JWT_SECRET, algorithm=env_settings.JWT_ALG)


def decode_token(token: str):
    try:
        # print(token)
        payload = jwt.decode(
            token=token,
            key=env_settings.JWT_SECRET,
            # access_token=
            # options={"verify_signature": False},
            algorithms=[env_settings.JWT_ALG],
        )
        # print(payload) # {'exp': 1674022037, 'iat': 1673417237, 'user_id': 1} # Where 1 is user_id
        return payload["user_id"]
    except ExpiredSignatureError:
        print("ExpiredSignatureError")
        # raise TokenExpired()

    except JWTError:
        print("JWTError")
        # raise InvalidToken()


# %%
encoded_token_value = encode_token(
    user_id=111,
    issued_at=datetime.datetime.now(datetime.UTC),
    expires_at=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
)
# %%
print(encoded_token_value)

# %%
decode_token(encoded_token_value)

# %%
import datetime

datetime.datetime.now(datetime.UTC)


# %%
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(pwd, hashed_pwd):
    return pwd_context.verify(pwd, hashed_pwd)


# %%
get_password_hash(password="Admin@123")
# %%
verify_password(
    pwd="Admin@123",
    hashed_pwd="$2b$12$tC0.5iIZ8hqH4H2hK4JiK.YWz6mcIT6tCjY1GLHkKbMFGIq7bMDNC",
)
# %%
