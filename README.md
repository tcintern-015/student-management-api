# Book API (FastAPI Fundamentals – Part 2)

A CRUD REST API built with **FastAPI** to manage books, using an in-memory data store and Pydantic models for request/response validation.

> This project continues from Day 1's Student Management API, applying the same fundamentals (routing, path/query params, Pydantic validation) plus PUT/DELETE, HTTPException handling, and better code organization.

## Features

- `GET /books` – Retrieve all books
- `GET /books/{id}` – Retrieve a book by ID
- `POST /books` – Add a new book
- `PUT /books/{id}` – Update an existing book (partial updates supported)
- `DELETE /books/{id}` – Delete a book
- `GET /books/search` – Search books by title, author, genre, or year (query parameters)
- Input validation via Pydantic (title/author length, valid year, non-negative price)
- Proper HTTP status codes (200, 201, 204, 404, 422)
- Errors handled with `HTTPException`
- Pydantic models organized in a separate `models.py` file
- Auto-generated interactive docs (Swagger UI + ReDoc)

## Project Structure

```
student-management-api/
├── main.py            # FastAPI app and all routes
├── models.py           # Pydantic models (Book, BookCreate, BookUpdate)
├── requirements.txt    # Python dependencies
└── README.md
```

## Setup & Run

1. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Open your browser:
   - API base: http://127.0.0.1:8000
   - Swagger docs: http://127.0.0.1:8000/docs
   - ReDoc docs: http://127.0.0.1:8000/redoc

## Example Usage

**Create a book**
```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "genre": "Fantasy", "price": 15.99}'
```

**Get all books**
```bash
curl http://127.0.0.1:8000/books
```

**Get a book by ID**
```bash
curl http://127.0.0.1:8000/books/1
```

**Search books**
```bash
curl "http://127.0.0.1:8000/books/search?author=tolkien"
curl "http://127.0.0.1:8000/books/search?genre=fantasy&year=1937"
```

**Update a book**
```bash
curl -X PUT http://127.0.0.1:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 9.99}'
```

**Delete a book**
```bash
curl -X DELETE http://127.0.0.1:8000/books/1
```

## Notes

- Data is stored **in memory**, so it resets every time the server restarts. This keeps the example simple — the next part of the track moves on to real databases.
