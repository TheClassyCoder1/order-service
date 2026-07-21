"""HTTP read API for the web-frontend (React).

Exposes GET /api/v2/orders/{id} returning the order JSON, and
POST /api/v2/orders/{id}/pay which charges via payment-service.

This is the Python -> React (HTTP) contract. The JSON field names
(id, amount, currency, status) are consumed by the frontend.
"""
from fastapi import FastAPI, HTTPException

from store import get_order, mark_paid
from payment_client import charge_order

app = FastAPI(title="order-service")


@app.get("/api/v2/orders/{order_id}")
def read_order(order_id: str):
    o = get_order(order_id)
    if o is None:
        raise HTTPException(status_code=404, detail="order not found")
    # Response contract consumed by web-frontend:
    return {
        "id": o["order_id"],
        "amount": o["amount_cents"] / 100.0,   # dollars
        "currency": o["currency"],
        "status": o["status"],
    }


@app.post("/api/v2/orders/{order_id}/pay")
def pay_order(order_id: str):
    o = get_order(order_id)
    if o is None:
        raise HTTPException(status_code=404, detail="order not found")
    result = charge_order(o["order_id"], o["amount_cents"] / 100.0, o["currency"])
    mark_paid(order_id)
    return {"id": order_id, "charge": result}
