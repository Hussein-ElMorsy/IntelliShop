from sqlalchemy import func, select
from sqlalchemy.orm import Session
from decimal import Decimal
from math import ceil
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductListResponse,
)
from app.schemas.product import ProductListResponse
from app.schemas.product_query import (
    ProductSortField,
    SortOrder,
)

def category_exists(
    db: Session,
    category_id: int,
) -> bool:
    category = db.get(
        Category,
        category_id,
    )

    return category is not None

def create_product(
    db: Session,
    product_data: ProductCreate,
) -> Product:

    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock_quantity=product_data.stock_quantity,
        category_id=product_data.category_id,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:

    return db.get(
        Product,
        product_id,
    )


def get_products(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    category_id: int | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    in_stock: bool | None = None,
    is_active: bool | None = True,
    sort_by: ProductSortField = ProductSortField.name,
    sort_order: SortOrder = SortOrder.asc,
) -> ProductListResponse:

    filters = []

    if search:
        filters.append(
            Product.name.ilike(f"%{search}%")
        )

    if category_id is not None:
        filters.append(
            Product.category_id == category_id
        )

    if min_price is not None:
        filters.append(
            Product.price >= min_price
        )

    if max_price is not None:
        filters.append(
            Product.price <= max_price
        )

    if in_stock is True:
        filters.append(
            Product.stock_quantity > 0
        )

    if is_active is not None:
        filters.append(
            Product.is_active == is_active
        )

    count_statement = (
        select(func.count())
        .select_from(Product)
        .where(*filters)
    )

    total = db.scalar(count_statement) or 0

    statement = (
        select(Product)
        .where(*filters)
    )

    if sort_by == ProductSortField.price:
        sort_column = Product.price
    else:
        sort_column = Product.name

    if sort_order == SortOrder.desc:
        statement = statement.order_by(
            sort_column.desc()
        )
    else:
        statement = statement.order_by(
            sort_column.asc()
        )

    offset = (page - 1) * page_size

    statement = (
        statement
        .offset(offset)
        .limit(page_size)
    )

    result = db.execute(statement)

    products = list(
        result.scalars().all()
    )

    total_pages = (
        ceil(total / page_size)
        if total > 0
        else 0
    )

    return ProductListResponse(
        items=products,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


def update_product(
    db: Session,
    product: Product,
    product_data: ProductUpdate,
) -> Product:

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            product,
            field,
            value,
        )

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product,
) -> None:

    db.delete(product)

    db.commit()