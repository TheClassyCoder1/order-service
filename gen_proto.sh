#!/usr/bin/env bash
# Regenerate gRPC stubs from proto/order.proto after any contract change.
set -euo pipefail
cd "$(dirname "$0")"
python -m grpc_tools.protoc -I proto --python_out=app --grpc_python_out=app proto/order.proto
echo "regenerated app/order_pb2.py + app/order_pb2_grpc.py"
