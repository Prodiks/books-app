from operator import attrgetter
from typing import List

from src.books.models import Book
from src.reviews.models import Review

books_ = [
    Book(
        id=1,
        name="name11",
        author="author1",
        rating=2,
        genres=["Фантастика", "Фэнтези"],
        reviews=[
            Review(
                id=1,
                content="Некоторый крутой отзыв",
                rating=4.5,
            ),
            Review(
                id=2,
                content="Второй некоторый крутой отзыв",
                rating=3.5,
            )
        ],
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
        id=3,
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
        if not book.id:
            if self.__books:
                max_id = max(self.__books, key=lambda book: book.id).id
            else:
                max_id = 0
            book.id = max_id + 1
            self.__books.append(book)
        else:
            for i, b in enumerate(self.__books):
                if b.id == book.id:
                    self.__books[i] = book
                    return

    def new(self) -> Book:
        book = Book(
            name="",
            author="",
            rating=5,
            genres=[],
            reviews=[],
        )
        self.save(book)
        return book

    def remove(self, id):
        for i, b in enumerate(self.__books):
            if b.id == id:
                del self.__books[i]
