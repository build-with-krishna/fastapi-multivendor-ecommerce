from sqlalchemy.orm import Session

from app.models.wishlist_model import Wishlist
from app.models.product_model import Product


# ADD TO WISHLIST
def add_to_wishlist(
    db: Session,
    wishlist,
    current_user
):

    product = db.query(Product).filter(
        Product.id == wishlist.product_id
    ).first()

    if not product:

        return {
            "error": "Product not found"
        }

    existing = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == wishlist.product_id
    ).first()

    if existing:

        return {
            "message": "Already in wishlist"
        }

    new_item = Wishlist(
        user_id=current_user.id,
        product_id=wishlist.product_id
    )

    db.add(new_item)

    db.commit()

    return {
        "message": "Added to wishlist"
    }


# GET WISHLIST
def get_wishlist(
    db: Session,
    current_user
):

    items = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id
    ).all()

    data = []

    for item in items:

        data.append({
            "wishlist_id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "price": item.product.price,
            "image": item.product.image
        })

    return data


# REMOVE WISHLIST
def remove_wishlist(
    db: Session,
    wishlist_id: int,
    current_user
):

    item = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == current_user.id
    ).first()

    if not item:

        return {
            "error": "Wishlist item not found"
        }

    db.delete(item)

    db.commit()

    return {
        "message": "Wishlist item removed"
    }