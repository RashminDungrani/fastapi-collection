from app.models.user_model import User

users: list[User] = [
    User(
        username="admin",
        password="Admin@123",
        disabled=False,
        hashed_password=None,
    )
]
