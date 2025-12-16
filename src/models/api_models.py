from pydantic import BaseModel

from .address import Address


class CreateAddressRequest(BaseModel):
    address: Address
