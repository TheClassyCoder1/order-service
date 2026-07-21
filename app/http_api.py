"""HTTP read API for the web-frontend (React).

Exposes GET /api/orders/{ref} returning the order JSON, and
POST /api/orders/{ref}/pay which charges via payment-service.

This is the Python -> React (HTTP) contract. The JSON field names
(order_ref, amount_cents, currency_code, status, created_at_ms, customer_id)
are consumed by the frontend.
"""
from fastapi import FastAPI, HTTPException

from store import get_order, mark_paid
from payment_client import charge_order

app = FastAPI(title="order-service")


@app.get("/api/orders/{order_ref}")
def read_order(order_ref: str):
    o = get_order(order_ref)
    if o is None:
        raise HTTPException(status_code=404, detail="order not found")
    # Response contract consumed by web-frontend:
    return {
        "order_ref": o["order_id"],
        "amount_cents": o["amount_cents"],
        "currency_code": o["currency"],
        "status": o["status"],
        "created_at_ms": o["created_at_ms"] // 1000,   # epoch seconds
        "customer_id": o["customer_id"],
    }


@app.post("/api/orders/{order_ref}/pay")
def pay_order(order_ref: str):
    o = get_order(order_ref)
    if o is None:
        raise HTTPException(status_code=404, detail="order not found")
    result = charge_order(
        o["order_id"], o["amount_cents"], o["currency"], o["customer_id"]
    )
    mark_paid(order_ref)
    return {"order_ref": order_ref, "charge": result}
