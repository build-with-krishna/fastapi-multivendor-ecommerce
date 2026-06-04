from sqlalchemy.orm import Session

from app.models.cart_model import Cart
from app.models.product_model import Product


# ADD TO CART
def add_to_cart(
    db: Session,
    cart,
    current_user
):

    product = db.query(Product).filter(
        Product.id == cart.product_id
    ).first()

    if not product:
        return {
            "error": "Product not found"
        }

    # CHECK EXISTING CART
    existing_cart = db.query(Cart).filter(
        Cart.user_id == current_user.id,
        Cart.product_id == cart.product_id
    ).first()

    if existing_cart:

        existing_cart.quantity += cart.quantity

        db.commit()

        return {
            "message": "Cart updated"
        }

    new_cart = Cart(
        user_id=current_user.id,
        product_id=cart.product_id,
        quantity=cart.quantity
    )

    db.add(new_cart)

    db.commit()

    db.refresh(new_cart)

    return {
        "message": "Product added to cart"
    }


# GET USER CART
def get_user_cart(
    db: Session,
    current_user
):

    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).all()

    total = 0

    data = []

    for item in cart_items:

        subtotal = (
            item.product.price * item.quantity
        )

        total += subtotal

        data.append({
            "cart_id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "cart_items": data,
        "grand_total": total
    }


# REMOVE CART ITEM
def remove_cart_item(
    db: Session,
    cart_id: int,
    current_user
):

    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart_item:
        return {
            "error": "Cart item not found"
        }

    db.delete(cart_item)

    db.commit()

    return {
        "message": "Cart item removed"
    }