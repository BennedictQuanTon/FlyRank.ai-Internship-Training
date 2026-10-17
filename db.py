import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgres://postgres:dev@localhost:5432/tasks"
)

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    try:
        conn = get_connection()
    except Exception as e:
        print(f"Notice: PostgreSQL connection unavailable ({e}). Start Docker container to enable task database.")
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        done BOOLEAN NOT NULL DEFAULT FALSE
                    );
                """)
                cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_done ON tasks(done);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_title ON tasks(title);")
                cur.execute("SELECT COUNT(*) FROM tasks;")
                row = cur.fetchone()
                count = row["count"] if isinstance(row, dict) else row[0]
                if count == 0:
                    cur.executemany(
                        "INSERT INTO tasks (title, done) VALUES (%s, %s);",
                        [
                            ("Buy milk", False),
                            ("Read FastAPI docs", True),
                            ("Build CRUD API assignment", False),
                        ]
                    )
    finally:
        conn.close()

def get_all_tasks(
    done: Optional[bool] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None
) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT id, title, done FROM tasks WHERE 1=1"
            params = []
            if done is not None:
                query += " AND done = %s"
                params.append(done)
            if search:
                query += " AND title ILIKE %s"
                params.append(f"%{search}%")
            if sort == "title":
                query += " ORDER BY title ASC"
            else:
                query += " ORDER BY id ASC"
            cur.execute(query, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
    finally:
        conn.close()

def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    finally:
        conn.close()

def create_task(title: str) -> Dict[str, Any]:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;",
                    (title, False)
                )
                return dict(cur.fetchone())
    finally:
        conn.close()

def update_task(task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
                existing = cur.fetchone()
                if not existing:
                    return None
                new_title = title if title is not None else existing["title"]
                new_done = done if done is not None else existing["done"]
                cur.execute(
                    "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
                    (new_title, new_done, task_id)
                )
                return dict(cur.fetchone())
    finally:
        conn.close()

def delete_task(task_id: int) -> bool:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", (task_id,))
                return cur.fetchone() is not None
    finally:
        conn.close()

def get_stats() -> Dict[str, int]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM tasks;")
            total = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) AS completed FROM tasks WHERE done = TRUE;")
            completed = cur.fetchone()["completed"]
            return {
                "total": total,
                "done": completed,
                "open": total - completed
            }
    finally:
        conn.close()

def reset_tasks() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE tasks RESTART IDENTITY;")
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s);",
                    [
                        ("Buy milk", False),
                        ("Read FastAPI docs", True),
                        ("Build CRUD API assignment", False),
                    ]
                )
                cur.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
                return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()

def ping_db() -> bool:
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
        conn.close()
        return True
    except Exception:
        return False
