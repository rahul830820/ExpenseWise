from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.expense import Expense
from app.models.category import Category
from app.models.user import User
from datetime import date
from typing import Optional

def create_expense(
    db: Session,
    amount: float,
    description: str,
    expense_date,
    category_id: int,
    current_user: User,
):

    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    expense = Expense(
        amount=amount,
        description=description,
        expense_date=expense_date,
        category_id=category_id,
        user_id=current_user.id,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expenses(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 20,
    category_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    offset = (page - 1) * limit

    query = db.query(Expense).filter(
    Expense.user_id == user_id
)

    if category_id:
        query = query.filter(
            Expense.category_id == category_id
        )

    if start_date:
        query = query.filter(
            Expense.expense_date >= start_date
        )

    if end_date:
        query = query.filter(
            Expense.expense_date <= end_date
    )
        
    total = query.count()

    expenses = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": expenses,
        "total": total,
        "page": page,
        "limit": limit,
    }


def update_expense(
    db: Session,
    expense_id: int,
    amount: float,
    description: str,
    expense_date,
    category_id: int,
    current_user: User,
):

    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
        .first()
    )

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    expense.amount = amount
    expense.description = description
    expense.expense_date = expense_date
    expense.category_id = category_id

    db.commit()
    db.refresh(expense)

    return expense


def delete_expense(db: Session, expense_id: int, current_user: User):

    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
        .first()
    )

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}
