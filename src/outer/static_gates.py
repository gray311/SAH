"""Static safety gates for M_phi-generated tool code (h2spec/1.0).

Fail-closed: any violation returns errors and the code is rejected (the
candidate can still be repaired by the reviewer before final rejection).

The contract for generated code:
  * defines exactly one top-level ``def run(ctx, args):``
  * imports only from IMPORT_WHITELIST
  * never touches filesystem/process/network primitives directly — all side
    effects go through the ``ctx`` capability object (see inner/harness_sdk.py)
"""
from __future__ import annotations

import ast
from typing import List, Tuple

IMPORT_WHITELIST = {
    "math", "re", "json", "itertools", "functools", "collections", "heapq",
    "bisect", "random", "statistics", "string", "typing", "dataclasses",
    "numpy", "pandas",
}
FORBIDDEN_NAMES = {
    "open", "exec", "eval", "compile", "__import__", "input", "breakpoint",
    "globals", "locals", "vars", "memoryview", "exit", "quit",
}
FORBIDDEN_MODULES = {
    "os", "sys", "subprocess", "socket", "shutil", "pathlib", "importlib",
    "ctypes", "multiprocessing", "threading", "signal", "resource", "pickle",
    "requests", "urllib", "http", "ftplib", "telnetlib", "builtins", "io",
}
MAX_CODE_CHARS = 6000


def check_tool_code(code: str) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if len(code) > MAX_CODE_CHARS:
        errors.append(f"code exceeds {MAX_CODE_CHARS} chars")
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, [f"syntax error: {e}"]

    run_defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run"]
    if len(run_defs) != 1:
        errors.append("must define exactly one top-level `def run(ctx, args):`")
    elif [a.arg for a in run_defs[0].args.args][:2] != ["ctx", "args"]:
        errors.append("run() signature must be (ctx, args)")

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in node.names] if isinstance(node, ast.Import) \
                else [node.module or ""]
            for m in mods:
                root = m.split(".")[0]
                if root in FORBIDDEN_MODULES:
                    errors.append(f"forbidden import: {m}")
                elif root not in IMPORT_WHITELIST:
                    errors.append(f"import not in whitelist: {m}")
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            errors.append(f"forbidden builtin: {node.id}")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__") \
                and node.attr not in ("__init__",):
            errors.append(f"forbidden dunder access: .{node.attr}")
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            errors.append("global/nonlocal not allowed")

    return (not errors), sorted(set(errors))
