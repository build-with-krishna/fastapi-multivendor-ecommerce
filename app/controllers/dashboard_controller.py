from sqlalchemy.orm import Session

from sqlalchemy import func

from app.models.user_model import User
from app.models.product_model import Product
from app.models.order_model import Order
from app.models.order_item_model import OrderItem


# ADMIN DASHBOARD
def admin_dashboard(
    db: Session,
    current_user
):

    if current_user.role != "admin":

        return {
            "error": "Unauthorized"
        }

    total_users = db.query(User).count()

    total_vendors = db.query(User).filter(
        User.role == "vendor"
    ).count()

    total_customers = db.query(User).filter(
        User.role == "customer"
    ).count()

    total_products = db.query(Product).count()

    total_orders = db.query(Order).count()

    total_sales = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    return {
        "total_users": total_users,
        "total_vendors": total_vendors,
        "total_customers": total_customers,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_sales": total_sales or 0
    }


# VENDOR DASHBOARD
def vendor_dashboard(
    db: Session,
    current_user
):

    if current_user.role != "vendor":

        return {
            "error": "Unauthorized"
        }

    total_products = db.query(Product).filter(
        Product.vendor_id == current_user.id
    ).count()

    total_orders = db.query(OrderItem).filter(
        OrderItem.vendor_id == current_user.id
    ).count()

    revenue = db.query(
        func.sum(OrderItem.subtotal)
    ).filter(
        OrderItem.vendor_id == current_user.id
    ).scalar()

    recent_orders = db.query(OrderItem).filter(
        OrderItem.vendor_id == current_user.id
    ).limit(5).all()

    order_data = []

    for item in recent_orders:

        order_data.append({
            "order_id": item.order_id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "subtotal": item.subtotal
        })

    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "revenue": revenue or 0,
        "recent_orders": order_data
    }