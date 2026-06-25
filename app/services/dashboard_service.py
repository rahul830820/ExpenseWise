from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from app.utils.date_filters import get_period_dates
from app.models.expense import Expense
from app.models.category import Category
from app.models.user import User
from app.models.income import Income
from app.schemas.dashboard_period import DashboardPeriod

def get_dashboard_summary(db: Session, 
                          current_user: User, 
                          period: DashboardPeriod):

    start_date, end_date = get_period_dates(period)
    income_query = (
    db.query(func.coalesce(func.sum(Income.amount), 0))
    .filter(Income.user_id == current_user.id)
    )

    if start_date:
        income_query = income_query.filter(
            Income.income_date >= start_date,
            Income.income_date <= end_date,
        )

    total_income = income_query.scalar()

    expense_query = (
    db.query(func.coalesce(func.sum(Expense.amount), 0))
    .filter(Expense.user_id == current_user.id)
    )

    if start_date:
        expense_query = expense_query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )

    total_expenses = expense_query.scalar()

    expense_count_query = (
    db.query(Expense)
    .filter(Expense.user_id == current_user.id)
    )

    if start_date:
        expense_count_query = expense_count_query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )

    expense_count = expense_count_query.count()

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

def get_recent_expenses(
    db: Session,
    current_user: User,
    limit: int = 5,
):
    return (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id
        )
        .order_by(
            Expense.expense_date.desc(),
            Expense.id.desc()
        )
        .limit(limit)
        .all()
    )

def get_dashboard_charts(
    db: Session,
    current_user: User,
    period: DashboardPeriod,
):
    start_date, end_date = get_period_dates(period)
    expense_trend_query = (
        db.query(
            func.to_char(
                Expense.expense_date,
                "YYYY-MM",
            ).label("month"),
            func.sum(
                Expense.amount
            ).label("total"),
        )
        .filter(
            Expense.user_id == current_user.id
        )
    )
    if start_date:
        expense_trend_query = (
            expense_trend_query.filter(
                Expense.expense_date >= start_date,
                Expense.expense_date <= end_date,
            )
        )
    expense_trend = (
    expense_trend_query
    .group_by("month")
    .order_by("month")
    .all()
)

    category_query = (
        db.query(
            Category.name.label("category"),
            func.sum(Expense.amount).label("total"),
        )
        .join(
            Expense,
            Expense.category_id == Category.id,
        )
        .filter(
            Expense.user_id == current_user.id
        )
    )

    if start_date:
        category_query = category_query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )

    category_distribution = (
    category_query
    .group_by(Category.name)
    .order_by(
        func.sum(Expense.amount).desc()
    )
    .all()
)

    return {
        "expense_trend": expense_trend,
        "category_distribution": category_distribution,
    }