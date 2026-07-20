from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Student Management API",
    description="A simple API to manage student records built with FastAPI",
    version="1.0.0",
)


# ---------- Pydantic Models ----------

class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="John Doe")
    age: int = Field(..., gt=0, lt=120, example=20)
    email: str = Field(..., example="john.doe@example.com")
    course: Optional[str] = Field(None, example="Computer Science")


class StudentCreate(StudentBase):
    """Model used when creating a new student (no ID needed, client doesn't set it)."""
    pass


class StudentUpdate(BaseModel):
    """Model used for updating a student. All fields optional for partial updates."""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, gt=0, lt=120)
    email: Optional[str] = None
    course: Optional[str] = None


class Student(StudentBase):
    """Model returned to the client, includes the ID."""
    id: int


# ---------- In-memory "database" ----------

students_db: dict[int, Student] = {}
next_id = 1


# ---------- Routes ----------

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Student Management API. Visit /docs for the interactive API docs."}


@app.get("/students", response_model=List[Student], tags=["Students"])
def get_students():
    """Return all students."""
    return list(students_db.values())


@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: int):
    """Return a single student by ID."""
    student = students_db.get(student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found",
        )
    return student


@app.post(
    "/students",
    response_model=Student,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def create_student(student: StudentCreate):
    """Add a new student."""
    global next_id
    new_student = Student(id=next_id, **student.dict())
    students_db[next_id] = new_student
    next_id += 1
    return new_student


@app.put("/students/{student_id}", response_model=Student, tags=["Students"])
def update_student(student_id: int, student_update: StudentUpdate):
    """Update an existing student. Supports partial updates."""
    existing = students_db.get(student_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found",
        )

    update_data = student_update.dict(exclude_unset=True)
    updated_student = existing.copy(update=update_data)
    students_db[student_id] = updated_student
    return updated_student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int):
    """Delete a student by ID."""
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found",
        )
    del students_db[student_id]
    return None
