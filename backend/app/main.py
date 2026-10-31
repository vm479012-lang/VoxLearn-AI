"""
VoxLearn AI - FastAPI Application Main Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .data.seed import seed_database
from .routers import auth_user, dashboard, tutor, quiz, mastery, practice

# Create DB tables on startup
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure Class 10 Physics content and baseline learner state are seeded
    seed_database()
    yield
    # Shutdown logic if any

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered adaptive learning web application with Socratic voice tutor and Bayesian Knowledge Tracing learner model.",
    lifespan=lifespan
)

# Enable CORS for React frontend & Wispr Flow client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth_user.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)
app.include_router(tutor.router, prefix=settings.API_V1_STR)
app.include_router(quiz.router, prefix=settings.API_V1_STR)
app.include_router(mastery.router, prefix=settings.API_V1_STR)
app.include_router(practice.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "app": "VoxLearn AI",
        "description": "AI Prep Tutor with Learner Model",
        "version": settings.VERSION,
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "VoxLearn AI Backend"}
