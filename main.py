from fastapi import FastAPI, HTTPException, status, Query
from typing import Optional, List

from models import Book, BookCreate, BookUpdate

app = FastAPI(
    title="Book API",
    description="A simple CRUD API to manage books, built with FastAPI (Part 2 - continued from Student Management API)",
    version="2.0.0",
)


# ---------- In-memory "database" ----------

books_db: dict[int, Book] = {}
next_id = 1


# ---------- Routes ----------

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Book API. Visit /docs for the interactive API docs."}


@app.get("/books", response_model=List[Book], tags=["Books"])
def get_books():
    """Retrieve all books."""
    return list(books_db.values())


@app.get("/books/search", response_model=List[Book], tags=["Books"])
def search_books(
    title: Optional[str] = Query(None, description="Filter by (partial) title"),
    author: Optional[str] = Query(None, description="Filter by (partial) author name"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    year: Optional[int] = Query(None, description="Filter by exact publication year"),
):
    """
    Search books using query parameters.
    Example: /books/search?author=tolkien&genre=fantasy
    """
    results = list(books_db.values())

    if title:
        results = [b for b in results if title.lower() in b.title.lower()]
    if author:
        results = [b for b in results if author.lower() in b.author.lower()]
    if genre:
        results = [b for b in results if b.genre and genre.lower() in b.genre.lower()]
    if year:
        results = [b for b in results if b.year == year]

    return results


@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
def get_book(book_id: int):
    """Retrieve a book by ID."""
    book = books_db.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return book


@app.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
)
def create_book(book: BookCreate):
    """Add a new book."""
    global next_id
    new_book = Book(id=next_id, **book.dict())
    books_db[next_id] = new_book
    next_id += 1
    return new_book


@app.put("/books/{book_id}", response_model=Book, tags=["Books"])
def update_book(book_id: int, book_update: BookUpdate):
    """Update an existing book. Supports partial updates."""
    existing = books_db.get(book_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )

    update_data = book_update.dict(exclude_unset=True)
    updated_book = existing.copy(update=update_data)
    books_db[book_id] = updated_book
    return updated_book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
def delete_book(book_id: int):
    """Delete a book by ID."""
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    del books_db[book_id]
    return None
