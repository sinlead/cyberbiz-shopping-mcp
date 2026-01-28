"""Middleware to extract shop information from headers."""

import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from context import set_shop_id, set_shop_domain

logger = logging.getLogger(__name__)


class ShopContextMiddleware(BaseHTTPMiddleware):
    """Middleware to extract shop_id and shop_domain from headers and set in context."""

    async def dispatch(self, request: Request, call_next):
        """Extract shop_id and shop_domain from headers and set in context."""

        # Extract from headers
        shop_id_str = request.headers.get("X-Shop-ID")
        shop_domain = request.headers.get("X-Shop-Domain")

        if not shop_id_str:
            logger.error("Missing X-Shop-ID header")
            raise ValueError("X-Shop-ID header is required")

        if not shop_domain:
            logger.error("Missing X-Shop-Domain header")
            raise ValueError("X-Shop-Domain header is required")

        try:
            shop_id = int(shop_id_str)
        except ValueError:
            logger.error(f"Invalid X-Shop-ID header: {shop_id_str}")
            raise ValueError(f"Invalid X-Shop-ID: {shop_id_str}")

        # Set in context
        set_shop_id(shop_id)
        set_shop_domain(shop_domain)

        logger.info(f"Request context set: shop_id={shop_id}, shop_domain={shop_domain}")

        # Continue processing
        response = await call_next(request)
        return response
