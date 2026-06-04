from sqlalchemy.orm import Session

from app.models.product_model import Product


# ADD PRODUCT
def add_product(
    db: Session,
    product,
    current_user
):

    if current_user.role != "vendor":

        return {
            "error": "Only vendor can add products"
        }

    new_product = Product(
        vendor_id=current_user.id,
        category_id=product.category_id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image=product.image
    )

    db.add(new_product)

    db.commit()

    db.refresh(new_product)

    return {
        "message": "Product added successfully",
        "product": new_product
    }


# GET PRODUCTS
def get_products(
    db: Session,
    search: str = "",
    category_id: int = None,
    page: int = 1,
    limit: int = 10
):

    query = db.query(Product)

    # SEARCH
    if search:

        query = query.filter(
            Product.name.like(f"%{search}%")
        )

    # CATEGORY FILTER
    if category_id:

        query = query.filter(
            Product.category_id == category_id
        )

    # PAGINATION
    skip = (page - 1) * limit

    products = query.offset(skip).limit(limit).all()

    data = []

    for product in products:

        data.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "image": product.image,
            "category": product.category.name,
            "vendor_id": product.vendor_id
        })

    return data


# SINGLE PRODUCT
def get_single_product(
    db: Session,
    product_id: int
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:

        return {
            "error": "Product not found"
        }

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "image": product.image,
        "category": product.category.name
    }


# UPDATE PRODUCT
def update_product(
    db: Session,
    product_id: int,
    product,
    current_user
):

    existing_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not existing_product:

        return {
            "error": "Product not found"
        }

    if existing_product.vendor_id != current_user.id:

        return {
            "error": "Unauthorized"
        }

    existing_product.category_id = product.category_id
    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.stock = product.stock
    existing_product.image = product.image

    db.commit()

    db.refresh(existing_product)

    return {
        "message": "Product updated"
    }


# DELETE PRODUCT
def delete_product(
    db: Session,
    product_id: int,
    current_user
):

    existing_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not existing_product:

        return {
            "error": "Product not found"
        }

    if existing_product.vendor_id != current_user.id:

        return {
            "error": "Unauthorized"
        }

    db.delete(existing_product)

    db.commit()

    return {
        "message": "Product deleted"
    }