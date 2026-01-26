"""Tool for discovering and searching products."""

from typing import Literal

from pydantic import BaseModel

from dependencies import get_bigquery_client, get_cyberbiz_client, get_embedding_client
from mcp_instance import mcp
from models.product import Product
from repositories.product_repository import ProductRepository


class DiscoverProductsResponse(BaseModel):
    status: Literal["success", "error"]
    products: list[Product]


@mcp.tool(
    description="""Search for products using keyword or vector similarity search.

Search modes:
- 'keyword': Use for exact product names, brands, or specific terms
  Examples: "Nike shoes", "iPhone 15", "Adidas running shoes"

- 'vector': Use for scenario-based, feature-based, or conceptual queries
  Examples:
  * "gifts for my girlfriend who loves minimalist style"
  * "something comfortable for hiking in summer"
  * "products suitable for a beach vacation"
  * "eco-friendly items for home office"
  * "gifts for tech enthusiasts under $100"

Choose 'vector' mode when the user describes a scenario, need, or abstract concept rather than naming a specific product."""
)
async def discover_products(
    search_mode: Literal["keyword", "vector"],
    query: str,
    price_range: tuple[float, float] | None = None,
    channels: list[str] | None = None,
    max_results: int = 5,
) -> DiscoverProductsResponse:
    repository = ProductRepository(
        cyberbiz_client=get_cyberbiz_client(),
        bigquery_client=get_bigquery_client(),
        embedding_client=get_embedding_client(),
    )

    if search_mode == "keyword":
        products = await repository.search_by_keyword_matching(
            query=query,
            # price_range=None,
            # channels=None,
            limit=max_results,
        )
        return DiscoverProductsResponse(
            status="success",
            products=products
        )
    elif search_mode == "vector":
        products = await repository.search_by_vector_similarity(
            query=query,
            # price_range=None,
            # channels=None,
            limit=max_results,
        )
        return DiscoverProductsResponse(
            status="success",
            products=products
        )
