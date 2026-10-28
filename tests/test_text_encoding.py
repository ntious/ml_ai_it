"""Course text is UTF-8; checks must not depend on the platform's default encoding.

Windows commonly defaults to cp1252, which cannot decode some UTF-8 punctuation
used in lessons. A crash there blocked the Windows core checks.
"""
import ast
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PYTHON_FOLDERS = ["apps", "examples", "projects", "scripts", "src", "tests"]


def default_encoding_calls(source):
    """Return line numbers of text-mode reads/writes that omit an encoding."""
    lines = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", None)
        keywords = {keyword.arg for keyword in node.keywords}
        if "encoding" in keywords or name not in {"read_text", "write_text", "open"}:
            continue
        if name == "open":
            receiver = getattr(node.func, "value", None)
            # Zip members are binary streams, not decoded text.
            if "archive" in getattr(receiver, "id", "") or "zip" in getattr(receiver, "id", "").lower():
                continue
            # Builtin open(file, mode); Path.open(mode).
            position = 1 if isinstance(node.func, ast.Name) else 0
            mode = next((keyword.value for keyword in node.keywords if keyword.arg == "mode"),
                        node.args[position] if len(node.args) > position else None)
            if isinstance(mode, ast.Constant) and "b" in str(mode.value):
                continue
        lines.append(node.lineno)
    return lines


class TextEncodingTests(unittest.TestCase):
    def test_scanner_flags_only_default_encoding_text_io(self):
        flagged = default_encoding_calls(
            "p.read_text()\np.read_text(encoding='utf-8')\np.write_text(s)\np.read_bytes()\n"
            "open(n)\nopen(n, 'rb')\nopen(n, encoding='utf-8')\narchive.open('member')\n"
            "path.open('w')\npath.open('rb')\n")
        self.assertEqual(flagged, [1, 3, 5, 9])

    def test_course_python_declares_text_encoding(self):
        offenders = []
        for folder in PYTHON_FOLDERS:
            for path in sorted((ROOT / folder).rglob("*.py")):
                for line in default_encoding_calls(path.read_text(encoding="utf-8")):
                    offenders.append(f"{path.relative_to(ROOT).as_posix()}:{line}")
        self.assertEqual(offenders, [], "Pass encoding='utf-8' for course text files.")

    @unittest.skipUnless(importlib.util.find_spec("nbformat"), "Practice validation needs the verification extra.")
    def test_practice_validation_runs_under_a_non_utf8_locale(self):
        environment = {key: value for key, value in os.environ.items() if key != "PYTHONUTF8"}
        # On Linux/macOS, the C locale without coercion selects ASCII; Windows keeps its code page.
        environment.update({"LC_ALL": "C", "LANG": "C", "PYTHONCOERCECLOCALE": "0",
                            "PYTHONPATH": os.pathsep.join(filter(None, [str(ROOT / "src"), os.environ.get("PYTHONPATH")]))})
        result = subprocess.run([sys.executable, "-X", "utf8=0", str(ROOT / "scripts/check_practice.py"), "--validate-only"],
                                cwd=ROOT, env=environment, capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(result.returncode, 0, result.stderr[-2000:])
        self.assertIn("unchanged outcomes in all 14 modules", result.stdout)


if __name__ == "__main__":
    unittest.main()
