import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    # 🟢 अभी के लिए authentication हटाया – बाद में जोड़ेंगे
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files allowed")
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"url": f"/uploads/{safe_filename}"}