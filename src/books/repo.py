from typing import List

from src.books.models import Book

books_ = [
    Book(
        id=1,
        name="name1",
        author="author1",
        rating=2,
        genres=["Фантастика", "Фэнтези"],
        reviews=[],
    ),
    Book(
        id=2,
        name="name2",
        author="author2",
        rating=1,
        genres=[],
        reviews=[],
    ),
    Book(
        id=2,
        name="name3",
        author="author3",
        rating=1,
        genres=[],
        reviews=[],
    ),
]


class DummyBookRepo:
    def __init__(self) -> None:
        self.__books: List[Book] = books_

    def load(self, id: int) -> Book:
        for book in self.__books:
            if book.id == id:
                return book

    def load_all(self) -> List[Book]:
        return self.__books

    def save(self, book: Book) -> None:
        self.__books.append(book)
