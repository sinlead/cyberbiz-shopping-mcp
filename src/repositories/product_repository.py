import asyncio
import logging
from typing import Any
from pprint import pformat

import httpx

from config import config
from context import get_shop_domain
from models.product import (
    Product,
    ProductVariant,
    ProductDescription,
    ProductOption,
    ProductVariantPhoto,
    StoreType,
    Genre,
)
from services.cyberbiz_bigquery_client import CyberbizBigQueryClient
from services.embedding_client import EmbeddingClient

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(
        self,
        bigquery_client: CyberbizBigQueryClient,
        embedding_client: EmbeddingClient
    ):
        self.bigquery_client = bigquery_client
        self.embedding_client = embedding_client
        self.timeout = 30

    async def search_by_vector_similarity(
        self,
        query: str,
        limit: int,
        min_price: float | None = None,
        max_price: float | None = None,
        store_type: str | None = None,
        genre: str | None = None,
    ) -> list[Product]:
        embedding = await self.embedding_client.generate_embedding(query)
        product_embedding_table = f"{config.CYBERBIZ_GCP_PROJECT_ID}.cyberbiz_embedding_gemini.product_embeddings"
        similarity_threshold = 0.2

        # Build filter conditions and query params
        filter_conditions = []
        query_params = {
            "embedding": embedding,
            "limit": limit,
            "threshold": similarity_threshold
        }

        if min_price is not None:
            filter_conditions.append("base.price >= @min_price")
            query_params["min_price"] = min_price

        if max_price is not None:
            filter_conditions.append("base.price <= @max_price")
            query_params["max_price"] = max_price

        if store_type is not None:
            filter_conditions.append("base.store_type = @store_type")
            query_params["store_type"] = StoreType[store_type.upper()].value

        if genre is not None:
            filter_conditions.append("base.genre = @genre")
            query_params["genre"] = Genre[genre.upper()].value

        where_filter = ""
        if filter_conditions:
            where_filter = "AND " + " AND ".join(filter_conditions)

        sql = f"""
            SELECT
                base.id as product_id,
                base.shop_id,
                base.content,
                base.price,
                distance,
                (1 - distance) as similarity_score
            FROM
                VECTOR_SEARCH(
                (
                    SELECT id, shop_id, content, price, store_type, genre, ml_generate_embedding_result
                    FROM `{product_embedding_table}`
                    WHERE shop_id = @shop_id
                ),
                'ml_generate_embedding_result',
                (SELECT @embedding AS query_vector),
                top_k => @limit,
                distance_type => 'COSINE'
                )
            WHERE (1 - distance) >= @threshold
            {where_filter}
            ORDER BY similarity_score DESC
        """

        res = await self.bigquery_client.query(sql, query_params)

        logger.info(f"Vector search returned {len(res)} results")
        if res:
            logger.info(f"Top result similarity scores: {[f'{r.get('similarity_score', 0):.4f}' for r in res[:3]]}")
        else:
            logger.warning(f"No results found for query: '{query}' with threshold {similarity_threshold}")

        # Extract product IDs and fetch details in parallel
        product_ids = [result["product_id"] for result in res]
        products = await asyncio.gather(*[self.get_product_detail(product_id) for product_id in product_ids])

        logger.info(f"Successfully fetched {len(products)} product details")
        return products


    async def get_product_detail(self, product_id: int) -> Product:
        shop_domain = get_shop_domain()
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"https://{shop_domain}/api/storefront/v1/products/{product_id}"
            response = await client.get(url)
            response.raise_for_status()
            res = response.json()

        variants = []
        if res.get("variants"):
            for variant in res["variants"]:
                photo_urls = []
                if variant.get("photo_urls"):
                    for photo in variant["photo_urls"]:
                        photo_urls.append(
                            ProductVariantPhoto(
                                thumb=photo.get("thumb"),
                                large=photo.get("large"),
                                original=photo.get("original"),
                            )
                        )

                variants.append(
                    ProductVariant(
                        id=variant["id"],
                        title=variant.get("title", ""),
                        name=variant.get("name"),
                        options=variant.get("options"),
                        price=variant.get("price", 0),
                        compare_at_price=variant.get("compare_at_price"),
                        max_usable_bonus=variant.get("max_usable_bonus"),
                        inventory_availability=variant.get("inventory_availability"),
                        weight=variant.get("weight"),
                        featured_image=variant.get("featured_image"),
                        photo_urls=photo_urls if photo_urls else None,
                    )
                )

        descriptions = []
        if res.get("descriptions"):
            for desc in res["descriptions"]:
                descriptions.append(
                    ProductDescription(
                        type=desc.get("type"),
                        body_html=desc.get("body_html"),
                    )
                )

        options = []
        if res.get("options"):
            for opt in res["options"]:
                options.append(
                    ProductOption(
                        name=opt.get("name", ""),
                        types=opt.get("types", []),
                    )
                )

        return Product(
            id=product_id,
            title=res["title"],
            handle=res.get("handle"),
            price=res.get("price"),
            photo_urls=res.get("photo_urls"),
            brief=res.get("brief"),
            slogan=res.get("slogan"),
            vendor=res.get("vendor"),
            channel=res.get("channel"),
            temperature_types=res.get("temperature_types"),
            product_type=res.get("product_type"),
            store_type=res.get("store_type"),
            genre=res.get("genre"),
            descriptions=descriptions if descriptions else None,
            options=options if options else None,
            variants=variants,
        )

    async def list_products(
        self,
        query: str | None = None,
        page: int = 1,
        per_page: int = 10,
        store_type: str | None = None,
        genre: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str | None = None,
    ) -> list[Product]:
        """List published products with filtering and sorting options.

        Args:
            query: Search keyword (searches product name, description, type, vendor, channel)
            page: Page number (default: 1)
            per_page: Number of results per page (default: 10)
            store_type: Store type filter (shop, pos_shop, branch_store, other_sales_channel)
            genre: Product genre filter (normal, eticket, combo, fake_other_sales_channel_product)
            min_price: Minimum price filter
            max_price: Maximum price filter
            sort_by: Sort method (price-asc, price-desc, sell_from-asc, sell_from-desc, recent_days_sold-asc, recent_days_sold-desc)

        Returns:
            List of Product objects
        """
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }

        if query:
            params["q"] = query
        if store_type:
            params["store_type"] = store_type
        if genre:
            params["genre"] = genre
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        if sort_by:
            params["sort_by"] = sort_by

        shop_domain = get_shop_domain()
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"https://{shop_domain}/api/storefront/v1/products"
            response = await client.get(url, params=params)
            response.raise_for_status()
            res = response.json()

        products = []
        for item in res:
            variants = []
            if item.get("variants"):
                for variant in item["variants"]:
                    photo_urls = []
                    if variant.get("photo_urls"):
                        for photo in variant["photo_urls"]:
                            photo_urls.append(
                                ProductVariantPhoto(
                                    thumb=photo.get("thumb"),
                                    large=photo.get("large"),
                                    original=photo.get("original"),
                                )
                            )

                    variants.append(
                        ProductVariant(
                            id=variant["id"],
                            title=variant.get("title", ""),
                            name=variant.get("name"),
                            options=variant.get("options"),
                            price=variant.get("price", 0),
                            compare_at_price=variant.get("compare_at_price"),
                            max_usable_bonus=variant.get("max_usable_bonus"),
                            inventory_availability=variant.get("inventory_availability"),
                            weight=variant.get("weight"),
                            featured_image=variant.get("featured_image"),
                            photo_urls=photo_urls if photo_urls else None,
                        )
                    )

            descriptions = []
            if item.get("descriptions"):
                for desc in item["descriptions"]:
                    descriptions.append(
                        ProductDescription(
                            type=desc.get("type"),
                            body_html=desc.get("body_html"),
                        )
                    )

            options = []
            if item.get("options"):
                for opt in item["options"]:
                    options.append(
                        ProductOption(
                            name=opt.get("name", ""),
                            types=opt.get("types", []),
                        )
                    )

            product = Product(
                id=item["id"],
                title=item["title"],
                handle=item.get("handle"),
                price=item.get("price"),
                photo_urls=item.get("photo_urls"),
                brief=item.get("brief"),
                slogan=item.get("slogan"),
                vendor=item.get("vendor"),
                channel=item.get("channel"),
                temperature_types=item.get("temperature_types"),
                product_type=item.get("product_type"),
                store_type=item.get("store_type"),
                genre=item.get("genre"),
                descriptions=descriptions if descriptions else None,
                options=options if options else None,
                variants=variants,
            )
            products.append(product)

        return products
