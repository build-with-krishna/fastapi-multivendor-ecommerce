from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.config.database import Base


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(255),
        unique=True
    )