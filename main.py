import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Query, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
import db
import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    print("Server running and connected to Supabase")
    yield

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing a To-Do list backed by PostgreSQL in Docker with Supabase Auth.",
    lifespan=lifespan
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/auth"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Email and password are required"}
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

class AuthCredentials(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED, summary="Sign up a new user with Supabase Auth")
def signup(creds: AuthCredentials):
    if not creds.email or not creds.password or not creds.email.strip() or not creds.password.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Email and password are required"}
        )
    try:
        client = auth.get_supabase()
        res = client.auth.sign_up({"email": creds.email.strip(), "password": creds.password.strip()})
        if not res or not res.user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Registration failed"}
            )
        user_data = {
            "id": str(res.user.id),
            "email": res.user.email,
            "created_at": str(res.user.created_at) if res.user.created_at else None
        }
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User registered successfully", "user": user_data}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )

@app.post("/auth/login", summary="Log in with email and password")
def login(creds: AuthCredentials):
    if not creds.email or not creds.password or not creds.email.strip() or not creds.password.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Email and password are required"}
        )
    try:
        client = auth.get_supabase()
        res = client.auth.sign_in_with_password({"email": creds.email.strip(), "password": creds.password.strip()})
        if not res or not res.session or not res.session.access_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid login credentials"}
            )
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": str(res.user.id) if res.user else None,
                "email": res.user.email if res.user else creds.email
            }
        }
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid login credentials"}
        )

@app.get("/public/info", summary="Public information endpoint")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile", summary="User profile (unverified token check)")
def get_protected_profile_unverified(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Access token required"}
        )
    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Access token required"}
        )
    return {"message": "Token presented", "token": token}

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
    db_ok = db.ping_db()
    return {
        "status": "ok",
        "db": "ok" if db_ok else "error"
    }



@app.get("/tasks", summary="List tasks with optional filtering, search, and sorting")
def get_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    search: Optional[str] = Query(None, description="Search term to filter task titles"),
    sort: Optional[str] = Query(None, description="Sort order: 'title' or 'id'")
):
    return db.get_all_tasks(done=done, search=search, sort=sort)

@app.get("/tasks/{task_id}", summary="Get a single task by ID")
def get_task(task_id: int):
    task = db.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a new task")
def create_task(task_in: TaskCreate):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty or blank"
        )
    return db.create_task(task_in.title.strip())

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

    updated = db.update_task(
        task_id,
        title=task_in.title.strip() if task_in.title is not None else None,
        done=task_in.done
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return updated

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id: int):
    deleted = db.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return

@app.get("/stats", summary="Get task statistics")
def get_stats():
    return db.get_stats()

@app.post("/reset", summary="Reset tasks to initial state")
def reset_tasks():
    reset_list = db.reset_tasks()
    return {"message": "Tasks reset to initial state", "tasks": reset_list}
