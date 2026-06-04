from pydantic import BaseModel


class ProductCreate(BaseModel):

    category_id: int

    name: str

    description: str

    price: int

    stock: int

    image: str