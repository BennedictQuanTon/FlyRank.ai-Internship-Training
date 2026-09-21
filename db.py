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
    conn = get_connection()
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
