from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.pagination import PaginatedResponse
from app.schemas.category import CategoryCreate, CategoryResponse

from app.services.category_service import (
    create_category,
    get_categories  as get_categories_service,
    update_category,
    delete_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse, status_code=201)
def create_new_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_category(db=db, name=category_data.name, current_user=current_user)


@router.get(
    "",
    response_model=PaginatedResponse[CategoryResponse]
)
def read_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_categories_service(
        db=db,
        user_id=current_user.id,
        page=page,
        limit=limit,
    )


@router.put("/{category_id}", response_model=CategoryResponse)
def update_existing_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_category(
        db=db,
        category_id=category_id,
        name=category_data.name,
        current_user=current_user,
    )


@router.delete("/{category_id}")
def delete_existing_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_category(db=db, category_id=category_id, current_user=current_user)
