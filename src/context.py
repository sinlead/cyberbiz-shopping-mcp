"""Request context management for shop information."""

from contextvars import ContextVar
from typing import Optional

# Context variables for shop information
_shop_id: ContextVar[Optional[int]] = ContextVar("shop_id", default=None)
_shop_domain: ContextVar[Optional[str]] = ContextVar("shop_domain", default=None)

def get_shop_id() -> int:
    """Get shop_id from request context."""
    shop_id = _shop_id.get()
    if shop_id is None:
        raise ValueError("shop_id not found in request context")
    return shop_id

def get_shop_domain() -> str:
    """Get shop_domain from request context."""
    shop_domain = _shop_domain.get()
    if shop_domain is None:
        raise ValueError("shop_domain not found in request context")
    return shop_domain
