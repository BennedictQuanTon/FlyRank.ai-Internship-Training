import os
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Auth API")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
security = HTTPBearer()  # Notice: auto_error defaults to True, throwing 403 instead of 401 on missing header!

class UserCredentials(BaseModel):
    email: str
    password: str

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(creds: UserCredentials):
    # Flaw: Does not check for blank whitespace strings ("   ")
    try:
        res = supabase.auth.sign_up({"email": creds.email, "password": creds.password})
        return res.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
def login(creds: UserCredentials):
    try:
        res = supabase.auth.sign_in_with_password({"email": creds.email, "password": creds.password})
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

# Auth dependency
def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Flaw: Assumes credentials is always valid and does not check for malformed Bearer tokens manually
    token = credentials.credentials
    try:
        user_res = supabase.auth.get_user(token)
        return user_res.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/protected/profile")
def profile(user=Depends(get_user)):
    return user

@app.get("/protected/dashboard")
def dashboard(user=Depends(get_user)):
    return {"status": "ok", "user": user}

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user=Depends(get_user)):
    supabase.auth.sign_out()
    return None
