from fastapi import APIRouter, Depends

from src.books.repo import DummyBookRepo
from src.books.models import Book

router = APIRouter(prefix='/books', tags=['Работа с книгами'])

repo = DummyBookRepo()

@router.get("/", summary="Получить все книги")
def get_all_books() -> list[Book]:
    return repo.load_all()


@router.get("/{id}", summary="Получить книгу по id")
def get_book_by_id(id: int) -> list[Book]:
    return repo.load(id)
