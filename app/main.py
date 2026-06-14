from fastapi import FastAPI

from app.core.config import settings
from app.db.database import Base, engine
from app.api.auth import router as auth_router

import app.models

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

app.include_router(auth_router)

@app.get("/")
def health_check():
    return {
        "status": "success",
        "message": "ExpenseWise API Running"
    }