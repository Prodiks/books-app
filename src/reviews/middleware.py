from src.db import ReviewDB
from src.reviews.models import Review


def conv_review_to_db(review_model: Review) -> ReviewDB:
    return ReviewDB(
        id=review_model.id,
        content=review_model.content,
        rating=review_model.rating,
        book_id=review_model.book_id,
        user_id=review_model.user_id,
    )


def conv_review_from_db(review: ReviewDB) -> Review:
    return Review(
        id=review.id,
        content=review.content,
        rating=review.rating,
        book_id=review.book_id,
        user_id=review.user_id,
    )
