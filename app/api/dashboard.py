from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.dashboard import DashboardSummary, RecentExpense

from app.services.dashboard_service import (
    get_dashboard_summary,
    get_recent_expenses,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_dashboard_summary(db=db, current_user=current_user)

@router.get(
    "/recent-expenses",
    response_model=list[RecentExpense],
)
def recent_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_recent_expenses(
        db=db,
        current_user=current_user,
    )
