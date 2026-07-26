"""HarnessSpec v0.1 — the typed genome of an H2 candidate (plan.md §5).

The proposer M_phi emits a YAML spec; this module validates it fail-closed,
canonicalizes it, and hashes it. The spec controls only declarative surface:
prompts, skill text, tool descriptions, sampling, and iteration/middleware
parameters. Tool *code* (the executor contract) and the evaluation budget are
NOT part of the spec — the budget is enforced externally (plan.md §8.4) and
code changes are out of scope for the MVP action space.

A spec is *relative to a base package*: missing fields inherit the base value,
so M_phi can express a targeted mutation without regenerating everything. A
candidate identical to its base (canonical hash) is invalid.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

SCHEMA_VERSION = "h2spec/0.1"

# field -> (type, max_chars) for text fields
_TEXT_FIELDS = {
    "system_prompt": 8000,
    "skill_description": 600,
    "skill_body": 8000,
}
_TOOL_DESC_FIELDS = {  # tool name -> max chars
    "edit_solution": 1600,
    "evaluate_solution": 1000,
    "probe_solution": 1000,
    "finish": 600,
}
# numeric field -> (min, max, is_int)
_SAMPLING_FIELDS = {
    "temperature": (0.0, 1.5, False),
    "top_p": (0.05, 1.0, False),
    "top_k": (1, 100, True),
    "max_tokens": (1024, 16384, True),
}
_AGENT_FIELDS = {
    "max_iterations": (8, 80, True),
}
_MIDDLEWARE_FIELDS = {
    "budget_reminder_from_left": (0, 10, True),
    "long_tool_output_max_chars": (2000, 20000, True),
}
_TOP_KEYS = {"schema", "system_prompt", "skill_description", "skill_body",
             "tool_descriptions", "sampling", "agent", "middleware"}


@dataclass
class SpecValidation:
    valid: bool
    errors: List[str] = field(default_factory=list)
    spec: Optional[Dict[str, Any]] = None  # canonical (validated, defaults NOT folded in)


def _check_num(errors: List[str], group: str, key: str, val: Any,
               lo: float, hi: float, is_int: bool) -> Any:
    if is_int:
        if isinstance(val, bool) or not isinstance(val, int):
            errors.append(f"{group}.{key}: expected int, got {type(val).__name__}")
            return None
    elif not isinstance(val, (int, float)) or isinstance(val, bool):
        errors.append(f"{group}.{key}: expected number, got {type(val).__name__}")
        return None
    if not (lo <= val <= hi):
        errors.append(f"{group}.{key}: {val} outside [{lo}, {hi}]")
        return None
    return int(val) if is_int else float(val)


def parse_and_validate(text: str) -> SpecValidation:
    """Parse a raw YAML spec (optionally inside ```yaml fences) fail-closed."""
    m = re.search(r"```(?:yaml|yml)?\s*\n(.*?)```", text, re.DOTALL)
    raw = m.group(1) if m else text
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return SpecValidation(False, [f"yaml parse error: {str(e)[:200]}"])
    if not isinstance(data, dict):
        return SpecValidation(False, [f"spec must be a mapping, got {type(data).__name__}"])

    errors: List[str] = []
    unknown = set(data) - _TOP_KEYS
    if unknown:
        errors.append(f"unknown top-level keys (fail closed): {sorted(unknown)}")

    out: Dict[str, Any] = {"schema": SCHEMA_VERSION}
    if "schema" in data and data["schema"] != SCHEMA_VERSION:
        errors.append(f"schema must be {SCHEMA_VERSION!r}, got {data['schema']!r}")

    for key, cap in _TEXT_FIELDS.items():
        if key in data:
            v = data[key]
            if not isinstance(v, str) or not v.strip():
                errors.append(f"{key}: must be a non-empty string")
            elif len(v) > cap:
                errors.append(f"{key}: {len(v)} chars exceeds cap {cap}")
            else:
                out[key] = v.strip()

    if "tool_descriptions" in data:
        td = data["tool_descriptions"]
        if not isinstance(td, dict):
            errors.append("tool_descriptions: must be a mapping")
        else:
            bad = set(td) - set(_TOOL_DESC_FIELDS)
            if bad:
                errors.append(f"tool_descriptions: unknown tools {sorted(bad)}")
            good = {}
            for name, cap in _TOOL_DESC_FIELDS.items():
                if name in td:
                    v = td[name]
                    if not isinstance(v, str) or not v.strip():
                        errors.append(f"tool_descriptions.{name}: must be a non-empty string")
                    elif len(v) > cap:
                        errors.append(f"tool_descriptions.{name}: {len(v)} chars exceeds cap {cap}")
                    else:
                        good[name] = v.strip()
            if good:
                out["tool_descriptions"] = good

    for group, fields_def in (("sampling", _SAMPLING_FIELDS), ("agent", _AGENT_FIELDS),
                              ("middleware", _MIDDLEWARE_FIELDS)):
        if group in data:
            g = data[group]
            if not isinstance(g, dict):
                errors.append(f"{group}: must be a mapping")
                continue
            bad = set(g) - set(fields_def)
            if bad:
                errors.append(f"{group}: unknown keys {sorted(bad)}")
            good = {}
            for key, (lo, hi, is_int) in fields_def.items():
                if key in g:
                    v = _check_num(errors, group, key, g[key], lo, hi, is_int)
                    if v is not None:
                        good[key] = v
            if good:
                out[group] = good

    mutated = set(out) - {"schema"}
    if not mutated:
        errors.append("spec mutates nothing (all fields missing/invalid)")

    if errors:
        return SpecValidation(False, errors)
    return SpecValidation(True, [], out)


def canonical_json(spec: Dict[str, Any]) -> str:
    return json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def spec_hash(spec: Dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(spec).encode()).hexdigest()[:16]


# --------------------------------------------------------------------------- #
# Base-spec extraction: read the current best H2 package into spec form so the
# proposer sees the genome it is mutating and diffs are well-defined.
# --------------------------------------------------------------------------- #
def read_base_spec(package_dir: Path) -> Dict[str, Any]:
    """Extract the mutable surface of an existing H2 package as a full spec."""
    package_dir = Path(package_dir)
    agent = yaml.safe_load((package_dir / "agent.yaml").read_text())

    sys_file = package_dir / str(agent.get("system_prompt", "./system.md")).lstrip("./")
    if not sys_file.exists():  # candidate packages use prompt.md
        for alt in ("system.md", "prompt.md"):
            if (package_dir / alt).exists():
                sys_file = package_dir / alt
                break
    skill_dirs = [package_dir / str(s).lstrip("./") for s in agent.get("skills", [])]
    skill_md = next((d / "SKILL.md" for d in skill_dirs if (d / "SKILL.md").exists()), None)

    skill_desc, skill_body = "", ""
    if skill_md is not None:
        text = skill_md.read_text()
        fm = re.match(r"---\n(.*?)\n---\n(.*)", text, re.DOTALL)
        if fm:
            meta = yaml.safe_load(fm.group(1)) or {}
            skill_desc = str(meta.get("description", ""))
            skill_body = fm.group(2).strip()
        else:
            skill_body = text.strip()

    tool_descs = {}
    for t in agent.get("tools", []):
        ty = package_dir / str(t["yaml_path"]).lstrip("./")
        if ty.exists():
            tdoc = yaml.safe_load(ty.read_text())
            if tdoc.get("name") in _TOOL_DESC_FIELDS:
                tool_descs[tdoc["name"]] = str(tdoc.get("description", "")).strip()

    llm = agent.get("llm_config", {}) or {}
    mw_params: Dict[str, int] = {}
    for mw in agent.get("middlewares", []):
        imp, params = str(mw.get("import", "")), mw.get("params", {}) or {}
        if "budget_reminder" in imp:
            mw_params["budget_reminder_from_left"] = int(params.get("remind_from_left", 3))
        if "long_tool_output" in imp:
            mw_params["long_tool_output_max_chars"] = int(params.get("max_output_chars", 8000))

    return {
        "schema": SCHEMA_VERSION,
        "system_prompt": sys_file.read_text().strip(),
        "skill_description": skill_desc.strip(),
        "skill_body": skill_body,
        "tool_descriptions": tool_descs,
        "sampling": {
            "temperature": float(llm.get("temperature", 0.7)),
            "top_p": float(llm.get("top_p", 0.95)),
            "top_k": 20,
            "max_tokens": int(llm.get("max_tokens", 8192)),
        },
        "agent": {"max_iterations": int(agent.get("max_iterations", 36))},
        "middleware": mw_params or {"budget_reminder_from_left": 3,
                                    "long_tool_output_max_chars": 8000},
    }


def merge_with_base(spec: Dict[str, Any], base: Dict[str, Any]) -> Dict[str, Any]:
    """Fold a (validated, partial) spec over the base spec -> full effective spec."""
    eff = json.loads(json.dumps(base))  # deep copy
    for key in _TEXT_FIELDS:
        if key in spec:
            eff[key] = spec[key]
    if "tool_descriptions" in spec:
        eff.setdefault("tool_descriptions", {}).update(spec["tool_descriptions"])
    for group in ("sampling", "agent", "middleware"):
        if group in spec:
            eff.setdefault(group, {}).update(spec[group])
    eff["schema"] = SCHEMA_VERSION
    return eff


def differs_from_base(effective: Dict[str, Any], base: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Which fields does the effective spec actually change vs the base?"""
    changed: List[str] = []
    for key in _TEXT_FIELDS:
        if effective.get(key, "").strip() != base.get(key, "").strip():
            changed.append(key)
    for name in _TOOL_DESC_FIELDS:
        if (effective.get("tool_descriptions", {}).get(name, "").strip()
                != base.get("tool_descriptions", {}).get(name, "").strip()):
            changed.append(f"tool_descriptions.{name}")
    for group in ("sampling", "agent", "middleware"):
        for key, val in effective.get(group, {}).items():
            if val != base.get(group, {}).get(key):
                changed.append(f"{group}.{key}")
    return (len(changed) > 0, changed)
