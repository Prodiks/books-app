from typing import List
from pydantic import BaseModel


class Book(BaseModel):
    id: int
    name: str
    author: str
    rating: float
    genres: List[str]
