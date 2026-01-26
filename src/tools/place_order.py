"""Tool for placing orders."""

from mcp_instance import mcp


@mcp.tool()
def place_order(
    product_id: str,
    quantity: int,
    customer_info: dict
) -> dict:
    """
    Place an order for a product.

    Args:
        product_id: The product ID to order
        quantity: Quantity to order
        customer_info: Dictionary containing customer information
            (name, email, phone, shipping_address, payment_method)

    Returns:
        Dictionary containing order confirmation details
    """
    # Mock order placement
    import random
    order_id = f"ORD-{random.randint(10000, 99999)}"
    unit_price = 299.99
    total_price = unit_price * quantity

    return {
        "status": "success",
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": total_price,
        "currency": "USD",
        "order_status": "confirmed",
        "customer": {
            "name": customer_info.get("name", "Customer"),
            "email": customer_info.get("email", "customer@example.com")
        },
        "estimated_delivery": "2025-11-10",
        "tracking_number": f"TRK-{random.randint(100000, 999999)}",
        "message": "Order placed successfully"
    }
