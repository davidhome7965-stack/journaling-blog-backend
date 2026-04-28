import os
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

# Load environment variables (must be before using os.getenv)
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Journaling Blog API",
    description="Backend API for the Journaling Techniques blog",
    version="1.0.0",
)

# ---------- Database initialization ----------
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created (if not exist)")

# ---------- CORS configuration ----------
# Read CORS_ORIGINS from environment variable, split by comma, and strip whitespace
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]
print(f"CORS allowed origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,          # List of allowed origins
    allow_credentials=True,              # Allow cookies/auth headers
    allow_methods=["*"],                 # Allow all HTTP methods (including OPTIONS)
    allow_headers=["*"],                 # Allow all headers
)

# ---------- Include routers ----------
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(upload_router)

# ---------- Static files for uploads ----------
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ---------- Root endpoint ----------
@app.get("/")
async def root():
    return {"message": "Journaling Blog API is running", "docs": "/docs"}