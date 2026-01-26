"""Tool for modifying existing orders."""

from mcp_instance import mcp


@mcp.tool()
def modify_order(
    order_id: str,
    modifications: dict
) -> dict:
    """
    Modify an existing order.

    Args:
        order_id: The order ID to modify
        modifications: Dictionary containing modifications
            (e.g., quantity, shipping_address, delivery_date)

    Returns:
        Dictionary containing modification confirmation
    """
    # Mock order modification
    return {
        "status": "success",
        "order_id": order_id,
        "modification_status": "updated",
        "modifications_applied": modifications,
        "message": "Order modified successfully",
        "updated_order": {
            "order_id": order_id,
            "order_status": "updated",
            "total_price": 349.99,
            "currency": "USD",
            "estimated_delivery": modifications.get("delivery_date", "2025-11-12")
        },
        "note": "Some modifications may affect delivery time or total cost"
    }
