from src.db import BookDB
from src.books.models import Book
from src.reviews.middleware import conv_review_to_db, conv_review_from_db


def conv_book_to_db(book_model: Book) -> BookDB:
    return BookDB(
        id=book_model.id,
        name=book_model.name,
        author=book_model.author,
        rating=book_model.rating,
        genres=",".join(book_model.genres),
        reviews=[conv_review_to_db(review) for review in book_model.reviews],
    )


def conv_book_from_db(book_db: BookDB) -> Book:
    return Book(
        id=book_db.id,
        name=book_db.name,
        author=book_db.author,
        rating=book_db.rating,
        genres=book_db.genres.split(","),
        reviews=[conv_review_from_db(review) for review in book_db.reviews],
    )
