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
    CartResponse,
)
from app.services.cart import (
    add_item_to_cart,
    build_cart_response,
    get_cart_with_items,
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