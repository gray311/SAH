"""Runtime dispatcher for M_phi-generated custom tools (h2spec/1.0).

A materialized candidate carries its generated tools under
``custom_tools/<name>.py`` (each defining ``def run(ctx, args): ...``, already
static-gated and reviewer-passed at propose time). agent.yaml binds every such
tool to this single dispatcher, passing the source path through NexAU
``extra_kwargs``:

    tools:
      - name: sample_hit_probe
        yaml_path: ./tools/sample_hit_probe.tool.yaml
        binding: inner.harness.tools.custom_runtime:custom_tool
        extra_kwargs: {py_path: /abs/path/custom_tools/sample_hit_probe.py}

The dispatcher builds a fresh :class:`ToolContext` per call over the active
session (contextvar bridge), so generated code reaches only the audited
capability surface. Return values are stringified and every exception is
trapped — a crashing custom tool must never kill the rollout.
"""
from __future__ import annotations

import json
import tempfile
import traceback
from pathlib import Path
from typing import Any, Callable, Dict

from inner.harness.tools.runtime import get_session
from inner.harness_sdk import ToolContext

_CACHE: Dict[str, Callable] = {}


def _load_run(py_path: str) -> Callable:
    fn = _CACHE.get(py_path)
    if fn is not None:
        return fn
    ns: Dict[str, Any] = {}
    exec(compile(Path(py_path).read_text(), py_path, "exec"), ns)  # gated + reviewed upstream
    fn = ns.get("run")
    if not callable(fn):
        raise ValueError(f"custom tool {py_path} defines no run()")
    _CACHE[py_path] = fn
    return fn


def custom_tool(py_path: str = "", **kwargs: Any) -> str:
    """Generic binding for every generated tool; ``py_path`` comes from
    extra_kwargs, the model-supplied arguments arrive as ``kwargs``."""
    if not py_path:
        return "custom tool error: no py_path bound"
    try:
        session = get_session()
    except Exception:
        return "custom tool error: no active session"
    scratch = Path(tempfile.gettempdir()) / "sah_custom_scratch"
    ctx = ToolContext(session, scratch)
    try:
        out = _load_run(py_path)(ctx, dict(kwargs))
    except Exception:
        return "custom tool raised (ignored):\n" + traceback.format_exc(limit=3)[-600:]
    if isinstance(out, str):
        return out[:8000]
    try:
        return json.dumps(out)[:8000]
    except Exception:
        return str(out)[:8000]
