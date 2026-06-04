from sqlalchemy.orm import Session

from app.models.category_model import Category


# CREATE CATEGORY
def create_category(
    db: Session,
    category
):

    existing = db.query(Category).filter(
        Category.name == category.name
    ).first()

    if existing:
        return {
            "error": "Category already exists"
        }

    new_category = Category(
        name=category.name
    )

    db.add(new_category)

    db.commit()

    db.refresh(new_category)

    return {
        "message": "Category created successfully"
    }


# GET ALL CATEGORIES
def get_categories(db: Session):

    return db.query(Category).all()