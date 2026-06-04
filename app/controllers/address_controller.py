from sqlalchemy.orm import Session

from app.models.address_model import Address


# ADD ADDRESS
def add_address(
    db: Session,
    address,
    current_user
):

    new_address = Address(
        user_id=current_user.id,
        full_name=address.full_name,
        mobile=address.mobile,
        address_line=address.address_line,
        city=address.city,
        state=address.state,
        pincode=address.pincode,
        country=address.country
    )

    db.add(new_address)

    db.commit()

    db.refresh(new_address)

    return {
        "message": "Address added"
    }


# GET ADDRESSES
def get_addresses(
    db: Session,
    current_user
):

    return db.query(Address).filter(
        Address.user_id == current_user.id
    ).all()