from pydantic import BaseModel


class AddCart(BaseModel):

    product_id: int

    quantity: int