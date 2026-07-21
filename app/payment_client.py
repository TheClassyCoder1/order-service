"""HTTP client to payment-service (Java).

order-service calls payment-service over REST to charge an order.
This is the Python -> Java HTTP edge.
"""
import os
import requests

PAYMENT_BASE_URL = os.environ.get("PAYMENT_BASE_URL", "http://localhost:8080")


def charge_order(order_id: str, amount_cents: int, currency: str, customer_id: int) -> dict:
    """POST /charge on payment-service.

    The JSON keys here MUST match payment-service's ChargeRequest fields
    (orderId, amountCents, currency, customerId). Rename one side -> silent break.
    """
    resp = requests.post(
        f"{PAYMENT_BASE_URL}/charge",
        json={
            "orderId": order_id,
            "amountCents": amount_cents,
            "currency": currency,
            "customerId": customer_id,
        },
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()  # {chargeId, status}
