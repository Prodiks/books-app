from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.books.router import router as books_router
from src.db import db_create
from src.pages.router import router as books_pages
from src.users.router import router as users_pages
from src.reviews.router import router as reviews_pages


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home_page():
    return {"message": "Hello World"}


app.include_router(books_router)
app.include_router(books_pages)
app.include_router(users_pages)
app.include_router(reviews_pages)
