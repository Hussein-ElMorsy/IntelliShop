from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
)
from app.services.category import (
    create_category,
    get_categories,
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category_endpoint(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryResponse:

    return create_category(
        db=db,
        category_data=category_data,
    )

@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories_endpoint(
    db: Session = Depends(get_db),
) -> list:
    return get_categories(db)