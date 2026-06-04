from pydantic import BaseModel


class AddressCreate(BaseModel):

    full_name: str

    mobile: str

    address_line: str

    city: str

    state: str

    pincode: str

    country: str