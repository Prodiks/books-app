from typing import List
from pydantic import BaseModel

from src.reviews.models import Review


class Book(BaseModel):
    id: int | None = None
    name: str
    author: str
    rating: float
    genres: List[str]
    reviews: List[Review]