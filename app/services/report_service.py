from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.category import Category
from app.models.user import User


def get_category_wise_report(db: Session, current_user: User):

    results = (
        db.query(
            Category.name.label("category"), func.sum(Expense.amount).label("total")
        )
        .join(Expense, Expense.category_id == Category.id)
        .filter(Expense.user_id == current_user.id)
        .group_by(Category.name)
        .all()
    )

    return results


def get_monthly_report(db: Session, current_user: User):

    results = (
        db.query(
            extract("year", Expense.expense_date).label("year"),
            extract("month", Expense.expense_date).label("month"),
            func.sum(Expense.amount).label("total"),
        )
        .filter(Expense.user_id == current_user.id)
        .group_by(
            extract("year", Expense.expense_date),
            extract("month", Expense.expense_date),
        )
        .order_by(
            extract("year", Expense.expense_date),
            extract("month", Expense.expense_date),
        )
        .all()
    )

    return [
        {"month": f"{int(r.year)}-{int(r.month):02d}", "total": float(r.total)}
        for r in results
    ]


def get_top_categories(db: Session, current_user: User):

    results = (
        db.query(
            Category.name.label("category"), func.sum(Expense.amount).label("total")
        )
        .join(Expense, Expense.category_id == Category.id)
        .filter(Expense.user_id == current_user.id)
        .group_by(Category.name)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    return results
