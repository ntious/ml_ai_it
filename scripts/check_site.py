"""Check generated links and basic semantic structure, not WCAG conformance."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "site"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.headings = set(), [], []
        self.main, self.language, self.title = False, None, False
        self.problems = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.problems.append("duplicate ID " + attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "html": self.language = attrs.get("lang")
        if tag == "main": self.main = True
        if tag == "title": self.title = True
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"): self.headings.append(int(tag[1]))
        if tag == "img" and "alt" not in attrs: self.problems.append("image missing alternative")
        if tag == "pre" and (attrs.get("tabindex") != "0" or not attrs.get("aria-label")):
            self.problems.append("code/text example missing a named keyboard-focus target")
        for name in ("href", "src"):
            if name in attrs: self.links.append(attrs[name])


pages = {}
for path in ROOT.rglob("*.html"):
    parser = Page(); parser.feed(path.read_text(encoding="utf-8")); pages[path.resolve()] = parser
assert pages, "No generated HTML pages found"
problems = []
for path, page in pages.items():
    if not page.language or not page.main or not page.title or page.headings.count(1) != 1:
        problems.append(f"{path.name}: missing language/main/title or incorrect H1 count")
    if "main" not in page.ids or "#main" not in page.links:
        problems.append(f"{path.name}: missing skip-link destination")
    for previous, following in zip(page.headings, page.headings[1:]):
        if following > previous + 1: problems.append(f"{path.name}: heading level skipped")
    problems.extend(f"{path.name}: {problem}" for problem in page.problems)
    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc: continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if target.is_dir(): target = target / "index.html"
        if not target.is_relative_to(ROOT.resolve()) or not target.exists():
            problems.append(f"{path.name}: broken or escaping local link {link}")
        elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
            problems.append(f"{path.name}: missing fragment {link}")
assert not problems, "\n".join(problems)
print(f"Checked {len(pages)} pages: local links/fragments, language, title, main/skip link, heading order, image alternatives. Manual accessibility testing remains required.")
