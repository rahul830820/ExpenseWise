from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.category import Category
from app.models.user import User
from app.models.income import Income


def get_dashboard_summary(db: Session, current_user: User):

    total_income = (
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == current_user.id)
        .scalar()
    )

    total_expenses = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == current_user.id)
        .scalar()
    )

    expense_count = db.query(Expense).filter(Expense.user_id == current_user.id).count()

    category_count = (
        db.query(Category).filter(Category.user_id == current_user.id).count()
    )

    savings = total_income - total_expenses

    if total_income > 0:
        savings_rate = (savings / total_income) * 100
    else:
        savings_rate = 0

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings,
        "savings_rate": round(savings_rate, 2),
        "expense_count": expense_count,
        "category_count": category_count,
    }
