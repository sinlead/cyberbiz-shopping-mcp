import asyncio
import logging
from pprint import pformat

from config import config
from models.product import Product, ProductVariant
from services.cyberbiz_bigquery_client import CyberbizBigQueryClient
from services.cyberbiz_client import CyberbizClient
from services.embedding_client import EmbeddingClient

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(
        self,
        cyberbiz_client: CyberbizClient,
        bigquery_client: CyberbizBigQueryClient,
        embedding_client: EmbeddingClient
    ):
        self.cyberbiz_client = cyberbiz_client
        self.bigquery_client = bigquery_client
        self.embedding_client = embedding_client

    async def search_by_keyword_matching(self, query: str, limit: int) -> list[Product]:
        res = await self.cyberbiz_client.make_request(
            "GET",
            "/v2/products/search",
            params={"q": query, "limit": limit}
        )

        products = []
        for item in res:
            product = Product(
                id=item["id"],
                title=item["title"],
                published=item["published"],
                currency="TWD",  # Default to TWD, adjust if API provides this
                url=item["product_url"],
                photo_urls=item.get("photo_urls"),
                description="\n\n".join(filter(None, [item.get("brief"), item.get("body_html")])),
                variants=[
                    ProductVariant(
                        id=variant["id"],
                        title=variant["name"],
                        price=variant["price"],
                        quantity=variant.get("inventory_quantity"),
                    )
                    for variant in item.get("product_variants", [])
                ]
            )
            products.append(product)

        return products

    async def search_by_vector_similarity(self, query: str, limit: int) -> list[Product]:
        embedding = await self.embedding_client.generate_embedding(query)
        product_embedding_table = f"{config.CYBERBIZ_GCP_PROJECT_ID}.cyberbiz_embedding_gemini.product_embeddings"
        similarity_threshold = 0.2

        sql = f"""
            SELECT
                base.id as product_id,
                base.shop_id,
                base.content,
                distance,
                (1 - distance) as similarity_score
            FROM
                VECTOR_SEARCH(
                (
                    SELECT id, shop_id, content, ml_generate_embedding_result
                    FROM `{product_embedding_table}`
                    WHERE shop_id = @shop_id
                ),
                'ml_generate_embedding_result',
                (SELECT @embedding AS query_vector),
                top_k => @limit,
                distance_type => 'COSINE'
                )
            WHERE (1 - distance) >= @threshold
            ORDER BY similarity_score DESC
        """

        res = await self.bigquery_client.query(sql, {
            "embedding": embedding,
            "limit": limit,
            "threshold": similarity_threshold
        })

        # Extract product IDs and fetch details in parallel
        product_ids = [result["product_id"] for result in res]
        products = await asyncio.gather(*[self.get_product_detail(product_id) for product_id in product_ids])
        return products


    async def get_product_detail(self, product_id: int) -> Product:
        res = await self.cyberbiz_client.make_request(
            "GET",
            f"/v2/products/{product_id}",
        )

        return Product(
            id=product_id,
            title=res["title"],
            published=res["published"],
            currency="TWD",
            url=res["product_url"],
            photo_urls=res.get("photo_urls"),
            description="\n\n".join(filter(None, [res.get("brief"), res.get("body_html")])),
            variants=[
                ProductVariant(
                    id=variant["id"],
                    title=variant["name"],
                    price=variant["price"],
                    quantity=variant.get("inventory_quantity"),
                )
                for variant in res.get("product_variants", [])
            ]
        )
