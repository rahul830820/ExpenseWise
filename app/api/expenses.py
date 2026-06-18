from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.expense import ExpenseCreate, ExpenseResponse

from app.services.expense_service import (
    create_expense,
    get_expenses,
    update_expense,
    delete_expense,
)

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_new_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_expense(
        db=db,
        amount=expense_data.amount,
        description=expense_data.description,
        expense_date=expense_data.expense_date,
        category_id=expense_data.category_id,
        current_user=current_user,
    )


@router.get("", response_model=list[ExpenseResponse])
def get_all_expenses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_expenses(db=db, current_user=current_user)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_existing_expense(
    expense_id: int,
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_expense(
        db=db,
        expense_id=expense_id,
        amount=expense_data.amount,
        description=expense_data.description,
        expense_date=expense_data.expense_date,
        category_id=expense_data.category_id,
        current_user=current_user,
    )


@router.delete("/{expense_id}")
def delete_existing_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_expense(db=db, expense_id=expense_id, current_user=current_user)
