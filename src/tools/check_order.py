"""Tool for checking order status."""

def check_order(order_id: str) -> dict:
    """
    Check the status of an existing order.

    Args:
        order_id: The order ID to check

    Returns:
        Dictionary containing order status and details
    """
    # Mock order status
    return {
        "status": "success",
        "order_id": order_id,
        "order_status": "shipped",
        "order_date": "2025-11-01",
        "items": [
            {
                "product_id": "PROD-001",
                "product_name": "Premium Laptop - Model A",
                "quantity": 1,
                "unit_price": 299.99,
                "subtotal": 299.99
            }
        ],
        "total_price": 299.99,
        "currency": "USD",
        "shipping": {
            "status": "in_transit",
            "tracking_number": "TRK-123456",
            "estimated_delivery": "2025-11-10",
            "carrier": "Standard Shipping"
        },
        "payment": {
            "method": "credit_card",
            "status": "paid",
            "last_four_digits": "1234"
        },
        "customer": {
            "name": "John Doe",
            "email": "john@example.com"
        }
    }
