from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import roadmaps, ai, weeks, share, auth, recommendations

app = FastAPI(
    title="SkillSprint AI API",
    description="AI-powered learning roadmap generator",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(roadmaps.router)
app.include_router(ai.router)
app.include_router(weeks.router)
app.include_router(share.router)
app.include_router(recommendations.router)

@app.get("/")
async def root():
    return {"message": "SkillSprint AI API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "SkillSprint AI",
        "version": "1.0.0"
    }
