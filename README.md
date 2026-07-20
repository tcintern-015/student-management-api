# Student Management API

A simple REST API built with **FastAPI** to manage student records, using an in-memory data store and Pydantic models for request/response validation.

## Features

- `GET /students` – Return all students
- `GET /students/{id}` – Return a student by ID
- `POST /students` – Add a new student
- `PUT /students/{id}` – Update an existing student (partial updates supported)
- `DELETE /students/{id}` – Delete a student
- Input validation via Pydantic (name length, age range, etc.)
- Proper HTTP status codes (200, 201, 204, 404, 422)
- Auto-generated interactive docs (Swagger UI + ReDoc)

## Project Structure

```
student-management-api/
├── main.py            # FastAPI app and all routes
├── requirements.txt   # Python dependencies
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

**Create a student**
```bash
curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "age": 21, "email": "jane@example.com", "course": "Math"}'
```

**Get all students**
```bash
curl http://127.0.0.1:8000/students
```

**Get a student by ID**
```bash
curl http://127.0.0.1:8000/students/1
```

**Update a student**
```bash
curl -X PUT http://127.0.0.1:8000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"age": 22}'
```

**Delete a student**
```bash
curl -X DELETE http://127.0.0.1:8000/students/1
```

## Notes

- Data is stored **in memory**, so it resets every time the server restarts. This keeps the example simple — a real project would swap this for a database (e.g. SQLite/PostgreSQL with SQLAlchemy).
