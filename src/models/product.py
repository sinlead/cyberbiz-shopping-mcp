"""Product data models."""
from pydantic import BaseModel


class ProductDescription(BaseModel):
    """Product description entity."""
    type: str | None = None
    body_html: str | None = None


class ProductOption(BaseModel):
    """Product option/specification entity."""
    name: str
    types: list[str]


class ProductVariantPhoto(BaseModel):
    """Product variant photo entity with multiple sizes."""
    thumb: str | None = None
    large: str | None = None
    original: str | None = None


class ProductVariant(BaseModel):
    id: int
    title: str
    name: str | None = None
    options: list[str] | None = None
    price: float
    compare_at_price: float | None = None
    max_usable_bonus: int | None = None
    inventory_availability: str | None = None
    weight: float | None = None
    quantity: int | None = None
    featured_image: dict | None = None
    photo_urls: list[ProductVariantPhoto] | None = None


class Product(BaseModel):
    id: int
    title: str
    handle: str | None = None
    price: float | None = None
    photo_urls: list[str] | None = None
    brief: str | None = None
    slogan: str | None = None
    vendor: str | None = None
    channel: str | None = None
    temperature_types: list[str] | None = None
    product_type: str | None = None
    store_type: str | None = None
    genre: str | None = None
    descriptions: list[ProductDescription] | None = None
    options: list[ProductOption] | None = None
    variants: list[ProductVariant]
