from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.tutor import router as tutor_router
from .api.vision import router as vision_router
from .api.assessment import router as assessment_router
from .api.learning import router as learning_router
from .api.teacher import router as teacher_router
from .api.collaboration import router as collaboration_router
from .api.ai_status import router as ai_status_router
from .routes.auth_routes import router as auth_router
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="LearnSync AI Backend Services — Connecting Every Learner to Smarter Learning."
)

# CORS Middleware setup for mobile & browser preview access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tutor_router)
app.include_router(vision_router)
app.include_router(assessment_router)
app.include_router(learning_router)
app.include_router(teacher_router)
app.include_router(collaboration_router)
app.include_router(ai_status_router)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
