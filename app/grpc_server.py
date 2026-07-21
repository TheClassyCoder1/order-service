"""gRPC server exposing OrderService.FetchOrder.

payment-service (Java) is the gRPC client of this server.
Stubs (order_pb2, order_pb2_grpc) are generated from proto/order.proto.
"""
from concurrent import futures

import grpc

import order_pb2
import order_pb2_grpc
from store import get_order


class OrderServicer(order_pb2_grpc.OrderServiceServicer):
    def FetchOrder(self, request, context):
        o = get_order(request.id)
        if o is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"order {request.id} not found")
        return order_pb2.GetOrderResponse(
            id=o["order_id"],
            amount=o["amount_cents"] / 100.0,               # dollars, not cents
            status=order_pb2.OrderStatus.Value(o["status"]),  # enum
            currency=o["currency"],
        )


def serve(port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC OrderService listening on :{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
