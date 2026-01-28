"""Tool for discovering and searching products."""

from typing import Literal

from pydantic import BaseModel

from dependencies import get_bigquery_client, get_embedding_client
from mcp_instance import mcp
from models.product import Product
from repositories.product_repository import ProductRepository

class DiscoverProductsResponse(BaseModel):
    status: Literal["success", "error"]
    products: list[Product]

# Description 後續可補[shop: 線上商店 ; pos_shop: POS商店 ; branch_store: 門市]

@mcp.tool(
    description="""Search for products using keyword or vector similarity search.

Search modes:
- 'keyword': Use ONLY for exact product names, brands, or very specific terms
  Examples: "Nike shoes", "iPhone 15", "casual t-shirt"

- 'vector': Use for natural language queries, descriptions, or need-based searches
  Examples:
  * "I want to find men's casual t-shirts" (contains intent phrases)
  * "help me find gifts suitable for my girlfriend" (natural conversational language)
  * "something comfortable for hiking in summer"
  * "products suitable for a beach vacation"
  * "eco-friendly items for home office"

IMPORTANT: Use 'vector' mode when user query contains:
- Intent phrases (e.g., "I want", "help me find", "looking for")
- Full sentences or conversational language
- Scenario descriptions or abstract needs

Use 'keyword' mode ONLY for direct product names without extra words.

Filter options:
- store_type: Filter by store type
  * 'shop': 線上商店 (Online store)

- genre: Filter by product type
  * 'normal': 一般商品 (Regular products)
  * 'eticket': 電子票券 (E-tickets)
  * 'combo': 組合商品 (Combo products)

- sort_by: Sort results by
  * 'price-asc': 價格由低到高 (Price: low to high)
  * 'price-desc': 價格由高到低 (Price: high to low)
  * 'sell_from-asc': 上架時間由舊到新 (Listed: oldest first)
  * 'sell_from-desc': 上架時間由新到舊 (Listed: newest first)
  * 'recent_days_sold-asc': 近期銷售量由低到高 (Recent sales: low to high)
  * 'recent_days_sold-desc': 近期銷售量由高到低 (Recent sales: high to low)"""
)
async def discover_products(
    search_mode: Literal["keyword", "vector"],
    query: str,
    page: int = 1,
    per_page: int = 10,
    min_price: float | None = None,
    max_price: float | None = None,
    store_type: Literal["shop"] = "shop",
    genre: Literal["normal", "eticket", "combo"] | None = None,
    sort_by: Literal["price-asc", "price-desc", "sell_from-asc", "sell_from-desc", "recent_days_sold-asc", "recent_days_sold-desc"] | None = None,
) -> DiscoverProductsResponse:
    repository = ProductRepository(
        bigquery_client=get_bigquery_client(),
        embedding_client=get_embedding_client(),
    )

    if search_mode == "keyword":
        products = await repository.list_products(
            query=query if query else None,
            page=page,
            per_page=per_page,
            store_type=store_type,
            genre=genre,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by or "recent_days_sold-desc",
        )
        return DiscoverProductsResponse(
            status="success",
            products=products
        )
    elif search_mode == "vector":
        products = await repository.search_by_vector_similarity(
            query=query,
            limit=per_page,
            min_price=min_price,
            max_price=max_price,
            store_type=store_type,
            genre=genre,
        )

        return DiscoverProductsResponse(
            status="success",
            products=products
        )
