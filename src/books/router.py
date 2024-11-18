import shutil

from fastapi import APIRouter, Depends, Body, UploadFile
from fastapi.responses import RedirectResponse
import starlette.status as status
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


@router.put("/")
def update_book(data=Body()) -> Book:
    book = Book(
        id=int(data["id"]),
        name=data["name"],
        author=data["author"],
        rating=1.,
        genres=str(data["genres"]).split(','),
        reviews=[]
    )
    repo.save(book)
    return book


@router.post("/upload_image")
def upload_image(file: UploadFile, id: int) -> RedirectResponse:
    with open(f"static/images/{id}.webp", "wb+") as photo_obj:
        shutil.copyfileobj(file.file, photo_obj)
    return RedirectResponse(
        f'/pages/books/{id}',
        status_code=status.HTTP_302_FOUND)


@router.get("/{id}", summary="Получить книгу по id")
def get_book_by_id(id: int) -> Book:
    return repo.load(id)

@router.delete("/{id}")
def delete_book(id: int) -> Book:
    b = repo.load(id)
    repo.remove(id)
    return b
