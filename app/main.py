import sys
print("Python path:", sys.path)
print("Current directory files:", os.listdir("."))
print("App directory files:", os.listdir("app"))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os


from app.database.postgres import engine, Base

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# सही import – routes app के अंदर है
from app.routes.posts import router as posts_router
from app.routes.auth import router as auth_router
from app.routes.upload import router as upload_router

load_dotenv()

app = FastAPI(
    title="Journaling Blog API",
    description="Backend API for the Journaling Techniques blog",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(upload_router)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



@app.get("/")
async def root():
    return {"message": "Journaling Blog API is running", "docs": "/docs"}

