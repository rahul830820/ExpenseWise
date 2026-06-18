from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.income import IncomeCreate, IncomeResponse

from app.services.income_service import create_income, get_incomes

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


@router.get("", response_model=list[IncomeResponse])
def get_all_incomes(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_incomes(db=db, current_user=current_user)
