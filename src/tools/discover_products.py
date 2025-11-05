"""Tool for discovering and searching products."""

def discover_products(
    query: str,
    category: str | None = None,
    max_results: int = 10
) -> dict:
    """
    Search and discover products on CYBERBIZ platform.

    Args:
        query: Search query string
        category: Optional category filter (e.g., "electronics", "clothing")
        max_results: Maximum number of results to return (default: 10)

    Returns:
        Dictionary containing search results with product details
    """
    # Mock product data
    mock_products = [
        {
            "id": "PROD-001",
            "name": f"Premium {query.title()} - Model A",
            "price": 299.99,
            "currency": "USD",
            "description": f"High-quality {query} with advanced features",
            "category": category or "general",
            "stock": 50,
            "rating": 4.5,
            "image_url": "https://example.com/product-001.jpg"
        },
        {
            "id": "PROD-002",
            "name": f"Professional {query.title()} - Pro Edition",
            "price": 499.99,
            "currency": "USD",
            "description": f"Professional-grade {query} for experts",
            "category": category or "general",
            "stock": 25,
            "rating": 4.8,
            "image_url": "https://example.com/product-002.jpg"
        },
        {
            "id": "PROD-003",
            "name": f"Budget {query.title()} - Basic",
            "price": 149.99,
            "currency": "USD",
            "description": f"Affordable {query} for everyday use",
            "category": category or "general",
            "stock": 100,
            "rating": 4.0,
            "image_url": "https://example.com/product-003.jpg"
        }
    ]

    # Limit results
    results = mock_products[:max_results]

    return {
        "status": "success",
        "query": query,
        "category": category,
        "total_results": len(results),
        "products": results
    }
