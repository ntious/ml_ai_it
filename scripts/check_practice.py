"""Execute only the registered, trusted practice/solution notebooks.

Starter feedback must remain unfinished; solutions must pass their visible
checks and actual development sandbox. These are separate evidence claims.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / 'curriculum/practice.json').read_text())['modules']


def checks_digest():
    return hashlib.sha256(b''.join((ROOT / 'src/practical_ml_ai' / name).read_bytes() for name in ['practice.py', 'practice_cases.py'])).hexdigest()

def validate_sources():
    from practical_ml_ai.practice import CHECKS
    registered = set()
    assert [entry['id'] for entry in REGISTRY] == list(range(1, 15))
    for entry in REGISTRY:
        lesson = ROOT / 'docs/lessons' / entry['slug'] / 'index.md'
        outcomes = re.search(r'## (?:Learning outcomes|What you will learn)\n(.*?)(?=\n## )', lesson.read_text(), re.S)[1].strip()
        assert hashlib.sha256(outcomes.encode()).hexdigest() == entry['outcomes_sha256'], 'Practice must preserve the learning outcomes: ' + str(lesson)
        assert len(entry['checks']) == 3 and set(entry['checks']) <= CHECKS.keys()
        for kind in ['practice', 'solutions']:
            source = ROOT / entry[kind]; registered.add(source.resolve())
            notebook = nbformat.read(source, as_version=4); nbformat.validate(notebook)
            assert notebook.metadata['teaching_prototype'] == {'module': entry['id'], 'kind': kind}
            functions = [cell for cell in notebook.cells if cell.metadata.get('practice_function')]
            assert len(functions) == 3
            assert all(('raise NotImplementedError' in cell.source) == (kind == 'practice') for cell in functions)
            for cell in notebook.cells:
                if cell.cell_type == 'code':
                    import ast
                    ast.parse(cell.source)
                    assert cell.execution_count is None and not cell.outputs
    assert registered == {p.resolve() for p in (ROOT / 'notebooks/practice').glob('*.ipynb')}
    print(f'Checked {2*len(REGISTRY)} clean practice/solution notebooks and unchanged outcomes in all 14 modules.')


def execute(entry, kernel):
    destination = ROOT / 'runs/verified/practice' / f"module{entry['id']:02d}"
    destination.mkdir(parents=True, exist_ok=True)
    summary = {'module': entry['id'], 'kernel': kernel, 'human_pilot': 'NOT RUN',
               'checks_sha256': checks_digest(), 'notebooks': {}}
    for kind in ['practice', 'solutions']:
        source = ROOT / entry[kind]
        notebook = nbformat.read(source, as_version=4)
        expected = 'not_attempted' if kind == 'practice' else 'passed'
        verification = f'''assert len(results) == 3
assert set(results) == {set(entry['checks'])!r}
assert all(item["state"] == {expected!r} for item in results.values()), results
assert demo_verified is {kind == 'solutions'!r}
import json, sys
from importlib.metadata import version, PackageNotFoundError
runtime = {{"python": sys.version.split()[0]}}
for package in ["numpy", "pandas", "scikit-learn", "matplotlib", "tensorflow-cpu"]:
    try:
        runtime[package] = version(package)
    except PackageNotFoundError:
        pass
print("PRACTICE_RUNTIME " + json.dumps(runtime))
print("PRACTICE_EVIDENCE", {kind!r}, {entry['id']}, {expected!r})'''
        notebook.cells.append(nbformat.v4.new_code_cell(verification))
        NotebookClient(notebook, timeout=900, kernel_name=kernel,
                       resources={'metadata': {'path': str(ROOT)}}).execute()
        evidence_cell = notebook.cells.pop()
        streams = ''.join(output.get('text', '') for output in evidence_cell.outputs if output.output_type == 'stream')
        runtime = json.loads(next(line.removeprefix('PRACTICE_RUNTIME ') for line in streams.splitlines() if line.startswith('PRACTICE_RUNTIME ')))
        nbformat.write(notebook, destination / f'{kind}-executed.ipynb')
        summary['notebooks'][kind] = {'source': entry[kind], 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                                      'state': expected, 'checks': 3, 'runtime': runtime, 'real_development_sandbox_executed': kind == 'solutions' and entry.get('sandbox') != 'authored_operation', 'worked_operation_executed': kind == 'solutions'}
        print(f"Module {entry['id']} {kind}: three checks {expected}; {entry.get('sandbox', 'real_development_sandbox')} {'executed' if kind == 'solutions' else 'skipped as intended'}.")
    (destination / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--group', choices=['core', 'frameworks', 'all'], default='all')
    parser.add_argument('--kernel', default='ml-ai-core')
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args()
    validate_sources()
    if not args.validate_only:
        for entry in REGISTRY:
            if args.group == 'all' or entry['profile'] == args.group:
                execute(entry, args.kernel)
