"""Tool for handling after-sales service."""

def handle_after_sales(
    order_id: str,
    issue_type: str,
    description: str
) -> dict:
    """
    Handle after-sales service requests.

    Args:
        order_id: The order ID related to the issue
        issue_type: Type of issue (e.g., "refund", "exchange", "repair", "complaint")
        description: Detailed description of the issue

    Returns:
        Dictionary containing support ticket information
    """
    # Mock after-sales handling
    import random
    ticket_id = f"TICKET-{random.randint(10000, 99999)}"

    return {
        "status": "success",
        "ticket_id": ticket_id,
        "order_id": order_id,
        "issue_type": issue_type,
        "description": description,
        "ticket_status": "open",
        "priority": "medium",
        "created_at": "2025-11-05T10:30:00Z",
        "assigned_to": "Support Team",
        "estimated_resolution": "2-3 business days",
        "next_steps": [
            "Our support team will review your request",
            "You will receive an email update within 24 hours",
            "Please keep your order ID handy for reference"
        ],
        "message": f"After-sales ticket {ticket_id} created successfully. Our team will contact you shortly."
    }
