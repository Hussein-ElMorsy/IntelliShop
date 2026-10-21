from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
)
from app.services.cart import (
    add_item_to_cart,
    build_cart_response,
    clear_cart,
    get_cart_with_items,
    remove_cart_item,
    update_cart_item_quantity,
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)

@router.get(
    "",
    response_model=CartResponse,
)
def get_my_cart(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
) -> CartResponse:

    cart = get_cart_with_items(
        db=db,
        user_id=current_user.id,
    )

    return build_cart_response(cart)


@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_cart_item(
    item_data: CartItemCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
) -> CartResponse:

    try:
        cart = add_item_to_cart(
            db=db,
            user_id=current_user.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
        )

    except ValueError as error:

        if str(error) == "PRODUCT_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        if str(error) == "PRODUCT_INACTIVE":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product is not available.",
            )

        if str(error) == "INSUFFICIENT_STOCK":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Insufficient product stock.",
            )

        raise

    return build_cart_response(cart)


@router.patch(
    "/items/{item_id}",
    response_model=CartResponse,
)
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
) -> CartResponse:

    try:
        cart = update_cart_item_quantity(
            db=db,
            user_id=current_user.id,
            item_id=item_id,
            quantity=item_data.quantity,
        )

    except ValueError as error:
        error_code = str(error)

        if error_code == "CART_ITEM_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found.",
            )

        if error_code == "PRODUCT_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        if error_code == "PRODUCT_INACTIVE":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product is not available.",
            )

        if error_code == "INSUFFICIENT_STOCK":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Insufficient product stock.",
            )

        raise

    return build_cart_response(cart)


@router.delete(
    "/items/{item_id}",
    response_model=CartResponse,
) 
def delete_cart_item(
    item_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
) -> CartResponse:

    try:
        cart = remove_cart_item(
            db=db,
            user_id=current_user.id,
            item_id=item_id,
        )

    except ValueError as error:
        if str(error) == "CART_ITEM_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found.",
            )

        raise

    return build_cart_response(cart)

@router.delete(
    "",
    response_model=CartResponse,
)
def clear_my_cart(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
) -> CartResponse:

    cart = clear_cart(
        db=db,
        user_id=current_user.id,
    )

    return build_cart_response(cart)