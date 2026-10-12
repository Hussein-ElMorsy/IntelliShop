from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


def create_category(
    db: Session,
    category_data: CategoryCreate,
) -> Category:
    category = Category(
        name=category_data.name,
        description=category_data.description,
    )

    db.add(category)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(category)

    return category


def get_categories(
    db: Session,
) -> list:
    statement = select(Category).order_by(Category.name)

    result = db.execute(statement)

    return list(result.scalars().all())


def get_category_by_id(
    db: Session,
    category_id: int,
) -> Category | None:
    return db.get(Category, category_id)


def update_category(
    db: Session,
    category: Category,
    category_data: CategoryUpdate,
) -> Category:
    update_data = category_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(category, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category: Category,
) -> None:
    db.delete(category)
    db.commit()