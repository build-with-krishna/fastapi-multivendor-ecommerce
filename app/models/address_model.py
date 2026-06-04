from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.config.database import Base


class Address(Base):

    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    full_name = Column(String(255))

    mobile = Column(String(20))

    address_line = Column(String(500))

    city = Column(String(100))

    state = Column(String(100))

    pincode = Column(String(20))

    country = Column(String(100))