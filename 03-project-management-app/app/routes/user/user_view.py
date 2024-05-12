from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from app.models.user_model import LoginResponseModel, User, UserInput, UserResponse
from app.routes.user.user_dao import UserDAO

router = APIRouter()


# token_router = APIRouter()
# container = DependencyContainer()


# * POST
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_dao: UserDAO = Depends(),
) -> LoginResponseModel:
    # print("login inside")
    # print(form_data.username)
    user = await user_dao.select_from_email(form_data.username)

    if not user:
        # print("User not found")
        raise HTTPException(status_code=404, detail="user not found")

    # print("db password :: " + user.password)
    # print("input password :: " + form_data.password)
    from app.auth.auth_handler import auth_handler

    is_password_correct = auth_handler.verify_password(
        form_data.password,
        str(user.hashed_password),
    )
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="invalid username and/or password")

    # if not user.is_verified:
    #     raise HTTPException(
    #         status_code=401,
    #         detail="One more step, please verify your email that we sent you to your mail",
    #     )

    assert user.id is not None
    access_token = auth_handler.generate_access_token(user_id=user.id.__str__())

    # print("access_token_str :: ", access_token)

    return LoginResponseModel(
        access_token=access_token,
        token_type="Bearer",
        user=UserResponse(**user.__dict__),
    )


@router.post("/register")
async def register(
    new_user: UserInput,
    user_dao: UserDAO = Depends(),
) -> LoginResponseModel:
    user = await user_dao.select_from_email(new_user.email)

    # all_users: list[User] = await user_dao.select_all()
    # db_user = next((employee for employee in all_users if employee.username == new_user.username), None)

    if user:
        # if db_employee.is_verified == False:
        #     # TODO: parse issued and exp time
        #     token = auth_handler.auth_handler.encode_token(db_employee.id)  # type: ignore
        #     await send_email_verification_mail(name=db_employee.name, to_email=db_employee.email, token=token)
        #     raise HTTPException(
        #         status_code=401,
        #         detail="Already register once, please verify your email from email that we have just sent you and then after you will be able to login",
        #     )
        # else:
        raise HTTPException(
            status_code=401,
            detail="email already exist, please try to login with same.",
        )
    from app.auth.auth_handler import auth_handler

    assert new_user.password
    hashed_password = auth_handler.get_hash_password(
        new_user.password.get_secret_value()
    )
    new_user.password = SecretStr(hashed_password)

    db_user = await user_dao.insert(
        User(
            **new_user.model_dump(exclude={"password"}),
            **{
                "id": uuid4(),
                "hashed_password": hashed_password,
            },
        )
    )

    # TODO: make this background task
    # await send_email_verification_mail(name=db_user.name, to_email=db_user.email, token=token)

    assert db_user.id is not None
    access_token = auth_handler.generate_access_token(user_id=db_user.id.__str__())

    # print("access_token :: ", access_token)

    return LoginResponseModel(
        access_token=access_token,
        token_type="Bearer",
        user=UserResponse(**db_user.__dict__),
    )


# TODO: Make Verify user API
