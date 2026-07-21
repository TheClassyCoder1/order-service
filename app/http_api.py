"""HTTP read API for the web-frontend (React).

Exposes GET /orders/{id} returning the order JSON, and
POST /orders/{id}/pay which charges via payment-service.

This is the Python -> React (HTTP) contract. The JSON field names
(order_id, amount_cents, currency, status, created_at_ms, customer_id)
are consumed by the frontend.
"""
from fastapi import FastAPI, HTTPException

from store import get_order, mark_paid
from payment_client import charge_order

app = FastAPI(title="order-service")


@app.get("/orders/{order_id}")
def read_order(order_id: str):
    o = get_order(order_id)
    if o is None:
        raise HTTPException(status_code=404, detail="order not found")
    # Response contract consumed by web-frontend:
    return {
        "order_id": o["order_id"],
        "amount_cents": o["amount_cents"],
        "currency": o["currency"],
        "status": o["status"],
        "created_at_ms": o["created_at_ms"],
        "customer_id": o["customer_id"],
    }


@app.post("/orders/{order_id}/pay")
def pay_order(order_id: str):
    o = get_order(order_id)
    if o is None:
        raise HTTPException(status_code=404, detail="order not found")
    result = charge_order(
        o["order_id"], o["amount_cents"], o["currency"], o["customer_id"]
    )
    mark_paid(order_id)
    return {"order_id": order_id, "charge": result}
