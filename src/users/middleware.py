from src.reviews.middleware import conv_review_to_db, conv_review_from_db
from src.db import UserDB
from src.users.models import User


def conv_user_to_db(user_model: User) -> UserDB:
    return UserDB(
        id=user_model.id,
        login=user_model.login,
        password=user_model.password,
        reviews=[conv_review_to_db(review) for review in user_model.reviews],
    )


def conv_user_from_db(user: UserDB) -> User:
    return User(
        id=user.id,
        login=user.login,
        password=user.password,
        reviews=[conv_review_from_db(review) for review in user.reviews],
    )
