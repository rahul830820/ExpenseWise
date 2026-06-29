from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.category import Category
from app.models.user import User
from app.schemas.dashboard_period import DashboardPeriod
from app.utils.date_filters import get_period_dates

def get_category_wise_report(
    db: Session,
    current_user: User,
    period: DashboardPeriod,
):

    start_date, end_date = get_period_dates(period)
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
    results = (
    category_query
    .group_by(Category.name)
    .all()
)

    return results


def get_monthly_report(
    db: Session,
    current_user: User,
    period: DashboardPeriod,
):
    
    start_date, end_date = get_period_dates(period)

    monthly_query = (
    db.query(
        extract("year", Expense.expense_date).label("year"),
        extract("month", Expense.expense_date).label("month"),
        func.sum(Expense.amount).label("total"),
    )
    .filter(
        Expense.user_id == current_user.id
    )
)
    
    if start_date:
        monthly_query = monthly_query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )

    results = (
    monthly_query
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


def get_top_categories(
    db: Session,
    current_user: User,
    period: DashboardPeriod,
):
    start_date, end_date = get_period_dates(period)
    top_category_query = (
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
        top_category_query = top_category_query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )

    results = (
    top_category_query
    .group_by(Category.name)
    .order_by(
        func.sum(Expense.amount).desc()
    )
    .all()
)
    return results
