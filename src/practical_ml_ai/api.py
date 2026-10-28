"""A JSON prediction API for the Module 12 model, using only the standard library.

POST /predict accepts exactly the eleven chemistry features and returns the
checked prediction; GET /health reports the loaded model. Contract violations
return 422 with a reason, malformed JSON returns 400, and unknown paths 404.
This is a local teaching service: it has no authentication, rate limiting or
production availability guarantee. Frameworks such as FastAPI add request
schemas and documentation on top of the same contract.
"""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from .deployment import checked_predict

MAX_BODY_BYTES = 10_000


def create_server(bundle, host="127.0.0.1", port=8000):
    """Return an HTTP server bound to host:port; port 0 chooses a free port."""

    class Handler(BaseHTTPRequestHandler):
        def _send(self, status, body):
            payload = (json.dumps(body) + "\n").encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            if self.path != "/health":
                return self._send(404, {"error": "Unknown path. Use GET /health or POST /predict."})
            self._send(200, {"status": "ok", "model": bundle["selection"]["model"],
                             "threshold": bundle["selection"]["threshold"], "features": bundle["features"]})

        def do_POST(self):
            if self.path != "/predict":
                return self._send(404, {"error": "Unknown path. Use GET /health or POST /predict."})
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_BODY_BYTES:
                return self._send(413, {"error": "Request body is too large."})
            try:
                record = json.loads(self.rfile.read(length) or b"null")
            except (json.JSONDecodeError, UnicodeDecodeError):
                return self._send(400, {"error": "Send one JSON object of feature values."})
            try:
                result = checked_predict(bundle, record)
            except ValueError as error:
                return self._send(422, {"error": str(error)})
            self._send(200, result)

        def log_message(self, format, *args):
            pass  # Keep the terminal quiet; requests are not logged with their contents.

    return ThreadingHTTPServer((host, port), Handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)
    from .classical import classification_bundle
    server = create_server(classification_bundle(), args.host, args.port)
    print(f"Serving on http://{args.host}:{server.server_address[1]} (GET /health, POST /predict). Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
