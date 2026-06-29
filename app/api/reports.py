from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.report import CategoryWiseReport, MonthlyReport, TopCategoryReport
from app.schemas.dashboard_period import DashboardPeriod
from app.services.report_service import (
    get_monthly_report,
    get_top_categories,
    get_category_wise_report,
)

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/category-wise", response_model=list[CategoryWiseReport])
def category_wise_report(
    period: DashboardPeriod = DashboardPeriod.MONTH,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_category_wise_report(
        db=db,
        current_user=current_user,
        period=period,
    )


@router.get("/monthly", response_model=list[MonthlyReport])
def monthly_report(
    period: DashboardPeriod = DashboardPeriod.MONTH,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_monthly_report(
        db=db,
        current_user=current_user,
        period=period,
    )


@router.get("/top-categories", response_model=list[TopCategoryReport])
def top_categories_report(
    period: DashboardPeriod = DashboardPeriod.MONTH,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_top_categories(
        db=db,
        current_user=current_user,
        period=period,
    )
