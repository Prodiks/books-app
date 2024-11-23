import os
from dataclasses import dataclass
from types import TracebackType
from typing import Type, Optional, List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker
from sqlalchemy import create_engine, ForeignKey
from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(DeclarativeBase):
    pass


class ReviewDB(Base):
    __tablename__ = 'reviews_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    rating: Mapped[float]
    book_id: Mapped[int] = mapped_column(ForeignKey('books_table.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users_table.id'))


class UserDB(Base):
    __tablename__ = 'users_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password: Mapped[str]
    reviews: Mapped[List[ReviewDB]] = relationship(
        cascade='save-update, merge, delete, delete-orphan'
    )


class BookDB(Base):
    __tablename__ = 'books_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    author: Mapped[str]
    rating: Mapped[float]
    genres: Mapped[str]
    reviews: Mapped[List[ReviewDB]] = relationship(
        cascade='save-update, merge, delete, delete-orphan'
    )


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


_settings = Settings()
_engine = None
_repo_context = None


def get_db_url():
    return (f"postgresql://{_settings.DB_USER}:{_settings.DB_PASSWORD}@"
            f"{_settings.DB_HOST}:{_settings.DB_PORT}/{_settings.DB_NAME}")


def get_sqlite_db_url() -> str:
    return f'sqlite:///books-app.db'


def get_auth_data():
    return {"secret_key": _settings.SECRET_KEY, "algorithm": _settings.ALGORITHM}


def db_create():
    global _engine
    global _repo_context
    _engine = create_engine(get_sqlite_db_url(), echo=False)
    Base.metadata.create_all(_engine)
    _repo_context = RepoContext(sessionmaker(_engine, expire_on_commit=False))


@dataclass
class RepoContext:
    sessionmaker: sessionmaker[Session]
    _session: Optional[Session] = None
    _nested_count: int = 0

    def __enter__(self) -> Session:
        if self._session is None:
            self._session = self.sessionmaker()
            self._session.begin()
        self._nested_count += 1
        return self._session

    def __exit__(
        self, exc_type: Type[BaseException], exc_value: BaseException, exc_tb: TracebackType | None
    ) -> None:
        if exc_type is None:
            if self._session and self._nested_count == 1:
                self._session.commit()
                self._session.close()
                self._session = None
            self._nested_count -= 1
        elif self._session:
            self._session.rollback()
            self._session = None
            self._nested_count = 0


def repo_context() -> RepoContext:
    if _repo_context is None:
        db_create()
    return _repo_context
