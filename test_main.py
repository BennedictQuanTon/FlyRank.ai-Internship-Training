import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def setup_function():
    client.post("/reset")

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Task API"
    assert "endpoints" in data

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3

def test_get_single_task_success():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"

def test_get_single_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task 999 not found"

def test_create_task_success():
    response = client.post("/tasks", json={"title": "New Task"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["title"] == "New Task"
    assert data["done"] is False

def test_create_task_empty_title():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code in [400, 422]

def test_update_task_success():
    response = client.put("/tasks/1", json={"done": True, "title": "Buy organic milk"})
    assert response.status_code == 200
    data = response.json()
    assert data["done"] is True
    assert data["title"] == "Buy organic milk"

def test_update_task_not_found():
    response = client.put("/tasks/99", json={"done": True})
    assert response.status_code == 404

def test_delete_task_success():
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    # Verify deleted
    get_res = client.get("/tasks/1")
    assert get_res.status_code == 404

def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404

def test_filtering_and_search():
    res_done = client.get("/tasks?done=true")
    assert res_done.status_code == 200
    assert len(res_done.json()) == 1
    assert res_done.json()[0]["id"] == 2

    res_search = client.get("/tasks?search=milk")
    assert res_search.status_code == 200
    assert len(res_search.json()) == 1
    assert res_search.json()[0]["title"] == "Buy milk"

def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["done"] == 1
    assert data["open"] == 2

def test_reset():
    client.delete("/tasks/1")
    res_before = client.get("/tasks")
    assert len(res_before.json()) == 2

    res_reset = client.post("/reset")
    assert res_reset.status_code == 200
    res_after = client.get("/tasks")
    assert len(res_after.json()) == 3

def test_sorting():
    res = client.get("/tasks?sort=title")
    assert res.status_code == 200
    titles = [t["title"] for t in res.json()]
    assert titles == sorted(titles)

def test_persistence_in_database():
    import db
    res = client.post("/tasks", json={"title": "DB Direct Test"})
    assert res.status_code == 201
    new_id = res.json()["id"]

    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT title, done FROM tasks WHERE id = %s;", (new_id,))
        row = cur.fetchone()
    conn.close()

    assert row is not None
    assert row["title"] == "DB Direct Test"
    assert row["done"] is False
