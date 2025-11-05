"""Tool for checking if a purchase is feasible."""

def check_purchase_feasibility(
    product_id: str,
    quantity: int
) -> dict:
    """
    Check if a purchase is feasible for a given product and quantity.

    Args:
        product_id: The product ID to check
        quantity: Desired quantity to purchase

    Returns:
        Dictionary containing feasibility status and details
    """
    # Mock feasibility check
    available_stock = 50
    is_available = quantity <= available_stock

    return {
        "status": "success",
        "product_id": product_id,
        "requested_quantity": quantity,
        "available_stock": available_stock,
        "is_feasible": is_available,
        "can_purchase": is_available,
        "restrictions": {
            "min_order_quantity": 1,
            "max_order_quantity": 100,
            "requires_age_verification": False,
            "ships_to_region": True
        },
        "message": "Purchase is feasible" if is_available else f"Only {available_stock} units available"
    }
