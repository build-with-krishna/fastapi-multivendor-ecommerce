from pydantic import BaseModel


class CreateOrder(BaseModel):

    address: str