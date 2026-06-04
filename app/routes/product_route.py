from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from fastapi import UploadFile, File
from app.utils.file_upload import upload_product_image

from app.config.database import SessionLocal

from app.schemas.product_schema import (
    ProductCreate
)

from app.controllers import (
    product_controller
)

from app.utils.auth_middleware import (
    get_current_user
)

router = APIRouter()


# DATABASE
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ADD PRODUCT
@router.post("/products")
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return product_controller.add_product(
        db,
        product,
        current_user
    )


# ALL PRODUCTS
@router.get("/products")
def get_products(
    search: str = "",
    category_id: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    return product_controller.get_products(
        db,
        search,
        category_id,
        page,
        limit
    )


# SINGLE PRODUCT
@router.get("/products/{product_id}")
def get_single_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    return product_controller.get_single_product(
        db,
        product_id
    )


# UPDATE PRODUCT
@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return product_controller.update_product(
        db,
        product_id,
        product,
        current_user
    )


# DELETE PRODUCT
@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return product_controller.delete_product(
        db,
        product_id,
        current_user
    )



# PRODUCT IMAGE UPLOAD
@router.post("/upload-product-image")
def upload_image(
    file: UploadFile = File(...)
):

    file_name = upload_product_image(file)

    return {
        "message": "Image uploaded",
        "file_name": file_name,
        "image_url": f"/uploads/products/{file_name}"
    }