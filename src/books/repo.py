from typing import List

from src.db import BookDB
from src.books.middleware import conv_book_to_db, conv_book_from_db
from src.books.models import Book
from src.db import RepoContext, repo_context
from sqlalchemy import Select, and_, or_, select


class BookRepo:
    def __init__(self, context: RepoContext) -> None:
        self.__context = context

    def load(self, id_: int) -> Book | None:
        with self.__context as session:
            book = session.execute(
                select(BookDB).where(BookDB.id == id_)
            ).scalars().first()
            if book:
                return conv_book_from_db(book)
            return None

    def load_all(self) -> List[Book] | None:
        with self.__context as session:
            books = session.execute(
                select(BookDB)
            ).scalars().all()
            if books is not None:
                return [conv_book_from_db(book) for book in books]
            return None

    def save(self, book: Book) -> int | None:
        with self.__context as session:
            db_book = conv_book_to_db(book)
            db_book = session.merge(db_book)
            session.add(db_book)
        return db_book.id

    def new(self) -> Book:
        book_model = Book(
            id=None,
            name="",
            author="",
            rating=5.0,
            genres=[],
            reviews=[],
        )
        book_model.id = self.save(book_model)
        return book_model

    def remove(self, id_):
        with self.__context as session:
            session.delete(session.get(BookDB, id_))


book_repo = BookRepo(repo_context())

