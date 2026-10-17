import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
import auth

client = TestClient(app)

def test_signup_missing_fields():
    # Missing password
    res1 = client.post("/auth/signup", json={"email": "user@example.com"})
    assert res1.status_code == 400
    assert "error" in res1.json()

    # Missing email
    res2 = client.post("/auth/signup", json={"password": "password123"})
    assert res2.status_code == 400
    assert "error" in res2.json()

    # Blank strings
    res3 = client.post("/auth/signup", json={"email": "  ", "password": "  "})
    assert res3.status_code == 400
    assert "error" in res3.json()

    # Empty payload
    res4 = client.post("/auth/signup", json={})
    assert res4.status_code == 400
    assert "error" in res4.json()

def test_login_missing_fields():
    # Missing password
    res1 = client.post("/auth/login", json={"email": "user@example.com"})
    assert res1.status_code == 400
    assert "error" in res1.json()

    # Missing email
    res2 = client.post("/auth/login", json={"password": "password123"})
    assert res2.status_code == 400
    assert "error" in res2.json()

    # Blank strings
    res3 = client.post("/auth/login", json={"email": "", "password": ""})
    assert res3.status_code == 400
    assert "error" in res3.json()

def test_signup_success(monkeypatch):
    mock_supabase = MagicMock()
    mock_user = MagicMock()
    mock_user.id = "mock-uuid-1234"
    mock_user.email = "test@example.com"
    mock_user.created_at = "2026-10-17T00:00:00Z"
    
    mock_res = MagicMock()
    mock_res.user = mock_user
    mock_supabase.auth.sign_up.return_value = mock_res
    
    monkeypatch.setattr(auth, "get_supabase", lambda: mock_supabase)

    response = client.post("/auth/signup", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["id"] == "mock-uuid-1234"

def test_login_success(monkeypatch):
    mock_supabase = MagicMock()
    mock_session = MagicMock()
    mock_session.access_token = "mock_jwt_access_token"
    mock_session.refresh_token = "mock_refresh_token"
    
    mock_user = MagicMock()
    mock_user.id = "mock-uuid-1234"
    mock_user.email = "test@example.com"
    
    mock_res = MagicMock()
    mock_res.session = mock_session
    mock_res.user = mock_user
    mock_supabase.auth.sign_in_with_password.return_value = mock_res
    
    monkeypatch.setattr(auth, "get_supabase", lambda: mock_supabase)

    response = client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "mock_jwt_access_token"
    assert data["refresh_token"] == "mock_refresh_token"
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(monkeypatch):
    mock_supabase = MagicMock()
    mock_supabase.auth.sign_in_with_password.side_effect = Exception("Invalid login credentials")
    
    monkeypatch.setattr(auth, "get_supabase", lambda: mock_supabase)

    response = client.post("/auth/login", json={"email": "wrong@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"error": "Invalid login credentials"}
