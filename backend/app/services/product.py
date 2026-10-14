from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
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
    offset: int = 0,
    limit: int = 20,
    category_id: int | None = None,
    is_active: bool | None = True,
) -> list:
    statement = select(Product)

    if category_id is not None:
        statement = statement.where(
            Product.category_id == category_id
        )

    if is_active is not None:
        statement = statement.where(
            Product.is_active == is_active
        )

    statement = (
        statement
        .order_by(Product.id)
        .offset(offset)
        .limit(limit)
    )

    result = db.execute(statement)

    return list(
        result.scalars().all()
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