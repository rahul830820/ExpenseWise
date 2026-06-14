from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User

from fastapi import HTTPException


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



def update_category(
    db: Session,
    category_id: int,
    name: str,
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

    category.name = name

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
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

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully"
    }