from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.config.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    total_amount = Column(Integer)

    status = Column(
        String(50),
        default="pending"
    )

    user = relationship("User")