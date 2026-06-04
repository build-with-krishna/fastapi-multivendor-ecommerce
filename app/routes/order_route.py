from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.controllers import (
    order_controller
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


# PLACE ORDER
@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return order_controller.place_order(
        db,
        current_user
    )


# USER ORDERS
@router.get("/my-orders")
def my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return order_controller.user_orders(
        db,
        current_user
    )


# VENDOR ORDERS
@router.get("/vendor-orders")
def vendor_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return order_controller.vendor_orders(
        db,
        current_user
    )


# UPDATE ORDER STATUS
@router.put("/orders/{order_id}/status")
def update_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return order_controller.update_order_status(
        db,
        order_id,
        status,
        current_user
    )