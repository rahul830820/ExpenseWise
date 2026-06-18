from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.user import User


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


def get_incomes(db: Session, current_user: User):

    return db.query(Income).filter(Income.user_id == current_user.id).all()
