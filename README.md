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

---

## 🤖 Stage 7: The AI Rematch (AI vs Me)

### 1. Specification Prompt Provided to the AI
> *"Build a secured REST API using Python FastAPI and Supabase Auth as the Identity Provider.*
> *Implement 5 endpoints:*
> *1. POST /auth/signup (accepts JSON {email, password}, validates inputs returning 400 on empty fields, calls supabase.auth.sign_up, returns 201 on success).*
> *2. POST /auth/login (accepts {email, password}, returns 400 on missing fields, calls supabase.auth.sign_in_with_password, returns 200 with access_token and refresh_token, or 401 on bad credentials).*
> *3. GET /public/info (public endpoint returning 200 with public message).*
> *4. GET /protected/profile and GET /protected/dashboard (token-guarded endpoints returning user metadata on 200, or 401 with {'error': '...'} on missing/invalid/expired token).*
> *5. POST /auth/logout (protected endpoint, calls supabase.auth.sign_out, returns 204).*
> *Extract token inspection and verification into a reusable FastAPI dependency using HTTPBearer. Ensure Swagger UI at /docs supports Authorize padlock."*

The raw AI generated code is quarantined in [`ai-version/`](ai-version/).

### 2. Concrete Differences & Architectural Analysis (`git diff --no-index`)

1. **How did it handle token extraction — did it correctly parse the "Bearer " prefix, or would `Authorization: <token>` slip through or crash?**
   * The AI used FastAPI's default `security = HTTPBearer()` where `auto_error` defaults to `True`. When a client calls a protected route without an `Authorization` header, Starlette's dependency immediately aborts with `HTTP 403 Forbidden` (`{"detail": "Not authenticated"}`) instead of the assignment's required `HTTP 401 Unauthorized` (`{"error": "Access token required"}`).
   * In our hand-crafted implementation, we used `HTTPBearer(auto_error=False)` and inspected the header manually, correctly returning `401 Unauthorized` whenever a header is missing, malformed, or lacks the `Bearer ` prefix.

2. **What security flaws might it have introduced — does it safely reject an invalid token, or trust getUser without checking the error? Did it leak the service_role key or log the token?**
   * **Unsanitized Whitespace:** The AI declared standard Pydantic models `email: str`, `password: str`. A malicious or invalid input with only spaces (`{"email": "  ", "password": "  "}`) was accepted by validation and forwarded directly to Supabase. Our implementation explicitly trims and checks for empty or blank strings, returning `400 Bad Request`.
   * **Internal Error Leakage:** The AI caught registration errors with `raise HTTPException(status_code=400, detail=str(e))`, which exposes raw network errors, database hostnames, or API key validation failures directly to external callers.
   * **Unsafe Unpacking:** The AI assumed `supabase.auth.get_user(token)` always returns a valid object with `.user` attribute populated, rather than handling `None` checks defensively.

3. **What did your prompt forget to specify — and what did the AI silently decide for you?**
   * The initial prompt did not specify the exact JSON error schema (`{"error": "..."}` vs FastAPI's default `{"detail": "..."}`), nor did it specify the custom exception handler for `RequestValidationError` to map 422 errors to 400 for `/auth` routes.
   * The AI silently chose to place all database connection, authentication, and route handling into a single monolithic file rather than maintaining a clean, modular structure (`auth.py` + `main.py`).

### 3. Rematch & Prompt Refinement
* **Refined Prompt:** *"Configure HTTPBearer(auto_error=False) and custom exception handlers so missing, malformed, or invalid tokens strictly yield 401 with JSON key 'error'. Sanitize whitespace on credential inputs. Separate auth client initialization and dependencies into auth.py."*
* **Outcome:** With these precise constraints, the regenerated AI solution successfully adhered to strict 401 status codes and matched the modular architecture of the hand-crafted codebase.

