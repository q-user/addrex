from pydantic import BaseModel

from .address import Address
from .phone import Phone


class PhoneAddress(BaseModel):
    phone: Phone
    address: Address
