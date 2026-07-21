from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="The Hobbit")
    author: str = Field(..., min_length=1, max_length=100, example="J.R.R. Tolkien")
    year: int = Field(..., gt=0, lt=2100, example=1937)
    genre: Optional[str] = Field(None, max_length=50, example="Fantasy")
    price: Optional[float] = Field(None, ge=0, example=15.99)


class BookCreate(BookBase):
    """Model used when creating a new book (no ID needed, client doesn't set it)."""
    pass


class BookUpdate(BaseModel):
    """Model used for updating a book. All fields optional for partial updates."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, gt=0, lt=2100)
    genre: Optional[str] = Field(None, max_length=50)
    price: Optional[float] = Field(None, ge=0)


class Book(BookBase):
    """Model returned to the client, includes the ID."""
    id: int
