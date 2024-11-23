import shutil

from fastapi import APIRouter, Depends, Body, UploadFile
from fastapi.responses import RedirectResponse
import starlette.status as status
from src.books.repo import BookRepo, book_repo
from src.books.models import Book
from pydantic import BaseModel, Field

from src.reviews.models import Review
from src.users.repo import user_repo

router = APIRouter(prefix='/reviews')


class SReview(BaseModel):
    book_id: int
    content: str


@router.post("/add")
def send_review(review: SReview):
    book = book_repo.load(review.book_id)
    review = Review(
        id=None,
        content=review.content,
        rating=5,
        book_id=review.book_id,
        user_id=1,
    )
    book.reviews.append(review)
    book_repo.save(book)
