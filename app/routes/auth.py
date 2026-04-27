from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import hashlib
import time

load_dotenv()
router = APIRouter(prefix="/auth", tags=["auth"])

ADMIN_PASSWORD_HASH = hashlib.sha256(os.getenv("ADMIN_PASSWORD", "admin123").encode()).hexdigest()

# Simple in-memory token (for production use JWT)
_tokens: dict[str, float] = {}

class LoginRequest(BaseModel):
    password: str

@router.post("/login")
async def login(req: LoginRequest):
    pwd_hash = hashlib.sha256(req.password.encode()).hexdigest()
    if pwd_hash != ADMIN_PASSWORD_HASH:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token = hashlib.sha256(f"{req.password}{time.time()}".encode()).hexdigest()[:32]
    _tokens[token] = time.time() + 86400  # 24 hours
    return {"token": token}

def verify_token(token: str) -> bool:
    if token not in _tokens:
        return False
    if _tokens[token] < time.time():
        del _tokens[token]
        return False
    return True