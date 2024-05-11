from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth_handler import AuthHandler
from app.core.env_settings import env_settings
from app.data.data import users
from app.models.user_model import User, UserResponse

auth_handler = AuthHandler()

router = APIRouter()


# * POST
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> UserResponse:
    # print("login inside")
    user: User | None = next(
        (u for u in users if u.username == form_data.username), None
    )

    if not user:
        raise HTTPException(status_code=401, detail="invalid username and/or password")

    user.hashed_password = auth_handler.get_password_hash(user.password)
    is_password_correct = auth_handler.verify_password(
        form_data.password,
        user.hashed_password,
    )
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="invalid username and/or password")

    utc_now_time = datetime.now(UTC)
    token_exp_at = utc_now_time + timedelta(minutes=env_settings.JWT_EXP)
    token = auth_handler.encode_token(
        username=form_data.username,
        issued_at=utc_now_time,
        expires_at=token_exp_at,
    )

    # * Response required field "access_token", if this change then swagger /me route wont work
    user.access_token = token
    user.token_expires_at = token_exp_at

    # print(t.model_dump(exclude={"user": {"username", "password"}, "value": True}))
    return user


# * GET
@router.get("/me")
async def get_logged_in_user(
    user: User = Depends(auth_handler.get_current_user),
) -> UserResponse:
    return user


# * This aspects two parameters token and token_type,
# * we can also add additional data like in /login endpoint i passed user object
token_router = APIRouter()


@token_router.post("/token")
async def login_though_token(
    result=Depends(login),
):
    return result


# TODO * POST Register new user
