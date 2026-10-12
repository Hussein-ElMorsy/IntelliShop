from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category import (
    create_category,
    delete_category,
    get_categories,
    get_category_by_id,
    update_category,
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
    try:
        return create_category(
            db=db,
            category_data=category_data,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A category with this name already exists.",
        )

@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories_endpoint(
    db: Session = Depends(get_db),
) -> list:
    return get_categories(db)

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    category = get_category_by_id(
        db=db,
        category_id=category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return category

@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category_endpoint(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    category = get_category_by_id(
        db=db,
        category_id=category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    try:
        return update_category(
            db=db,
            category=category,
            category_data=category_data,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A category with this name already exists.",
        )

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
) -> Response:
    category = get_category_by_id(
        db=db,
        category_id=category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    delete_category(
        db=db,
        category=category,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )