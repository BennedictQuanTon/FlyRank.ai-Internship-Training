# To-Do List CRUD API with SQLite Persistence (FlyRank Internship Backend Track - W3-A2)

A production-ready, lightweight RESTful CRUD API for managing a To-Do list, built with **Python 3.10+**, **FastAPI**, and backed by a persistent **SQLite** database (`tasks.db`).

---

## 🚀 How to Install & Run

1. **Clone the repository:**
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd todo-crud-api
   ```

2. **Set up virtual environment & install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install "fastapi[standard]" pydantic pytest httpx
   ```

3. **Start the API server (One Documented Command):**
   ```bash
   uvicorn main:app --reload --port 8000
   # Or using FastAPI CLI:
   # fastapi dev main.py
   ```

The server will automatically create `tasks.db`, initialize the `tasks` table with indexes, and seed 3 initial tasks if the database is empty. The server runs at `http://localhost:8000`.

---

## 💡 Why SQLite Was Chosen

* **Zero-configuration & Serverless:** SQLite requires no separate server process, socket connection, daemon, or user credentials to manage.
* **Standard Library Integration:** Python comes with the `sqlite3` module built-in, requiring no external C-drivers or third-party database adapters.
* **Single-File Simplicity:** The entire database (schema, tables, indexes, data) is self-contained in a single portable file: `tasks.db`.
* **True Persistence:** Unlike the in-memory dictionary of Week 2, data stored in SQLite is written safely to disk via ACID transactions and survives application restarts or crashes.

---

## 📂 Database Architecture & Storage Lifecycle

* **Database File:** Located at `./tasks.db` in the repository root.
* **Auto-creation:** On application startup, `init_db()` runs automatically. If `tasks.db` or table `tasks` does not exist, it is created on the fly.
* **Idempotent Seeding:** The 3 initial tasks are only seeded if `SELECT COUNT(*) FROM tasks` returns `0`. Restarting the application multiple times will **never** duplicate records.
* **Git-Ignored:** `tasks.db` and `*.db` are listed in `.gitignore` so each clean clone starts with a fresh local database.

---

## 📋 Endpoints Overview

| Method | Endpoint | Description | Status Code (Success / Error) |
| --- | --- | --- | --- |
| `GET` | `/` | API metadata & available endpoints | `200 OK` |
| `GET` | `/health` | Server health check | `200 OK` |
| `GET` | `/tasks` | List tasks (supports `?done=true`, `?search=term`, `?sort=title`) | `200 OK` |
| `GET` | `/tasks/{id}` | Get single task details | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create a new task (parameterized `INSERT`) | `201 Created` / `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update task title and/or status (parameterized `UPDATE`) | `200 OK` / `400 Bad Request` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete a task (parameterized `DELETE`) | `204 No Content` / `404 Not Found` |
| `GET` | `/stats` | Task statistics via SQL `COUNT(*)` | `200 OK` |
| `POST` | `/reset` | Atomically reset database table to initial 3 tasks | `200 OK` |

---

## 💻 Sample `curl` Interaction

**1. Create a task:**
```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Verify SQLite Persistence"}'
```
*Response:* `201 Created`
```json
{"id": 4, "title": "Verify SQLite Persistence", "done": false}
```

**2. Fetch single task:**
```bash
curl -i http://localhost:8000/tasks/4
```
*Response:* `200 OK`
```json
{"id": 4, "title": "Verify SQLite Persistence", "done": false}
```

---

## 📸 Database Inspection with DB Browser for SQLite

Opening `tasks.db` in **DB Browser for SQLite** displays the `tasks` table with live rows:

![DB Browser for SQLite](db_browser.jpg)

Both FastAPI and DB Browser for SQLite read directly from the exact same `tasks.db` file on disk. Any edit or manual SQL query made in DB Browser is immediately visible on the API endpoints without restarting the server.

---

## 🔍 Stage 4: Explored SQLite by Hand

Using DB Browser's **Execute SQL** tab (or direct SQLite query), the following queries were executed and verified:

| SQL Query | Description | Result Observed |
| --- | --- | --- |
| `SELECT * FROM tasks;` | List every task | Returns 3 rows: `Buy milk`, `Read FastAPI docs`, `Build CRUD API assignment` |
| `SELECT * FROM tasks WHERE done = 1;` | Filter completed tasks | Returns 1 row: Task 2 (`Read FastAPI docs`) |
| `SELECT COUNT(*) FROM tasks;` | Count total records | Returns scalar value `3` |
| `UPDATE tasks SET done = 1;` | Mark all tasks as completed | Updated 3 rows; `GET /tasks` immediately returns all tasks with `done: true` |
| `DELETE FROM tasks WHERE done = 1;` | Purge completed tasks | Deleted all rows; `GET /tasks` immediately returns `[]` |

---

## 🛡️ Proof: Storage is "Just an Implementation Detail"

In Assignment 1, tasks were stored in a Python in-memory list `tasks_db`. In Assignment 2, tasks are stored in SQLite `tasks.db`.

Despite replacing the entire storage layer underneath:
1. **Identical API Contracts:** Every endpoint path, HTTP method, payload format, and status code (`200`, `201`, `204`, `400`, `404`) remains identical.
2. **100% Test Pass Rate:** The entire original test suite in `test_main.py` passes without any modifications to client assertions.

This demonstrates a foundational backend design principle: **the API is the public contract with clients; the database is merely an implementation detail of the persistence layer**.

---

## ⚡ Extras & Database Optimizations

* **Database Indexes:** Created `idx_tasks_done` on `tasks(done)` and `idx_tasks_title` on `tasks(title)`.
  * *Why it matters:* An index creates a B-Tree search structure enabling the database engine to locate filtered tasks in $O(\log N)$ time rather than performing an expensive $O(N)$ full-table scan.
* **Atomic Transactions:** Initial seeding and table resets are wrapped in database transactions (`BEGIN ... COMMIT`).
  * *Why it matters:* Transactions ensure atomicity (all-or-nothing execution), guaranteeing that partial or corrupted data is never written to disk if a query fails midway.
