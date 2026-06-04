from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.config.database import (
    engine,
    Base
)

from app.exceptions.handlers import (
    global_exception_handler
)

from app.models.user_model import User
from app.models.category_model import Category
from app.models.product_model import Product
from app.models.cart_model import Cart
from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.models.wishlist_model import Wishlist
from app.models.address_model import Address

from app.routes.auth_route import (
    router as auth_router
)

from app.routes.category_route import (
    router as category_router
)

from app.routes.product_route import (
    router as product_router
)

from app.routes.cart_route import (
    router as cart_router
)

from app.routes.order_route import (
    router as order_router
)

from app.routes.wishlist_route import (
    router as wishlist_router
)

from app.routes.address_route import (
    router as address_router
)

from app.routes.dashboard_route import (
    router as dashboard_router
)

# CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI()

# EXCEPTION HANDLER
app.add_exception_handler(
    Exception,
    global_exception_handler
)

# STATIC FILES
app.mount(
    "/uploads",
    StaticFiles(directory="app/uploads"),
    name="uploads"
)

# ROUTES
app.include_router(auth_router)

app.include_router(category_router)

app.include_router(product_router)

app.include_router(cart_router)

app.include_router(order_router)

app.include_router(wishlist_router)

app.include_router(address_router)

app.include_router(dashboard_router)


@app.get("/")
def home():

    return {
        "message": "Enterprise Ecommerce API Running"
    }