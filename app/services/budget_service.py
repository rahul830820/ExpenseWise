from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.models.user import User

from sqlalchemy import func

from app.models.expense import Expense

def create_budget(
    db: Session,
    amount: float,
    category_id: int,
    current_user: User
):

    category = (
        db.query(Category)
        .filter(
            Category.id == category_id,
            Category.user_id == current_user.id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    existing_budget = (
        db.query(Budget)
        .filter(
            Budget.category_id == category_id,
            Budget.user_id == current_user.id
        )
        .first()
    )

    if existing_budget:
        raise HTTPException(
            status_code=400,
            detail="Budget already exists for this category"
        )

    budget = Budget(
        amount=amount,
        category_id=category_id,
        user_id=current_user.id
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    return budget


def get_budgets(
    db: Session,
    current_user: User
):

    return (
        db.query(Budget)
        .filter(
            Budget.user_id == current_user.id
        )
        .all()
    )

def get_budget_analysis(
    db: Session,
    current_user: User
):

    budgets = (
        db.query(Budget)
        .filter(
            Budget.user_id == current_user.id
        )
        .all()
    )

    results = []

    for budget in budgets:

        spent = (
            db.query(
                func.coalesce(
                    func.sum(Expense.amount),
                    0
                )
            )
            .filter(
                Expense.category_id == budget.category_id,
                Expense.user_id == current_user.id
            )
            .scalar()
        )

        remaining = budget.amount - spent

        status = (
            "Within Budget"
            if remaining >= 0
            else "Over Budget"
        )

        results.append(
            {
                "category": budget.category.name,
                "budget": budget.amount,
                "spent": spent,
                "remaining": remaining,
                "status": status
            }
        )

    return results