# To-Do List CRUD API — Containerized Stack (FlyRank Internship Backend Track - W1-A3)

A production-grade, containerized RESTful CRUD API for managing a To-Do list, built with **Python 3.10+**, **FastAPI**, and backed by a **PostgreSQL** database running in **Docker**, fully managed via **Docker Compose**.

This marks the third evolutionary step of the storage layer in the same repository:
$$\text{In-Memory List (A1)} \longrightarrow \text{SQLite File (A2)} \longrightarrow \text{Containerized PostgreSQL (A3)}$$

---

## 🚀 One Command to Run Everything

From a fresh clone, you can start the entire stack (API server + PostgreSQL database) with zero manual database installation:

1. **Clone the repository:**
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd todo-crud-api
   ```

2. **Copy environment configuration:**
   ```bash
   cp .env.example .env
   ```

3. **Start the whole stack with one command:**
   ```bash
   docker compose up -d --build
   ```

* The API will be live at `http://localhost:8000`.
* The PostgreSQL database will be accessible at `localhost:5432` (`database: tasks`, `user: postgres`, `password: dev`).
* Automatic table creation and initial seeding happen automatically on first startup.

To stop the stack:
```bash
docker compose down
```

---

## ⚙️ Environment Variables (`.env`)

Database credentials and connection strings are managed securely via environment variables and never hardcoded in source code. 

* `.env` is ignored by Git in [.gitignore](.gitignore) to prevent credential leaks.
* Refer to [.env.example](.env.example) for key definitions:

```env
DATABASE_URL=postgres://postgres:dev@localhost:5432/tasks
```

Inside Docker Compose, the connection URL is automatically wired to the internal network service name `db`:
```env
DATABASE_URL=postgres://postgres:dev@db:5432/tasks
```

---

## 📋 Endpoints Overview

| Method | Endpoint | Description | Status Code (Success / Error) |
| --- | --- | --- | --- |
| `GET` | `/` | API metadata & registered routes | `200 OK` |
| `GET` | `/health` | Deep health check (pings database via `SELECT 1`) | `200 OK` (`{"status":"ok","db":"ok"}`) |
| `GET` | `/tasks` | List tasks (supports `?done=true`, `?search=term`, `?sort=title`) | `200 OK` |
| `GET` | `/tasks/{id}` | Get single task by ID | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create a new task (parameterized `INSERT ... RETURNING *`) | `201 Created` / `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update task title and/or status | `200 OK` / `400 Bad Request` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete a task | `204 No Content` / `404 Not Found` |
| `GET` | `/stats` | Task statistics computed via SQL `COUNT(*)` | `200 OK` |
| `POST` | `/reset` | Atomically truncate & re-seed 3 initial tasks | `200 OK` |

---

## 💻 Sample `curl` Output

**Request:** Creating a task against the Docker stack
```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Verify PostgreSQL in Docker"}'
```

**Response:**
```http
HTTP/1.1 201 Created
date: Mon, 21 Sep 2026 04:30:00 GMT
server: uvicorn
content-length: 77
content-type: application/json

{"id":4,"title":"Verify PostgreSQL in Docker","done":false}
```

---

## 📸 Database Verification (TablePlus / psql)

Inspecting the containerized PostgreSQL database confirms our schema, table, and data:

![PostgreSQL in Docker](postgres_db.jpg)

Running directly inside the container:
```bash
docker compose exec db psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```
Output:
```text
 id |           title           | done 
----+---------------------------+------
  1 | Buy milk                  | f
  2 | Read FastAPI docs         | t
  3 | Build CRUD API assignment | f
(3 rows)
```

---

## 🧪 The Mortality Experiment (Why Volumes Exist)

* **Without a Volume:** A container's writable filesystem layer is ephemeral. If you run a PostgreSQL container without mounting a volume and execute `docker rm -f <container_id>`, all data written to `/var/lib/postgresql/data` vanishes permanently with the destroyed container.
* **With a Named Volume (`taskdata`):** Named volumes live independently in Docker's host storage. When running `docker compose down` and `docker compose up`, the container is recreated fresh, but the database files in `taskdata` remain intact. This guarantees true durability across application lifecycles.

---

## 🛡️ Proof: Storage is "Just an Implementation Detail"

Across three consecutive assignments (A1: In-Memory, A2: SQLite, A3: PostgreSQL in Docker):
1. The 5 CRUD endpoints and their request/response JSON schemas remained completely identical.
2. All 16 automated tests in `test_main.py` pass 100% without changing endpoint assertions.
3. Every database operation is encapsulated inside a dedicated repository module ([db.py](db.py)).

This confirms the core architectural insight: **the API contract is the boundary; where and how data is persisted is purely an internal implementation detail**.

---

## ⚡ Extras & Production Best Practices

* **Deep Health Check:** `GET /health` executes a live `SELECT 1` query to verify that the database connection pool is responsive. In production, load balancers and container orchestrators (Kubernetes / ECS) use this probe to route traffic only to ready containers and prevent downtime during rollouts.
* **Database Indexes:** Created B-Tree indexes `idx_tasks_done` and `idx_tasks_title` in PostgreSQL for $O(\log N)$ lookup performance on filter and search queries.
* **Docker Compose Healthcheck:** Configured `pg_isready` check on `db` service with `depends_on: { db: { condition: service_healthy } }` so the API service only starts when PostgreSQL is ready to accept connections.
