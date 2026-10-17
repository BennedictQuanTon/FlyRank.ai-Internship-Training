# FastAPI Endpoint Audit

## `main.py`

| Method | Path | Requires `Depends(auth.get_current_user)` |
|---|---|---|
| POST | `/auth/signup` | ❌ |
| POST | `/auth/login` | ❌ |
| GET | `/public/info` | ❌ |
| GET | `/protected/profile` | ✅ |
| GET | `/protected/dashboard` | ✅ |
| POST | `/auth/logout` | ✅ |
| GET | `/` | ❌ |
| GET | `/health` | ❌ |
| GET | `/tasks` | ❌ |
| GET | `/tasks/{task_id}` | ❌ |
| POST | `/tasks` | ❌ |
| PUT | `/tasks/{task_id}` | ❌ |
| DELETE | `/tasks/{task_id}` | ❌ |
| GET | `/stats` | ❌ |
| POST | `/reset` | ❌ |

## `ai-version/main.py`

| Method | Path | Requires `Depends(auth.get_current_user)` |
|---|---|---|
| POST | `/auth/signup` | ❌ |
| POST | `/auth/login` | ❌ |
| GET | `/public/info` | ❌ |
| GET | `/protected/profile` | ❌ (uses its own `Depends(get_user)` instead) |
| GET | `/protected/dashboard` | ❌ (uses its own `Depends(get_user)` instead) |
| POST | `/auth/logout` | ❌ (uses its own `Depends(get_user)` instead) |

## Security note

In `main.py`, every task endpoint is open to anyone without logging in, so any caller can create, edit or delete tasks, or wipe the whole table with `POST /reset` (which runs `TRUNCATE` in `db.py`), and tasks aren't tied to a user either.
