from fastapi import FastAPI

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as users_router

from app.api.categories import router as categories_router

from app.api.expenses import router as expenses_router

from app.api.dashboard import router as dashboard_router

from app.api.reports import router as reports_router

from app.api.incomes import router as incomes_router

from app.api.budgets import router as budgets_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(dashboard_router)
app.include_router(reports_router)
app.include_router(incomes_router)
app.include_router(budgets_router)


@app.get("/")
def health_check():
    return {"status": "success", "message": "ExpenseWise API Running"}
