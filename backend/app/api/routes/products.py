from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session
from app.db.session import get_db
from decimal import Decimal
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.schemas.product_query import (
    ProductSortField,
    SortOrder,
)
from app.services.product import (
    category_exists,
    create_product,
    delete_product,
    get_product_by_id,
    get_products,
    update_product,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_endpoint(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductResponse:

    if not category_exists(
        db=db,
        category_id=product_data.category_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return create_product(
        db=db,
        product_data=product_data,
    )

@router.get(
    "",
    response_model=ProductListResponse,
)
def get_products_endpoint(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
    ),
    category_id: int | None = Query(
        default=None,
        gt=0,
    ),
    min_price: Decimal | None = Query(
        default=None,
        ge=0,
    ),
    max_price: Decimal | None = Query(
        default=None,
        ge=0,
    ),
    in_stock: bool | None = Query(
        default=None,
    ),
    is_active: bool | None = Query(
        default=True,
    ),
    sort_by: ProductSortField = Query(
        default=ProductSortField.name,
    ),
    sort_order: SortOrder = Query(
        default=SortOrder.asc,
    ),
    db: Session = Depends(get_db),
) -> ProductListResponse:

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="min_price cannot be greater than max_price.",
        )

    return get_products(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
) -> ProductResponse:

    product = get_product_by_id(
        db=db,
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
) -> ProductResponse:

    product = get_product_by_id(
        db=db,
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    if product_data.category_id is not None:
        if not category_exists(
            db=db,
            category_id=product_data.category_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

    return update_product(
        db=db,
        product=product,
        product_data=product_data,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
) -> Response:

    product = get_product_by_id(
        db=db,
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    delete_product(
        db=db,
        product=product,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

