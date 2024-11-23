from typing import List

from src.db import BookDB
from src.books.middleware import conv_book_to_db, conv_book_from_db
from src.books.models import Book
from src.db import RepoContext, repo_context
from sqlalchemy import Select, and_, or_, select


class BookRepo:
    def __init__(self, context: RepoContext) -> None:
        self.__context = context

    def load(self, id_: int) -> Book:
        with self.__context as session:
            book = session.execute(
                select(BookDB).where(BookDB.id == id_)
            ).scalars().first()
            return conv_book_from_db(book)

    def load_all(self) -> List[Book]:
        with self.__context as session:
            books = session.execute(
                select(BookDB)
            ).scalars().all()
            return [conv_book_from_db(book) for book in books]

    def save(self, book: Book) -> None:
        with self.__context as session:
            db_book = conv_book_to_db(book)
            db_book = session.merge(db_book)
            session.add(db_book)

    def new(self) -> Book:
        book_model = Book(
            id=None,
            name="",
            author="",
            rating=5.0,
            genres=[],
            reviews=[],
        )
        self.save(book_model)
        return book_model

    def remove(self, id_):
        with self.__context as session:
            session.delete(session.get(BookDB, id_))

book_repo = BookRepo(repo_context())

