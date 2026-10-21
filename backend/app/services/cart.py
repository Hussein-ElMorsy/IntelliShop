from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.schemas.cart import (
    CartItemResponse,
    CartResponse,
)

def get_or_create_cart(
    db: Session,
    user_id: int,
) -> Cart:

    statement = (
        select(Cart)
        .where(Cart.user_id == user_id)
    )

    cart = db.scalar(statement)

    if cart is not None:
        return cart

    cart = Cart(
        user_id=user_id
    )

    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart


def get_cart_with_items(
    db: Session,
    user_id: int,
) -> Cart:

    cart = get_or_create_cart(
        db=db,
        user_id=user_id,
    )

    statement = (
        select(Cart)
        .options(
            selectinload(Cart.items)
            .selectinload(CartItem.product)
        )
        .where(Cart.id == cart.id)
    )

    return db.scalar(statement)


def build_cart_response(
    cart: Cart,
) -> CartResponse:

    items = []

    total_items = 0
    total_price = Decimal("0.00")

    for item in cart.items:
        subtotal = (
            item.product.price
            * item.quantity
        )

        items.append(
            CartItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.product.price,
                subtotal=subtotal,
            )
        )

        total_items += item.quantity
        total_price += subtotal

    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=items,
        total_items=total_items,
        total_price=total_price,
    )


def add_item_to_cart(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int,
) -> Cart:

    product = db.get(
        Product,
        product_id,
    )

    if product is None:
        raise ValueError(
            "PRODUCT_NOT_FOUND"
        )

    if not product.is_active:
        raise ValueError(
            "PRODUCT_INACTIVE"
        )

    if product.stock_quantity < quantity:
        raise ValueError(
            "INSUFFICIENT_STOCK"
        )

    cart = get_or_create_cart(
        db=db,
        user_id=user_id,
    )

    statement = select(CartItem).where(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id,
    )

    existing_item = db.scalar(statement)

    if existing_item is not None:
        new_quantity = (
            existing_item.quantity
            + quantity
        )

        if product.stock_quantity < new_quantity:
            raise ValueError(
                "INSUFFICIENT_STOCK"
            )

        existing_item.quantity = new_quantity

    else:
        db.add(
            CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
            )
        )

    db.commit()

    return get_cart_with_items(
        db=db,
        user_id=user_id,
    )

def get_cart_item(
    db: Session,
    user_id: int,
    item_id: int,
) -> CartItem | None:

    statement = (
        select(CartItem)
        .join(Cart)
        .where(
            CartItem.id == item_id,
            Cart.user_id == user_id,
        )
    )

    return db.scalar(statement)


def update_cart_item_quantity(
    db: Session,
    user_id: int,
    item_id: int,
    quantity: int,
) -> Cart:

    item = get_cart_item(
        db=db,
        user_id=user_id,
        item_id=item_id,
    )

    if item is None:
        raise ValueError(
            "CART_ITEM_NOT_FOUND"
        )

    product = db.get(
        Product,
        item.product_id,
    )

    if product is None:
        raise ValueError(
            "PRODUCT_NOT_FOUND"
        )

    if not product.is_active:
        raise ValueError(
            "PRODUCT_INACTIVE"
        )

    if product.stock_quantity < quantity:
        raise ValueError(
            "INSUFFICIENT_STOCK"
        )

    item.quantity = quantity

    db.commit()

    return get_cart_with_items(
        db=db,
        user_id=user_id,
    )

def remove_cart_item(
    db: Session,
    user_id: int,
    item_id: int,
) -> Cart:

    item = get_cart_item(
        db=db,
        user_id=user_id,
        item_id=item_id,
    )

    if item is None:
        raise ValueError(
            "CART_ITEM_NOT_FOUND"
        )

    db.delete(item)
    db.commit()

    return get_cart_with_items(
        db=db,
        user_id=user_id,
    )

def clear_cart(
    db: Session,
    user_id: int,
) -> Cart:

    cart = get_cart_with_items(
        db=db,
        user_id=user_id,
    )

    for item in cart.items:
        db.delete(item)

    db.commit()

    return get_cart_with_items(
        db=db,
        user_id=user_id,
    )