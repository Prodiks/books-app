from typing import List
from pydantic import BaseModel


class Review(BaseModel):
    id: int | None = None
    content: str
    rating: float
    book_id: int | None = None
    user_id: int | None = None
