from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.user import User
from datetime import date
from typing import Optional


def create_income(
    db: Session, amount: float, source: str, income_date, current_user: User
):

    income = Income(
        amount=amount, source=source, income_date=income_date, user_id=current_user.id
    )

    db.add(income)
    db.commit()
    db.refresh(income)

    return income


def get_incomes(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 20,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    sort_by: Optional[str] = None,
    order: str = "desc",
):
    offset = (page - 1) * limit

    query = db.query(Income).filter(
        Income.user_id == user_id
    )

    if start_date:
        query = query.filter(
            Income.income_date >= start_date
        )

    if end_date:
        query = query.filter(
            Income.income_date <= end_date
        )

    if sort_by == "amount":
        if order == "asc":
            query = query.order_by(Income.amount.asc())
        else:
            query = query.order_by(Income.amount.desc())

    elif sort_by == "income_date":
        if order == "asc":
            query = query.order_by(Income.income_date.asc())
        else:
            query = query.order_by(Income.income_date.desc())

    total = query.count()

    incomes = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": incomes,
        "total": total,
        "page": page,
        "limit": limit,
    }