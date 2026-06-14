from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.expense import Expense
from app.models.category import Category
from app.models.user import User


def create_expense(
    db: Session,
    amount: float,
    description: str,
    expense_date,
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

    expense = Expense(
        amount=amount,
        description=description,
        expense_date=expense_date,
        category_id=category_id,
        user_id=current_user.id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expenses(
    db: Session,
    current_user: User
):

    return (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id
        )
        .all()
    )