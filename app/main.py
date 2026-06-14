from fastapi import FastAPI

from app.core.config import settings
from app.db.database import Base, engine
from app.api.auth import router as auth_router
from app.api.users import router as users_router

from app.models.user import User
from app.models.category import Category

from app.api.categories import router as categories_router

from app.api.expenses import router as expenses_router


# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(expenses_router)

@app.get("/")
def health_check():
    return {
        "status": "success",
        "message": "ExpenseWise API Running"
    }