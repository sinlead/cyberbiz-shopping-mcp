"""Tool for checking order status."""

from fastmcp.server.dependencies import get_access_token

from config import config


def check_order(
    order_id: str,
) -> dict:
    """
    Check the status of an existing order.

    Args:
        order_id: The order ID to check

    Returns:
        Dictionary containing order status and details
    """
    token = get_access_token()

    if not token:
        return {
            "status": "error",
            "message": "Authentication required",
            "error_code": "AUTHENTICATION_REQUIRED"
        }

    # 驗證用戶是否有 read_orders scope
    required_scope = config.REQUIRED_SCOPES_CHECK_ORDER
    if required_scope not in token.scopes:
        return {
            "status": "error",
            "message": f"Insufficient permissions. Required scope: {required_scope}",
            "error_code": "INSUFFICIENT_SCOPE"
        }

    # 從 token claims 取得用戶資訊
    shop_id = token.claims.get("shop_id")
    shop_domain = token.claims.get("shop_domain")

    # TODO: 實際呼叫 cyberbiz.co API 查詢訂單
    # 使用 shop_id 來確保用戶只能查詢自己的訂單

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
        },
        # 包含驗證後的商店資訊
        "shop_info": {
            "shop_id": shop_id,
            "shop_domain": shop_domain
        }
    }
