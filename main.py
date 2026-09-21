import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing a To-Do list backed by PostgreSQL in Docker.",
    lifespan=lifespan
)

# Initialize database on module load
db.init_db()

# In-memory fallback / initial tasks definition for reference
INITIAL_TASKS: List[Dict[str, Any]] = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Read FastAPI docs", "done": True},
    {"id": 3, "title": "Build CRUD API assignment", "done": False},
]

tasks_db: List[Dict[str, Any]] = [dict(task) for task in INITIAL_TASKS]

class TaskCreate(BaseModel):
    title: str = Field(..., description="Title of the task")

    @field_validator("title")
    def title_must_not_be_empty(cls, value: str):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty or blank")
        return value.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Updated title of the task")
    done: Optional[bool] = Field(None, description="Updated completion status of the task")

    @field_validator("title")
    def title_must_not_be_empty(cls, value: Optional[str]):
        if value is not None and not value.strip():
            raise ValueError("Task title cannot be empty or blank")
        return value.strip() if value else value

@app.get("/", summary="Root endpoint providing API info")
def get_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health", "/stats", "/reset"]
    }

@app.get("/health", summary="Health check endpoint")
def get_health():
    return {"status": "ok"}

def row_to_task(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

@app.get("/tasks", summary="List tasks with optional filtering, search, and sorting")
def get_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    search: Optional[str] = Query(None, description="Search term to filter task titles"),
    sort: Optional[str] = Query(None, description="Sort order: 'title' or 'id'")
):
    conn = get_db_connection()
    try:
        query = "SELECT id, title, done FROM tasks WHERE 1=1"
        params = []
        if done is not None:
            query += " AND done = ?"
            params.append(1 if done else 0)
        if search:
            query += " AND title LIKE ?"
            params.append(f"%{search}%")
        
        if sort == "title":
            query += " ORDER BY title ASC"
        else:
            query += " ORDER BY id ASC"
        
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [row_to_task(r) for r in rows]
    finally:
        conn.close()

@app.get("/tasks/{task_id}", summary="Get a single task by ID")
def get_task(task_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        return row_to_task(row)
    finally:
        conn.close()

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a new task")
def create_task(task_in: TaskCreate):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty or blank"
        )
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                (task_in.title.strip(), 0)
            )
            new_id = cursor.lastrowid
        return {
            "id": new_id,
            "title": task_in.title.strip(),
            "done": False
        }
    finally:
        conn.close()

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, task_in: TaskUpdate):
    if task_in.title is None and task_in.done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must contain title or done status to update"
        )
    if task_in.title is not None and not task_in.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty or blank"
        )

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )

        updated_title = task_in.title.strip() if task_in.title is not None else row["title"]
        updated_done = (1 if task_in.done else 0) if task_in.done is not None else row["done"]

        with conn:
            conn.execute(
                "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
                (updated_title, updated_done, task_id)
            )

        return {
            "id": task_id,
            "title": updated_title,
            "done": bool(updated_done)
        }
    finally:
        conn.close()

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        with conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return
    finally:
        conn.close()

@app.get("/stats", summary="Get task statistics")
def get_stats():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
        completed = cursor.fetchone()[0]
        return {
            "total": total,
            "done": completed,
            "open": total - completed
        }
    finally:
        conn.close()

@app.post("/reset", summary="Reset tasks to initial state")
def reset_tasks():
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("DELETE FROM tasks")
            conn.execute("DELETE FROM sqlite_sequence WHERE name = 'tasks'")
            conn.executemany(
                "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
                [
                    (1, "Buy milk", 0),
                    (2, "Read FastAPI docs", 1),
                    (3, "Build CRUD API assignment", 0)
                ]
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, done FROM tasks")
            rows = cursor.fetchall()
            reset_tasks_list = [row_to_task(r) for r in rows]
        return {"message": "Tasks reset to initial state", "tasks": reset_tasks_list}
    finally:
        conn.close()
