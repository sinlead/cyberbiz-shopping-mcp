"""Tool for canceling orders."""

from mcp_instance import mcp


@mcp.tool()
def cancel_order(
    order_id: str,
    reason: str
) -> dict:
    """
    Cancel an existing order.

    Args:
        order_id: The order ID to cancel
        reason: Reason for cancellation

    Returns:
        Dictionary containing cancellation confirmation
    """
    # Mock order cancellation
    return {
        "status": "success",
        "order_id": order_id,
        "cancellation_status": "cancelled",
        "reason": reason,
        "refund": {
            "amount": 299.99,
            "currency": "USD",
            "method": "original_payment_method",
            "estimated_processing_time": "3-5 business days"
        },
        "cancelled_at": "2025-11-05T10:30:00Z",
        "message": "Order cancelled successfully. Refund will be processed within 3-5 business days."
    }
