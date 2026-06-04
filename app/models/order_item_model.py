from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.config.database import Base


class OrderItem(Base):

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    vendor_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    quantity = Column(Integer)

    price = Column(Integer)

    subtotal = Column(Integer)

    product = relationship("Product")