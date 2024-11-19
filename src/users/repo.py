from typing import List

from src.users.models import User

_users = [
    User(
        id=1,
        login="log1",
        password="_",
    ),
    User(
        id=5,
        login="log5",
        password="_",
    ),
]


class DummyUserRepo:
    def __init__(self) -> None:
        self.__users: List[User] = _users

    def load(self, id: int) -> User:
        print("LOAD ID: ", id)
        for user in self.__users:
            if user.id == id:
                return user

    def load_by_login(self, login: str) -> User:
        print("LOAD LOGIN: ", login)
        for user in self.__users:
            if user.login == login:
                print("FINDED: ", user)
                return user

    def load_all(self) -> List[User]:
        return self.__users

    def save(self, user: User) -> None:
        print("SAVE: ", user)
        if not user.id:
            if self.__users:
                max_id = max(self.__users, key=lambda user: user.id).id
            else:
                max_id = 0
            user.id = max_id + 1
            self.__users.append(user)
        else:
            for i, b in enumerate(self.__users):
                if b.id == user.id:
                    self.__users[i] = user
                    return

    def new(self) -> User:
        user = User(
            name="",
            author="",
            rating=5,
            genres=[],
            reviews=[],
        )
        self.save(user)
        return user

    def remove(self, id):
        for i, b in enumerate(self.__users):
            if b.id == id:
                del self.__users[i]


repo = DummyUserRepo()
