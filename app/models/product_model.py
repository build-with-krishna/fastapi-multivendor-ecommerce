from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.config.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    name = Column(String(255))

    description = Column(Text)

    price = Column(Integer)

    stock = Column(Integer)

    image = Column(String(255))

    vendor = relationship("User")

    category = relationship("Category")