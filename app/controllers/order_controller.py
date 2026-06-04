from sqlalchemy.orm import Session

from app.models.cart_model import Cart
from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.models.product_model import Product


# PLACE ORDER
def place_order(
    db: Session,
    current_user
):

    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).all()

    if not cart_items:
        return {
            "error": "Cart is empty"
        }

    grand_total = 0

    # CALCULATE TOTAL
    for item in cart_items:

        subtotal = (
            item.product.price * item.quantity
        )

        grand_total += subtotal

    # CREATE ORDER
    new_order = Order(
        user_id=current_user.id,
        total_amount=grand_total,
        status="pending"
    )

    db.add(new_order)

    db.commit()

    db.refresh(new_order)

    # CREATE ORDER ITEMS
    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        # STOCK CHECK
        if product.stock < item.quantity:

            return {
                "error": f"{product.name} out of stock"
            }

        subtotal = (
            product.price * item.quantity
        )

        order_item = OrderItem(
            order_id=new_order.id,
            vendor_id=product.vendor_id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
            subtotal=subtotal
        )

        db.add(order_item)

        # REDUCE STOCK
        product.stock -= item.quantity

    # CLEAR CART
    db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).delete()

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": new_order.id,
        "total_amount": grand_total
    }


# USER ORDERS
def user_orders(
    db: Session,
    current_user
):

    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()

    data = []

    for order in orders:

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        order_products = []

        for item in items:

            order_products.append({
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.subtotal
            })

        data.append({
            "order_id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
            "items": order_products
        })

    return data


# VENDOR ORDERS
def vendor_orders(
    db: Session,
    current_user
):

    items = db.query(OrderItem).filter(
        OrderItem.vendor_id == current_user.id
    ).all()

    data = []

    for item in items:

        data.append({
            "order_id": item.order_id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": item.price,
            "subtotal": item.subtotal
        })

    return data


# UPDATE ORDER STATUS
def update_order_status(
    db: Session,
    order_id: int,
    status: str,
    current_user
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:

        return {
            "error": "Order not found"
        }

    # ONLY ADMIN/VENDOR
    if current_user.role not in [
        "admin",
        "vendor"
    ]:

        return {
            "error": "Unauthorized"
        }

    order.status = status

    db.commit()

    return {
        "message": "Order status updated"
    }