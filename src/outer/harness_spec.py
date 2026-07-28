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

SCHEMA_VERSION = "h2spec/1.0"
# 0.1 specs are still accepted (declarative-only surface); 1.0 adds new_tools[]
# with generated implementation code, gated + reviewed at propose time.
_ACCEPTED_SCHEMAS = {"h2spec/0.1", "h2spec/1.0"}

# generated-tool structural limits (code SAFETY is enforced by outer.static_gates
# + the reviewer self-test, NOT here — this only checks the spec shape)
_TOOL_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{2,31}$")
_RESERVED_TOOL_NAMES = {"edit_solution", "evaluate_solution", "probe_solution",
                        "finish"}
_MAX_NEW_TOOLS = 3

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
             "tool_descriptions", "sampling", "agent", "middleware",
             "new_tools", "remove_tools", "new_skills", "new_middlewares"}

_SKILL_NAME_RE = re.compile(r"^[a-z][a-z0-9-]{2,39}$")
_MW_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{2,31}$")
_MW_HOOKS = {"before_model", "after_model", "before_tool", "after_tool"}
_MAX_NEW_SKILLS = 2
_MAX_NEW_MIDDLEWARES = 2


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
    if "schema" in data and data["schema"] not in _ACCEPTED_SCHEMAS:
        errors.append(f"schema must be one of {sorted(_ACCEPTED_SCHEMAS)}, got {data['schema']!r}")

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

    # --- generative surface (h2spec/1.0): new_tools[] + remove_tools[] ------
    if "remove_tools" in data:
        rt = data["remove_tools"]
        if not isinstance(rt, list) or not all(isinstance(x, str) for x in rt):
            errors.append("remove_tools: must be a list of tool names")
        else:
            # only optional built-ins may be removed; core edit/evaluate/finish stay
            removable = {"probe_solution"}
            bad = set(rt) - removable
            if bad:
                errors.append(f"remove_tools: not removable {sorted(bad)} "
                              f"(only {sorted(removable)})")
            else:
                out["remove_tools"] = sorted(set(rt))

    if "new_tools" in data:
        nt = data["new_tools"]
        if not isinstance(nt, list):
            errors.append("new_tools: must be a list")
        elif len(nt) > _MAX_NEW_TOOLS:
            errors.append(f"new_tools: {len(nt)} exceeds cap {_MAX_NEW_TOOLS}")
        else:
            seen, good_tools = set(), []
            for i, t in enumerate(nt):
                if not isinstance(t, dict):
                    errors.append(f"new_tools[{i}]: must be a mapping")
                    continue
                extra = set(t) - {"name", "description", "input_schema",
                                  "implementation_py"}
                if extra:
                    errors.append(f"new_tools[{i}]: unknown keys {sorted(extra)}")
                name = t.get("name")
                if not isinstance(name, str) or not _TOOL_NAME_RE.match(name or ""):
                    errors.append(f"new_tools[{i}].name: must match [a-z][a-z0-9_]{{2,31}}")
                elif name in _RESERVED_TOOL_NAMES:
                    errors.append(f"new_tools[{i}].name: {name!r} is reserved")
                elif name in seen:
                    errors.append(f"new_tools[{i}].name: duplicate {name!r}")
                else:
                    seen.add(name)
                desc = t.get("description")
                if not isinstance(desc, str) or not desc.strip() or len(desc) > 800:
                    errors.append(f"new_tools[{i}].description: non-empty string <=800 chars")
                code = t.get("implementation_py")
                if not isinstance(code, str) or "def run" not in code:
                    errors.append(f"new_tools[{i}].implementation_py: must be code defining run(ctx, args)")
                sch = t.get("input_schema", {"type": "object", "properties": {}})
                if not isinstance(sch, dict):
                    errors.append(f"new_tools[{i}].input_schema: must be a JSON-schema mapping")
                if name and name in seen and isinstance(code, str) and isinstance(desc, str):
                    good_tools.append({"name": name, "description": desc.strip(),
                                       "input_schema": sch,
                                       "implementation_py": code})
            if good_tools:
                out["new_tools"] = good_tools

    # --- new_skills[]: extra skill playbooks (pure text, no code risk) -------
    if "new_skills" in data:
        ns = data["new_skills"]
        if not isinstance(ns, list):
            errors.append("new_skills: must be a list")
        elif len(ns) > _MAX_NEW_SKILLS:
            errors.append(f"new_skills: {len(ns)} exceeds cap {_MAX_NEW_SKILLS}")
        else:
            seen, good = set(), []
            for i, s in enumerate(ns):
                if not isinstance(s, dict):
                    errors.append(f"new_skills[{i}]: must be a mapping"); continue
                extra = set(s) - {"name", "description", "body"}
                if extra:
                    errors.append(f"new_skills[{i}]: unknown keys {sorted(extra)}")
                name = s.get("name")
                if not isinstance(name, str) or not _SKILL_NAME_RE.match(name or ""):
                    errors.append(f"new_skills[{i}].name: must match [a-z][a-z0-9-]{{2,39}}")
                elif name in seen or name == "discovery-optimization":
                    errors.append(f"new_skills[{i}].name: duplicate/reserved {name!r}")
                else:
                    seen.add(name)
                desc = s.get("description", "")
                body = s.get("body")
                if not isinstance(body, str) or not body.strip() or len(body) > 8000:
                    errors.append(f"new_skills[{i}].body: non-empty string <=8000 chars")
                if name in seen and isinstance(body, str) and body.strip():
                    good.append({"name": name, "description": str(desc).strip()[:600],
                                 "body": body.strip()})
            if good:
                out["new_skills"] = good

    # --- new_middlewares[]: generated hooks (code — same safety chain) --------
    if "new_middlewares" in data:
        nm = data["new_middlewares"]
        if not isinstance(nm, list):
            errors.append("new_middlewares: must be a list")
        elif len(nm) > _MAX_NEW_MIDDLEWARES:
            errors.append(f"new_middlewares: {len(nm)} exceeds cap {_MAX_NEW_MIDDLEWARES}")
        else:
            seen, good = set(), []
            for i, mw in enumerate(nm):
                if not isinstance(mw, dict):
                    errors.append(f"new_middlewares[{i}]: must be a mapping"); continue
                extra = set(mw) - {"name", "description", "hook", "implementation_py"}
                if extra:
                    errors.append(f"new_middlewares[{i}]: unknown keys {sorted(extra)}")
                name = mw.get("name")
                if not isinstance(name, str) or not _MW_NAME_RE.match(name or ""):
                    errors.append(f"new_middlewares[{i}].name: must match [a-z][a-z0-9_]{{2,31}}")
                elif name in seen:
                    errors.append(f"new_middlewares[{i}].name: duplicate {name!r}")
                else:
                    seen.add(name)
                hook = mw.get("hook")
                if hook not in _MW_HOOKS:
                    errors.append(f"new_middlewares[{i}].hook: must be one of {sorted(_MW_HOOKS)}")
                code = mw.get("implementation_py")
                if not isinstance(code, str) or "def " not in code:
                    errors.append(f"new_middlewares[{i}].implementation_py: must be a hook function body")
                desc = mw.get("description", "")
                if name in seen and isinstance(code, str) and hook in _MW_HOOKS:
                    good.append({"name": name, "hook": hook,
                                 "description": str(desc).strip()[:600],
                                 "implementation_py": code})
            if good:
                out["new_middlewares"] = good

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
        **_read_generated(package_dir, agent),
    }


def _read_generated(package_dir: Path, agent: Dict[str, Any]) -> Dict[str, Any]:
    """Recover generated tools/skills/middlewares from a materialized package so
    the harness ratchet carries them forward — without this, every candidate's
    invented tools/skills/hooks vanish and M_phi must reinvent them each round.
    Reconstructs the h2spec/1.0 new_* fields from the package's own files."""
    out: Dict[str, Any] = {}
    reserved = {"discovery-optimization"}

    # generated tools: custom_tools/<name>.py bound via custom_runtime dispatcher
    ct_dir = package_dir / "custom_tools"
    if ct_dir.is_dir():
        by_name = {}
        for t in agent.get("tools", []):
            if "custom_runtime" in str(t.get("binding", "")):
                ty = package_dir / str(t["yaml_path"]).lstrip("./")
                desc, isch = "", {"type": "object", "properties": {}}
                if ty.exists():
                    doc = yaml.safe_load(ty.read_text()) or {}
                    desc = str(doc.get("description", "")).strip()
                    isch = doc.get("input_schema", isch)
                by_name[t["name"]] = (desc, isch)
        tools = []
        for py in sorted(ct_dir.glob("*.py")):
            name = py.stem
            desc, isch = by_name.get(name, ("", {"type": "object", "properties": {}}))
            tools.append({"name": name, "description": desc or f"generated tool {name}",
                          "input_schema": isch, "implementation_py": py.read_text()})
        if tools:
            out["new_tools"] = tools

    # generated skills: skills/<name>/SKILL.md beyond the base skill
    sk_root = package_dir / "skills"
    if sk_root.is_dir():
        skills = []
        for d in sorted(sk_root.iterdir()):
            if not d.is_dir() or d.name in reserved:
                continue
            md = d / "SKILL.md"
            if not md.exists():
                continue
            text = md.read_text()
            fm = re.match(r"---\n(.*?)\n---\n(.*)", text, re.DOTALL)
            if fm:
                meta = yaml.safe_load(fm.group(1)) or {}
                skills.append({"name": d.name,
                               "description": str(meta.get("description", "")).strip(),
                               "body": fm.group(2).strip()})
        if skills:
            out["new_skills"] = skills

    # generated middlewares: middlewares/<name>.py bound as GeneratedMiddleware
    gen_mw = [m for m in agent.get("middlewares", [])
              if str(m.get("import", "")).endswith(":GeneratedMiddleware")]
    mws = []
    for m in gen_mw:
        name = str(m["import"]).split(".")[1].split(":")[0]
        py = package_dir / "middlewares" / f"{name}.py"
        if not py.exists():
            continue
        src = py.read_text()
        # recover the ORIGINAL user hook body (between sentinels), not the
        # nexau-importing wrapper — re-gating the wrapper would fail the import
        # whitelist and drop the inherited middleware.
        seg = re.search(r"# --USER-HOOK-START--\n(.*?)\n# --USER-HOOK-END--", src, re.DOTALL)
        user_code = seg.group(1) if seg else src
        hook = next((h for h in _MW_HOOKS if f"def {h}(hook_input)" in user_code),
                    "before_model")
        mws.append({"name": name, "hook": hook,
                    "description": f"generated middleware {name}",
                    "implementation_py": user_code})
    if mws:
        out["new_middlewares"] = mws
    return out


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
    # generative surface (h2spec/1.0): tools are additive per candidate; the
    # base never carries new_tools, so a plain copy is the effective set.
    if "new_tools" in spec:
        eff["new_tools"] = spec["new_tools"]
    if "remove_tools" in spec:
        eff["remove_tools"] = spec["remove_tools"]
    if "new_skills" in spec:
        eff["new_skills"] = spec["new_skills"]
    if "new_middlewares" in spec:
        eff["new_middlewares"] = spec["new_middlewares"]
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
    # generative surface (h2spec/1.0): the base never carries these, so their
    # presence in the effective spec is itself a change
    for t in effective.get("new_tools", []):
        changed.append(f"new_tools.{t.get('name', '?')}")
    for sk in effective.get("new_skills", []):
        changed.append(f"new_skills.{sk.get('name', '?')}")
    for mw in effective.get("new_middlewares", []):
        changed.append(f"new_middlewares.{mw.get('name', '?')}")
    if effective.get("remove_tools"):
        changed.append("remove_tools")
    return (len(changed) > 0, changed)
