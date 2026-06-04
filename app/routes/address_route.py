from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.schemas.address_schema import (
    AddressCreate
)

from app.controllers import (
    address_controller
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


# ADD ADDRESS
@router.post("/addresses")
def add_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return address_controller.add_address(
        db,
        address,
        current_user
    )


# GET ADDRESSES
@router.get("/addresses")
def get_addresses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return address_controller.get_addresses(
        db,
        current_user
    )