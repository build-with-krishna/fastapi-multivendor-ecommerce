from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.schemas.category_schema import (
    CategoryCreate
)

from app.controllers import (
    category_controller
)

router = APIRouter()


# DATABASE
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# CREATE CATEGORY
@router.post("/categories")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    return category_controller.create_category(
        db,
        category
    )


# GET CATEGORIES
@router.get("/categories")
def get_categories(
    db: Session = Depends(get_db)
):

    return category_controller.get_categories(
        db
    )