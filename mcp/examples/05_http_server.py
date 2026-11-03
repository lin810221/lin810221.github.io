"""Default: inspect the app. --serve starts a loopback-only HTTP service."""
import argparse
from demo_server import build_server

server = build_server()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if args.serve:
        server.run(transport="streamable-http", host="127.0.0.1", port=args.port,
                   stateless_http=True, json_response=True)
    else:
        app = server.streamable_http_app(stateless_http=True, json_response=True)
        print("Routes:", [route.path for route in app.routes])
        print("Start explicitly: python 05_http_server.py --serve")
