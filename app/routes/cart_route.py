from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.schemas.cart_schema import (
    AddCart
)

from app.controllers import (
    cart_controller
)

from app.utils.auth_middleware import (
    get_current_user
)

router = APIRouter()


# DATABASE
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ADD TO CART
@router.post("/cart")
def add_to_cart(
    cart: AddCart,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return cart_controller.add_to_cart(
        db,
        cart,
        current_user
    )


# GET USER CART
@router.get("/cart")
def get_cart(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return cart_controller.get_user_cart(
        db,
        current_user
    )


# REMOVE CART ITEM
@router.delete("/cart/{cart_id}")
def remove_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return cart_controller.remove_cart_item(
        db,
        cart_id,
        current_user
    )