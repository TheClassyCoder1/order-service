# order-service (Python)

Owns the **Order** domain and the source-of-truth gRPC contract (`proto/order.proto`).

## Interfaces
- **gRPC server** — `OrderService.FetchOrder` (`app/grpc_server.py`, port 50051).
  Consumed by **payment-service** (Java), which vendors a copy of `order.proto`.
- **HTTP read API** — `GET /api/v2/orders/{id}`, `POST /api/v2/orders/{id}/pay` (`app/http_api.py`, port 8000).
  Consumed by **web-frontend** (React).
- **HTTP client** — calls **payment-service** `POST /charge` (`app/payment_client.py`).

## Cross-repo contract
`proto/order.proto` fields (`id`, `amount`, `currency`, `status`) and the
`GET /api/v2/orders/{id}` JSON shape are consumed by the other two repos. Renaming a field here
requires matching changes in payment-service (vendored proto + gRPC client) and web-frontend.

## Run
```bash
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./gen_proto.sh                                   # regenerate stubs
PYTHONPATH=app ./.venv/bin/python app/grpc_server.py     # gRPC :50051
PYTHONPATH=app ./.venv/bin/uvicorn http_api:app --port 8000   # HTTP :8000
```
