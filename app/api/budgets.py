from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services.budget_service import create_budget, get_budgets, get_budget_analysis

from app.schemas.budget import (
    BudgetCreate,
    BudgetResponse,
    BudgetAnalysis,
    BudgetUpdate,
)

from app.services.budget_service import (
    update_budget,
    delete_budget,
)

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("", response_model=BudgetResponse, status_code=201)
def create_new_budget(
    budget_data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_budget(
        db=db,
        amount=budget_data.amount,
        category_id=budget_data.category_id,
        current_user=current_user,
    )


@router.get("", response_model=list[BudgetResponse])
def get_all_budgets(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_budgets(db=db, current_user=current_user)


@router.get("/analysis", response_model=list[BudgetAnalysis])
def budget_analysis(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_budget_analysis(db=db, current_user=current_user)


@router.put("/{budget_id}", response_model=BudgetResponse)
def update_existing_budget(
    budget_id: int,
    budget_data: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_budget(
        db=db, budget_id=budget_id, amount=budget_data.amount, current_user=current_user
    )


@router.delete("/{budget_id}")
def delete_existing_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_budget(db=db, budget_id=budget_id, current_user=current_user)
