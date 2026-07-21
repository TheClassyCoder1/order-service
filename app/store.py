"""In-memory order store. ponytail: a dict is the whole DB for a demo."""

ORDERS = {
    "ord_1001": {
        "order_id": "ord_1001",
        "amount_cents": 4999,
        "currency": "USD",
        "status": "CREATED",
        "created_at_ms": 1721563200000,   # epoch millis
        "customer_id": 7203344561288675329,  # snowflake id, > 2^53
    },
    "ord_1002": {
        "order_id": "ord_1002",
        "amount_cents": 12000,
        "currency": "EUR",
        "status": "PAID",
        "created_at_ms": 1721476800000,
        "customer_id": 7203344561288675330,  # snowflake id, > 2^53
    },
}


def get_order(order_id: str):
    return ORDERS.get(order_id)


def mark_paid(order_id: str):
    o = ORDERS.get(order_id)
    if o:
        o["status"] = "PAID"
    return o
