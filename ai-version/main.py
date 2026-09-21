import sqlite3
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="AI Version - SQLite To-Do CRUD API")

DB_NAME = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Buy milk", 0),
                ("Read FastAPI docs", 1),
                ("Build CRUD API assignment", 0)
            ]
        )
        conn.commit()
    conn.close()

init_db()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool

@app.get("/")
def get_root():
    return {"message": "Welcome to AI-generated SQLite Task API"}

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r["id"], "title": r["title"], "done": bool(r["done"])} for r in rows]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task_in.title.strip(), 0))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": new_id, "title": task_in.title.strip(), "done": False}

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdate):
    if task_in.title is None and task_in.done is None:
        raise HTTPException(status_code=400, detail="Must provide title or done")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    new_title = task_in.title.strip() if task_in.title is not None else row["title"]
    new_done = task_in.done if task_in.done is not None else bool(row["done"])
    
    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (new_title, int(new_done), task_id))
    conn.commit()
    conn.close()
    return {"id": task_id, "title": new_title, "done": bool(new_done)}

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return None
