from typing import List

from pydantic import BaseModel

from src.reviews.models import Review


class User(BaseModel):
    id: int | None = None
    login: str
    password: str
    reviews: List[Review]
