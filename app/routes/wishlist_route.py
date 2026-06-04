from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.schemas.wishlist_schema import (
    WishlistCreate
)

from app.controllers import (
    wishlist_controller
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


# ADD WISHLIST
@router.post("/wishlist")
def add_wishlist(
    wishlist: WishlistCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return wishlist_controller.add_to_wishlist(
        db,
        wishlist,
        current_user
    )


# GET WISHLIST
@router.get("/wishlist")
def get_wishlist(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return wishlist_controller.get_wishlist(
        db,
        current_user
    )


# REMOVE WISHLIST
@router.delete("/wishlist/{wishlist_id}")
def remove_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return wishlist_controller.remove_wishlist(
        db,
        wishlist_id,
        current_user
    )