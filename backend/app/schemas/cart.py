from decimal import Decimal
from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int = Field(
        gt=0
    )

    quantity: int = Field(
        default=1,
        ge=1,
        le=100,
    )


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        ge=1,
        le=100,
    )

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: list[CartItemResponse]
    total_items: int
    total_price: Decimal