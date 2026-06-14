from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.category import Category
from app.models.user import User


def get_dashboard_summary(
    db: Session,
    current_user: User
):

    total_expenses = (
        db.query(
            func.coalesce(
                func.sum(Expense.amount),
                0
            )
        )
        .filter(
            Expense.user_id == current_user.id
        )
        .scalar()
    )

    expense_count = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id
        )
        .count()
    )

    category_count = (
        db.query(Category)
        .filter(
            Category.user_id == current_user.id
        )
        .count()
    )

    return {
        "total_expenses": total_expenses,
        "expense_count": expense_count,
        "category_count": category_count
    }