"""Validate source Markdown links, including published reading-site downloads."""
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
PAGES_DOWNLOADS='https://ntious.github.io/ml_ai_it/downloads/'
files=[*ROOT.glob('*.md'),*(ROOT/'docs').rglob('*.md'),*(ROOT/'templates').rglob('*.md'),*(ROOT/'projects').rglob('*.md')]
OFFLINE=ROOT/'docs/setup/student-workspace.md'
OFFLINE_ANCHOR='student-workspace.md#if-a-download-link-does-not-open'
problems=[];count=0
for source in files:
    text=source.read_text(encoding='utf-8')
    # Site downloads can be unavailable; learners must meet the offline route at or before the first one.
    first=re.search(r'"site-download:',text)
    if first and source!=OFFLINE:
        end=text.find('\n\n',first.start())
        if OFFLINE_ANCHOR not in text[:len(text) if end<0 else end]:
            problems.append(f'{source.relative_to(ROOT)}: link the offline access route at or before the first site download')
    for match in re.finditer(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"([^"]*)")?\)',text):
        url=urlsplit(match.group(1))
        # Generated downloads exist only on the published reading site.
        if (match.group(2) or '').startswith('site-download:'):
            name=match.group(2).removeprefix('site-download:')
            if match.group(1)!=PAGES_DOWNLOADS+name:problems.append(f'{source.relative_to(ROOT)}: download link must be {PAGES_DOWNLOADS+name}')
            continue
        if url.scheme or url.netloc:continue
        target=(source.parent/unquote(url.path)).resolve() if url.path else source
        count+=1
        if not target.is_relative_to(ROOT) or not target.is_file():
            problems.append(f'{source.relative_to(ROOT)}: {match.group(1)}')
        elif url.fragment and target.suffix=='.md':
            headings=re.findall(r'^#{1,6} (.+)$',target.read_text(encoding='utf-8'),re.M)
            ids=[re.sub(r'[^a-z0-9]+','-',heading.lower()).strip('-') for heading in headings]
            if unquote(url.fragment) not in ids:problems.append(f'{source.relative_to(ROOT)}: missing source heading {match.group(1)}')
assert not problems,'\n'.join(problems)
print(f'Checked {count} local source Markdown destinations/fragments, independently of generated-site links.')
