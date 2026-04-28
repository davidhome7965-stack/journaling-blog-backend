import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Database imports
from app.database.postgres import engine, Base

# Route imports
from app.routes.posts import router as posts_router
from app.routes.auth import router as auth_router
from app.routes.upload import router as upload_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Journaling Blog API",
    description="Backend API for the Journaling Techniques blog",
    version="1.0.0",
)

# Database initialization (startup event)
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created (if not exist)")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(upload_router)

# Static files for uploads
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Journaling Blog API is running", "docs": "/docs"}