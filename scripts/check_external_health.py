"""Check public documentation links and freshly downloaded pinned UCI archives."""
import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MAX_SOURCE_BYTES = 100_000_000


def constants(path):
    values = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                values[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return values


def sources(root=ROOT):
    shared = constants(root / "src/practical_ml_ai/continuation_data.py")["SOURCES"]
    entries = [{"name": name, "url": f"https://archive.ics.uci.edu/static/public/{s['id']}/{s['slug']}.zip", "sha256": s["sha256"]}
               for name, s in shared.items()]
    bike = constants(root / "src/practical_ml_ai/regression.py")
    iot = constants(root / "projects/rt-iot-triage/scripts/run.py")
    return entries + [{"name": "bike", "url": bike["UCI_URL"], "sha256": bike["UCI_ARCHIVE_SHA256"]},
                      {"name": "rt-iot", "url": iot["URL"], "sha256": iot["DIGEST"]}]


def links(root=ROOT):
    found = {}
    paths = [*root.glob("*.md")]
    for folder in ("docs", "projects", "templates"):
        paths.extend((root / folder).rglob("*.md"))
    for path in sorted(paths):
        text = re.sub(r"(?ms)^(```|~~~).*?^\1[^\n]*", "", path.read_text(encoding="utf-8"))
        for raw in re.findall(r'\]\((https?://[^\s\)]+)|<(https?://[^\s>]+)>', text):
            raw = next(value for value in raw if value)
            url = urldefrag(raw.rstrip(".,;`"))[0]
            found.setdefault(url, set()).add(path.relative_to(root).as_posix())
    return [(url, sorted(paths)) for url, paths in sorted(found.items())]


def exclusion(url):
    if urlsplit(url).hostname in {"localhost", "127.0.0.1", "::1"}:
        return "local development address, not a public link"
    if "TESTED_COMMIT" in url:
        return "documented revision placeholder"
    return None


def probe(url, expected=None, opener=urlopen, sleep=time.sleep):
    """GET once per attempt; source downloads never reuse caches or accept a new digest."""
    error = ""
    for attempt in range(3):
        try:
            request = Request(url, headers={"User-Agent": "ML-AI-course-health/1.0"})
            with opener(request, timeout=25) as response:
                if expected:
                    digest, size = hashlib.sha256(), 0
                    while chunk := response.read(1024 * 1024):
                        size += len(chunk)
                        if size > MAX_SOURCE_BYTES:
                            raise ValueError("Archive exceeds download limit")
                        digest.update(chunk)
                    observed = digest.hexdigest()
                    return {"ok": observed == expected, "observed_sha256": observed,
                            "detail": "checksum matches" if observed == expected else "checksum mismatch; manual review required"}
                return {"ok": True, "detail": f"HTTP {response.status}; fragment content not checked"}
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            error = str(exc)
            if isinstance(exc, HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                break
            if attempt < 2:
                sleep(2 ** attempt)
    return {"ok": False, "detail": error}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="runs/external-health.json")
    parser.add_argument("--sources-only", action="store_true")
    args = parser.parse_args()
    checks = [{**source, "kind": "source"} for source in sources()]
    if not args.sources_only:
        checks += [{"url": url, "locations": locations, "kind": "link"} for url, locations in links()]
    def check(item):
        reason = exclusion(item["url"]) if item["kind"] == "link" else None
        if reason:
            return {**item, "ok": True, "skipped": True, "detail": reason}
        return {**item, **probe(item["url"], item.get("sha256"))}
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, checks))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"checks": results, "failed": sum(not r["ok"] for r in results)}, indent=2) + "\n", encoding="utf-8")
    print(f"Checked {len(results)} endpoints; {sum(not r['ok'] for r in results)} need review. See {output}.")
    raise SystemExit(1 if any(not r["ok"] for r in results) else 0)


if __name__ == "__main__":
    main()
