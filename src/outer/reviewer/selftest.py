"""Subprocess self-test for generated tool code.

Runs ``run(MockContext, {})`` in an isolated python with a hard timeout and
resource limits. A tool passes if it returns without raising; its return value
must be str/dict/list/number (JSON-representable-ish).
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Tuple

_RUNNER = r'''
import json, resource, sys
resource.setrlimit(resource.RLIMIT_CPU, (20, 20))
resource.setrlimit(resource.RLIMIT_AS, (6 << 30, 6 << 30))
sys.path.insert(0, {src_path!r})
from inner.harness_sdk import MockContext
ns = {{}}
code = open({code_path!r}).read()
exec(compile(code, "generated_tool.py", "exec"), ns)
ctx = MockContext({scratch!r})
try:
    out = ns["run"](ctx, {{}})
except Exception as e:
    import traceback
    print(json.dumps({{"ok": False, "error": traceback.format_exc(limit=4)[-1200:]}}))
    raise SystemExit(0)
ok_types = (str, dict, list, int, float, type(None))
if not isinstance(out, ok_types):
    print(json.dumps({{"ok": False, "error": f"run() returned {{type(out).__name__}}; must be str/dict/list/number"}}))
else:
    print(json.dumps({{"ok": True, "ctx_calls": ctx.calls, "ret_type": type(out).__name__}}))
'''


def selftest_tool_code(code: str, timeout_s: float = 30.0) -> Tuple[bool, str]:
    """Returns (passed, detail)."""
    src_path = str(Path(__file__).resolve().parents[2])  # .../src
    with tempfile.TemporaryDirectory(prefix="tool_selftest_") as td:
        code_path = Path(td) / "generated_tool.py"
        code_path.write_text(code)
        runner = _RUNNER.format(src_path=src_path, code_path=str(code_path),
                                scratch=str(Path(td) / "scratch"))
        try:
            r = subprocess.run([sys.executable, "-c", runner],
                               capture_output=True, text=True, timeout=timeout_s)
        except subprocess.TimeoutExpired:
            return False, f"self-test timeout ({timeout_s}s)"
        line = (r.stdout or "").strip().splitlines()
        if not line:
            return False, f"self-test produced no verdict; stderr: {(r.stderr or '')[-400:]}"
        try:
            d = json.loads(line[-1])
        except Exception:
            return False, f"unparseable verdict: {line[-1][:200]}"
        return bool(d.get("ok")), d.get("error") or json.dumps(
            {k: d[k] for k in ("ctx_calls", "ret_type") if k in d})
