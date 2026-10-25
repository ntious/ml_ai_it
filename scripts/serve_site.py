"""Preview the generated site at its project prefix, including custom 404s.

This loopback-only server is a development aid, not production hosting. Build
the complete site first. Ctrl+C stops it; no source files are modified.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PREFIX = json.loads((ROOT / "curriculum/site.json").read_text(encoding="utf-8"))["base_path"]


class CourseHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        route = unquote(urlsplit(path).path)
        if not route.startswith(PREFIX):
            return str(SITE / "__outside_project_prefix__")
        candidate = (SITE / route[len(PREFIX):]).resolve()
        return str(candidate) if candidate.is_relative_to(SITE.resolve()) else str(SITE / "__outside_project_prefix__")

    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", PREFIX)
            self.end_headers()
            return
        super().do_GET()

    def send_error(self, code, message=None, explain=None):
        if code == 404 and (SITE / "404.html").is_file():
            content = (SITE / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(content)
            return
        super().send_error(code, message, explain)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    if not (SITE / "index.html").is_file():
        parser.error("Build site/ first; see docs/publishing.md.")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(CourseHandler, directory=str(SITE)))
    print(f"Preview: http://127.0.0.1:{args.port}{PREFIX}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
