"""HTTP client to payment-service (Java).

order-service calls payment-service over REST to charge an order.
This is the Python -> Java HTTP edge.
"""
import os
import requests

PAYMENT_BASE_URL = os.environ.get("PAYMENT_BASE_URL", "http://localhost:8080")


def charge_order(order_id: str, amount: float, currency: str) -> dict:
    """POST /charge on payment-service.

    The JSON keys here MUST match payment-service's ChargeRequest fields.
    Rename one side -> silent break.
    """
    resp = requests.post(
        f"{PAYMENT_BASE_URL}/charge",
        json={
            "id": order_id,
            "amount": amount,
            "currency": currency,
        },
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()  # {chargeId, status}
