from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.income import IncomeCreate, IncomeResponse

from app.schemas.pagination import PaginatedResponse
from app.schemas.income import IncomeResponse

from app.services.income_service import (
    create_income,
    get_incomes as get_incomes_service,
)
from app.schemas.pagination import PaginatedResponse
from datetime import date
from typing import Literal, Optional

router = APIRouter(prefix="/incomes", tags=["Incomes"])


@router.post("", response_model=IncomeResponse, status_code=201)
def create_new_income(
    income_data: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_income(
        db=db,
        amount=income_data.amount,
        source=income_data.source,
        income_date=income_data.income_date,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=PaginatedResponse[IncomeResponse]
)
def get_incomes(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    sort_by: Optional[
    Literal["amount", "income_date"]
    ] = Query(None),
    order: Literal["asc", "desc"] = Query("desc"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if (
        start_date
        and end_date
        and start_date > end_date
):
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date",
        )
    return get_incomes_service(
        db=db,
        user_id=current_user.id,
        page=page,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        order=order,
    )