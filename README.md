# To-Do & Auth API — Secured with Supabase Auth & JWTs (FlyRank Backend Track - W2-A4)

A secure, production-grade RESTful API built with **Python 3.10+**, **FastAPI**, and **Supabase Auth** as the Identity Provider (IdP). This system implements end-to-end user authentication (Sign Up, Log In, Log Out), token issuance, JSON Web Token (JWT) verification, and reusable dependency-based route protection with interactive Swagger UI Bearer authorization.

---

## 🏛️ The Architecture: The Trust Triangle

Secure authentication follows a strict three-party trust model:

```
[ Client ] ────────── (1) Email + Password ──────────► [ Supabase Auth (IdP) ]
    │                                                          │
    │ ◄────────── (2) JWT Access Token + Refresh Token ────────┘
    │
    ▼
(3) HTTP Request + Header
    `Authorization: Bearer <token>`
    │
    ▼
[ FastAPI Backend ] ─── (4) Verify Token via SDK ────► [ Supabase Auth ]
    │
    ▼
(5) 200 OK / Protected Resource OR 401 Unauthorized
```

1. **Client &rarr; Supabase**: User submits credentials to register or log in.
2. **Supabase &rarr; Client**: Supabase securely verifies and hashes credentials, issuing a signed JWT `access_token` and `refresh_token`.
3. **Client &rarr; Backend**: Client attaches the token in the `Authorization: Bearer <token>` HTTP header.
4. **Backend &rarr; Supabase**: Backend verifies the token authenticity with Supabase (`get_user`).
5. **Backend &rarr; Client**: Access is granted (`200 OK`) or forged/expired passes are rejected (`401 Unauthorized`).

---

## 🚀 One Command to Run the Server

From a fresh clone, run the authenticated API server in under 1 minute:

```bash
uvicorn main:app --reload --port 8000
```

* Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Alternative ReDoc documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* Public healthcheck: [http://localhost:8000/public/info](http://localhost:8000/public/info)

---

## ⚙️ Environment Variables Configuration (`.env`)

Never commit credentials to version control. All secrets are managed through environment variables loaded via `python-dotenv`:

1. Copy the provided template:
   ```bash
   cp .env.example .env
   ```
2. Populate `.env` with your Supabase credentials:
   ```env
   # Database connection for task CRUD
   DATABASE_URL=postgres://postgres:dev@localhost:5432/tasks

   # Supabase Project settings (Dashboard -> Project Settings -> API)
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-public-key

   PORT=8000
   ```
3. **Supabase Dashboard Setting:** Under **Authentication &rarr; Providers &rarr; Email**, toggle **"Confirm email"** to **OFF** so newly registered accounts can log in immediately for development and testing.

> [!IMPORTANT]
> The `.env` file is protected by [.gitignore](.gitignore) and is never committed to GitHub. Only [.env.example](.env.example) with placeholder values is tracked.

---

## 📋 API Reference Table

| Method | Endpoint | Auth Required | Header / Body | Success | Error Statuses |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `POST` | `/auth/signup` | ❌ No | Body: `{"email", "password"}` | `201 Created` | `400 Bad Request` |
| `POST` | `/auth/login` | ❌ No | Body: `{"email", "password"}` | `200 OK` | `400 Bad Request`, `401 Unauthorized` |
| `POST` | `/auth/logout` | ✅ Yes | `Authorization: Bearer <token>` | `204 No Content` | `401 Unauthorized` |
| `GET` | `/public/info` | ❌ No | None | `200 OK` | — |
| `GET` | `/protected/profile` | ✅ Yes | `Authorization: Bearer <token>` | `200 OK` | `401 Unauthorized` |
| `GET` | `/protected/dashboard` | ✅ Yes | `Authorization: Bearer <token>` | `200 OK` | `401 Unauthorized` |

---

## 🔒 Interactive Swagger UI with Bearer Padlock

FastAPI provides built-in Swagger UI with full `HTTPBearer` security integration:

![Swagger UI Authorization](assets/swagger_auth.jpg)

### Testing via Swagger UI:
1. Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.
2. Execute `POST /auth/login` to obtain an `access_token`.
3. Click the green **Authorize 🔓** button at the top right.
4. Paste the token into the value field and click **Authorize**.
5. All protected endpoints (`/protected/profile`, `/protected/dashboard`, `/auth/logout`) now display locked padlocks **🔒** and can be tested directly with **Try it out**.

---

## 💻 Testing via `curl` Checkpoints

### 1. Register a new user (`POST /auth/signup`)
```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"password123"}'
```
*Expected: `201 Created` with user metadata.*

### 2. Log in (`POST /auth/login`)
```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"password123"}'
```
*Expected: `200 OK` with `access_token` and `refresh_token`.*

### 3. Public endpoint (`GET /public/info`)
```bash
curl -i http://localhost:8000/public/info
```
*Expected: `200 OK` (`{"message": "Welcome stranger! This info is public."}`).*

### 4. Protected profile with valid token (`GET /protected/profile`)
```bash
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <PASTE_YOUR_ACCESS_TOKEN_HERE>"
```
*Expected: `200 OK` with user id, email, and account creation timestamp.*

### 5. Rejection of tampered / invalid token
```bash
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer invalid_or_tampered_token"
```
*Expected: `401 Unauthorized` with `{"error": "Invalid or expired token"}`.*

### 6. Log out (`POST /auth/logout`)
```bash
curl -i -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer <PASTE_YOUR_ACCESS_TOKEN_HERE>"
```
*Expected: `204 No Content`.*

---

## 🧪 Automated Test Suite

Run the full automated test suite covering all authentication scenarios (valid credentials, invalid credentials, missing headers, tampered tokens, logout, and public endpoints):

```bash
pytest test_auth.py -v
```

All 14 unit and integration test cases pass 100% with zero warnings.
