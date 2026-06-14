from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User


def create_category(
    db: Session,
    name: str,
    current_user: User
):

    category = Category(
        name=name,
        user_id=current_user.id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(
    db: Session,
    current_user: User
):

    return (
        db.query(Category)
        .filter(
            Category.user_id == current_user.id
        )
        .all()
    )