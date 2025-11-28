"""Product data models."""
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    title: str
    published: bool
    currency: str
    url: str
    photo_urls: list[str] | None
    description: str
    variants: list[ProductVariant]

class ProductVariant(BaseModel):
    id: int
    title: str
    price: float
    quantity: int | None
