from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.dashboard_period import DashboardPeriod
from app.schemas.dashboard import (
    DashboardSummary,
    DashboardCharts,
    RecentExpense,
)

from app.services.dashboard_service import (
    get_dashboard_summary,
    get_recent_expenses,
    get_dashboard_charts,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    period: DashboardPeriod = DashboardPeriod.MONTH,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_dashboard_summary(
    db=db,
    current_user=current_user,
    period=period,
)

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

@router.get(
    "/charts",
    response_model=DashboardCharts,
)
def dashboard_charts(
    period: DashboardPeriod = DashboardPeriod.MONTH,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_dashboard_charts(
        db=db,
        current_user=current_user,
        period=period,
    )
