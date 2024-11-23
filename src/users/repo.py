from typing import List

from src.db import RepoContext, repo_context
from src.db import UserDB
from src.users.middleware import conv_user_to_db, conv_user_from_db
from src.users.models import User
from sqlalchemy import Select, and_, or_, select


class UserRepo:
    def __init__(self, context: RepoContext) -> None:
        self.__context = context

    def load(self, id_: int) -> User | None:
        with self.__context as session:
            user = session.execute(
                select(UserDB).where(UserDB.id == id_)
            ).scalars().first()
        return conv_user_from_db(user)

    def load_by_login(self, login: str) -> User | None:
        with self.__context as session:
            user = session.execute(
                select(UserDB).where(UserDB.login == login)
            ).scalars().first()
            if user:
                return conv_user_from_db(user)
            return None

    def load_all(self) -> List[User]:
        with self.__context as session:
            users = session.execute(
                select(UserDB)
            ).scalars().all()
        if users:
            return [conv_user_from_db(user) for user in users]
        return None

    def save(self, user: User) -> None:
        with self.__context as session:
            session.add(conv_user_to_db(user))

    def new(self) -> User:
        user_model = User(
            id=None,
            login="",
            password="",
            reviews=[],
        )
        self.save(user_model)
        return user_model

    def remove(self, id_):
        with self.__context as session:
            session.delete(session.get(UserDB, id_))


user_repo = UserRepo(repo_context())
