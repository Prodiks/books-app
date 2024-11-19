from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.books.models import Book
from src.books.router import get_all_books, get_book_by_id, get_new_book

router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory='src/templates')


@router.get('/books')
def get_books_html(request: Request, books=Depends(get_all_books)):
    return templates.TemplateResponse(name='books.html',
                                      context={'request': request, 'books': books})


@router.get('/books/new')
def get_new_books_html(request: Request, book=Depends(get_new_book)):
    return templates.TemplateResponse(name='book.html',
                                      context={'request': request, 'book': book})

@router.get('/books/{id}')
def get_book_html(request: Request, book=Depends(get_book_by_id)):
    return templates.TemplateResponse(name='book.html',
                                      context={'request': request, 'book': book})

@router.get('/register')
async def get_register_html(request: Request):
    return templates.TemplateResponse(name='register_form.html', context={'request': request})


@router.get('/login')
async def get_login_html(request: Request):
    return templates.TemplateResponse(name='login_form.html', context={'request': request})