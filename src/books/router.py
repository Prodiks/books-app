from fastapi import APIRouter, Depends, Body

from src.books.repo import DummyBookRepo
from src.books.models import Book

router = APIRouter(prefix='/books', tags=['Работа с книгами'])

repo = DummyBookRepo()


@router.get("/", summary="Получить все книги")
def get_all_books() -> list[Book]:
    return repo.load_all()


@router.get("/new")
def get_new_book() -> Book:
    return repo.new()


@router.put("/update")
def update_book(data=Body()) -> Book:
    book = Book(
            id=int(data["id"]),
            name=data["name"],
            author=data["author"],
            rating=float(data["rating"]),
            genres=str(data["genres"]).split(',')
        )
    repo.save(book)
    return book



@router.get("/{id}", summary="Получить книгу по id")
def get_book_by_id(id: int) -> Book:
    print(repo.load_all())
    return repo.load(id)
