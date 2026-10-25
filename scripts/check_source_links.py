"""Validate source Markdown links, including the GitHub artifact-access route."""
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
files=[*ROOT.glob('*.md'),*(ROOT/'docs').rglob('*.md'),*(ROOT/'templates').rglob('*.md')]
problems=[];count=0
for source in files:
    text=source.read_text(encoding='utf-8')
    for match in re.finditer(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',text):
        url=urlsplit(match.group(1))
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
