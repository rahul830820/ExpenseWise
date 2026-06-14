from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.category import (
    CategoryCreate,
    CategoryResponse
)

from app.services.category_service import (
    create_category,
    get_categories,
    update_category,
    delete_category
)

from app.services.category_service import (
    create_category,
    get_categories
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=201
)
def create_new_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_category(
        db=db,
        name=category_data.name,
        current_user=current_user
    )


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def get_all_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_categories(
        db=db,
        current_user=current_user
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_existing_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_category(
        db=db,
        category_id=category_id,
        name=category_data.name,
        current_user=current_user
    )

@router.delete(
    "/{category_id}"
)
def delete_existing_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_category(
        db=db,
        category_id=category_id,
        current_user=current_user
    )