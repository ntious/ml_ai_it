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


def request_length(headers):
    """Return (length, None) for a usable Content-Length, or (None, (status, body)) explaining the problem."""
    values = headers.get_all("Content-Length") or []
    if not values:
        # Chunked or unsized bodies are not accepted; the client must declare the length.
        return None, (411, {"error": "Send a Content-Length header with the JSON body."})
    if len(set(value.strip() for value in values)) > 1:
        return None, (400, {"error": "Conflicting Content-Length headers."})
    value = values[0].strip()
    if not value.isascii() or not value.isdigit():
        return None, (400, {"error": "Content-Length must be a non-negative whole number of bytes."})
    length = int(value)
    if length > MAX_BODY_BYTES:
        return None, (413, {"error": f"Request body is too large; the limit is {MAX_BODY_BYTES} bytes."})
    return length, None


def create_server(bundle, host="127.0.0.1", port=8000, timeout=10):
    """Return an HTTP server bound to host:port; port 0 chooses a free port.

    `timeout` bounds how long one connection may take to send its request, so a
    client that declares more bytes than it sends cannot hold a thread forever.
    """

    connection_timeout = timeout

    class Handler(BaseHTTPRequestHandler):
        # Applied to the connection's socket; a slow or short body raises TimeoutError on read.
        timeout = connection_timeout

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
            length, problem = request_length(self.headers)
            if problem:
                return self._send(*problem)
            try:
                body = self.rfile.read(length)
            except TimeoutError:
                return self._send(408, {"error": "The request body did not arrive within the time limit."})
            if len(body) < length:
                return self._send(400, {"error": "The request body is shorter than its Content-Length."})
            try:
                record = json.loads(body)
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
