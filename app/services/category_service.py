from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User

from fastapi import HTTPException
from typing import Optional

def create_category(db: Session, name: str, current_user: User):

    category = Category(name=name, user_id=current_user.id)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
):
    offset = (page - 1) * limit

    query = db.query(Category).filter(
        Category.user_id == user_id
    )

    if search:
        query = query.filter(
            Category.name.ilike(f"%{search}%")
        )

    total = query.count()

    categories = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": categories,
        "total": total,
        "page": page,
        "limit": limit,
    }

def update_category(db: Session, category_id: int, name: str, current_user: User):

    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = name

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category_id: int, current_user: User):

    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}
