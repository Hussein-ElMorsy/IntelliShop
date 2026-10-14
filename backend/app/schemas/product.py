from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    price: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    stock_quantity: int = Field(
        default=0,
        ge=0,
    )

    category_id: int = Field(
        gt=0,
    )


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    stock_quantity: int | None = Field(
        default=None,
        ge=0,
    )

    is_active: bool | None = None

    category_id: int | None = Field(
        default=None,
        gt=0,
    )


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    is_active: bool
    category_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int