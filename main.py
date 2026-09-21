import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional

DB_FILE = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0
                )
            """)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks")
            count = cursor.fetchone()[0]
            if count == 0:
                conn.executemany(
                    "INSERT INTO tasks (title, done) VALUES (?, ?)",
                    [
                        ("Buy milk", 0),
                        ("Read FastAPI docs", 1),
                        ("Build CRUD API assignment", 0)
                    ]
                )
    finally:
        conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing a To-Do list backed by SQLite.",
    lifespan=lifespan
)

# Initialize database on module load
init_db()

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

@app.get("/tasks", summary="List tasks with optional filtering and search")
def get_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    search: Optional[str] = Query(None, description="Search term to filter task titles")
):
    result = tasks_db
    if done is not None:
        result = [t for t in result if t["done"] == done]
    if search:
        result = [t for t in result if search.lower() in t["title"].lower()]
    return result

@app.get("/tasks/{task_id}", summary="Get a single task by ID")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a new task")
def create_task(task_in: TaskCreate):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty or blank"
        )
    next_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {
        "id": next_id,
        "title": task_in.title.strip(),
        "done": False
    }
    tasks_db.append(new_task)
    return new_task

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

    for task in tasks_db:
        if task["id"] == task_id:
            if task_in.title is not None:
                task["title"] = task_in.title.strip()
            if task_in.done is not None:
                task["done"] = task_in.done
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )

@app.get("/stats", summary="Get task statistics")
def get_stats():
    total = len(tasks_db)
    completed = sum(1 for t in tasks_db if t["done"])
    return {
        "total": total,
        "done": completed,
        "open": total - completed
    }

@app.post("/reset", summary="Reset tasks to initial state")
def reset_tasks():
    global tasks_db
    tasks_db = [dict(task) for task in INITIAL_TASKS]
    return {"message": "Tasks reset to initial state", "tasks": tasks_db}
