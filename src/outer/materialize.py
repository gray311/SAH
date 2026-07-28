"""Materialize an effective HarnessSpec into a full candidate H2 package.

Layout (matches the scaffold in src/inner/harness_candidate/candNN/):

    <cand_dir>/
    ├── agent.yaml                  # NexAU agent config (spec sampling/iteration/middleware params)
    ├── prompt.md                   # system prompt (spec.system_prompt)
    ├── spec.yaml                   # the raw partial spec M_phi generated (provenance)
    ├── meta.json                   # round/k/hash/changed-fields/raw generation pointer
    ├── tools/                      # tool schemas (descriptions from spec); bindings = shared executor code
    ├── skills/discovery-optimization/SKILL.md
    └── middlewares/                # per-candidate copy of the middleware code, imported as
        └── budget_reminder.py      #   middlewares.budget_reminder (cand_dir goes on sys.path)

Deterministic compilation: same effective spec -> byte-identical package
(modulo meta.json provenance fields).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

INNER_HARNESS = Path(__file__).resolve().parents[1] / "inner" / "harness"

_TOOL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "edit_solution": {
        "input_schema": {
            "type": "object",
            "properties": {"code": {"type": "string",
                                    "description": "Either SEARCH/REPLACE diff block(s) to apply to the current program, or the full replacement body for the EVOLVE-BLOCK region."}},
            "required": ["code"],
            "additionalProperties": False,
        },
    },
    "evaluate_solution": {
        "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "probe_solution": {
        "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
        "default_description": (
            "Cheaply score the CURRENT program on SUBSAMPLED data (~2000 rows). "
            "Fast; does NOT consume the evaluation budget; approximate and NOT "
            "comparable to full scores — use it to rank variants when full "
            "evaluation is slow, then confirm with evaluate_solution."),
    },
    "finish": {
        "input_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string", "minLength": 1,
                                       "description": "One line on the final approach and best score."}},
            "required": ["summary"],
            "additionalProperties": False,
        },
    },
}


_BUILTIN_OPTIONAL = {"probe_solution"}

# generated-middleware wrapper: the model supplies just the hook function body;
# we wrap it in a NexAU Middleware subclass that fails OPEN (a crashing hook
# never kills the rollout) and only ever appends a framework message.
_MW_WRAPPER = '''"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

{user_code}

class GeneratedMiddleware(Middleware):
    def {hook}(self, hook_input):
        try:
            note = {hook}(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
'''


def _build_skill_list(effective: Dict[str, Any], cand_dir: Path) -> list:
    """Materialize M_phi-generated skills into skills/<name>/SKILL.md."""
    out = []
    for sk in effective.get("new_skills", []):
        name = sk["name"]
        d = cand_dir / "skills" / name
        d.mkdir(parents=True, exist_ok=True)
        header = f"# {name}\n\n{sk.get('description', '').strip()}\n\n"
        (d / "SKILL.md").write_text(header + sk["body"].strip() + "\n")
        out.append(f"./skills/{name}")
    return out


def _build_custom_middlewares(effective: Dict[str, Any], cand_dir: Path) -> list:
    """Materialize generated middleware code (gated+reviewed at propose time)
    into middlewares/<name>.py wrapped in a fail-open Middleware subclass."""
    out = []
    for mw in effective.get("new_middlewares", []):
        name = mw["name"]
        (cand_dir / "middlewares").mkdir(parents=True, exist_ok=True)
        code = _MW_WRAPPER.format(user_code=mw["implementation_py"].strip(),
                                  hook=mw["hook"])
        (cand_dir / "middlewares" / f"{name}.py").write_text(code)
        out.append({"import": f"middlewares.{name}:GeneratedMiddleware", "params": {}})
    return out


def _build_tool_list(effective: Dict[str, Any], cand_dir: Path) -> list:
    """Assemble agent.yaml tool entries: core built-ins (minus removed
    optionals) + generated custom tools (h2spec/1.0)."""
    removed = set(effective.get("remove_tools", []))
    builtins = [n for n in ("edit_solution", "evaluate_solution",
                            "probe_solution", "finish")
                if n not in (removed & _BUILTIN_OPTIONAL)]
    tools = [{"name": n, "yaml_path": f"./tools/{n}.tool.yaml",
              "binding": f"inner.harness.tools.discovery:{n}"} for n in builtins]
    for t in effective.get("new_tools", []):
        name = t["name"]
        (cand_dir / "custom_tools").mkdir(exist_ok=True)
        (cand_dir / "custom_tools" / f"{name}.py").write_text(t["implementation_py"])
        (cand_dir / "tools" / f"{name}.tool.yaml").write_text(_yaml_str({
            "type": "tool", "name": name,
            "description": t["description"],
            "input_schema": t.get("input_schema") or {"type": "object", "properties": {}},
        }))
        # bind every generated tool to the single dispatcher; its source path
        # rides through NexAU extra_kwargs (merged into the tool call params)
        src = str((cand_dir / "custom_tools" / f"{name}.py").resolve())
        tools.append({"name": name, "yaml_path": f"./tools/{name}.tool.yaml",
                      "binding": "inner.harness.tools.custom_runtime:custom_tool",
                      "extra_kwargs": {"py_path": src}})
    return tools


def _yaml_str(data: Dict[str, Any]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)


def materialize(effective: Dict[str, Any], cand_dir: Path, *,
                raw_spec_text: str = "", meta: Optional[Dict[str, Any]] = None) -> Path:
    """Write the full candidate package for ``effective`` (a FULL merged spec)."""
    cand_dir = Path(cand_dir)
    if cand_dir.exists():
        shutil.rmtree(cand_dir)
    (cand_dir / "tools").mkdir(parents=True)
    (cand_dir / "skills" / "discovery-optimization").mkdir(parents=True)
    (cand_dir / "middlewares").mkdir(parents=True)

    # --- prompt.md (system prompt) --- #
    (cand_dir / "prompt.md").write_text(effective["system_prompt"].rstrip() + "\n")

    # --- skill --- #
    skill = "---\nname: discovery-optimization\ndescription: " + \
        json.dumps(effective.get("skill_description", "").strip()) + \
        "\n---\n\n" + effective.get("skill_body", "").rstrip() + "\n"
    (cand_dir / "skills" / "discovery-optimization" / "SKILL.md").write_text(skill)

    # --- tools (descriptions from spec; bindings = fixed executor contract) --- #
    tool_descs = effective.get("tool_descriptions", {})
    for name, schema in _TOOL_SCHEMAS.items():
        doc = {"type": "tool", "name": name,
               "description": tool_descs.get(name, "").strip()
                              or schema.get("default_description")
                              or f"The {name} tool.",
               "input_schema": schema["input_schema"]}
        (cand_dir / "tools" / f"{name}.tool.yaml").write_text(_yaml_str(doc))

    # --- middleware code copy (imported per-process as middlewares.budget_reminder) --- #
    (cand_dir / "middlewares" / "__init__.py").write_text("# candidate middleware package\n")
    src_mw = INNER_HARNESS / "middleware" / "budget_reminder.py"
    mw_text = src_mw.read_text().replace(
        "from inner.harness.tools.runtime import get_session",
        "from inner.harness.tools.runtime import get_session  # shared session bridge (fixed runtime)",
    )
    (cand_dir / "middlewares" / "budget_reminder.py").write_text(mw_text)
    sr_text = (INNER_HARNESS / "middleware" / "stall_restart.py").read_text().replace(
        "from inner.harness.tools.runtime import get_session",
        "from inner.harness.tools.runtime import get_session  # shared session bridge (fixed runtime)",
    )
    (cand_dir / "middlewares" / "stall_restart.py").write_text(sr_text)

    # --- agent.yaml --- #
    sampling = effective.get("sampling", {})
    agent_p = effective.get("agent", {})
    mw_p = effective.get("middleware", {})
    agent = {
        "type": "agent",
        "name": "inner_h2_candidate",
        "description": "Candidate H2 generated by the outer loop (M_phi + H1).",
        "max_context_tokens": 131072,
        "system_prompt": "./prompt.md",
        "system_prompt_type": "file",
        "tool_call_mode": "structured",
        "max_iterations": int(agent_p.get("max_iterations", 36)),
        "retry_attempts": 2,
        "retry_backoff_max_seconds": 30,
        "timeout": 600,
        "llm_config": {
            "model": "qwen3.5-9b",           # overridden at runtime by harness_runner
            "base_url": "http://127.0.0.1:8800/v1",
            "api_key": "EMPTY",
            "api_type": "openai_chat_completion",
            "max_tokens": int(sampling.get("max_tokens", 8192)),
            "temperature": float(sampling.get("temperature", 0.7)),
            "top_p": float(sampling.get("top_p", 0.95)),
            "stream": False,
        },
        "sandbox_config": {"type": "local", "work_dir": "/tmp"},
        "tools": _build_tool_list(effective, cand_dir),
        "stop_tools": ["finish"],
        "skills": ["./skills/discovery-optimization"] + _build_skill_list(effective, cand_dir),
        "middlewares": _build_custom_middlewares(effective, cand_dir) + [
            {"import": "middlewares.budget_reminder:BudgetReminderMiddleware",
             "params": {"remind_from_left": int(mw_p.get("budget_reminder_from_left", 3))}},
            {"import": "middlewares.stall_restart:StallRestartMiddleware",
             "params": {"stall_after": int(mw_p.get("stall_after", 8)),
                        "max_restarts": int(mw_p.get("max_restarts", 2))}},
            {"import": "nexau.archs.main_sub.execution.middleware.long_tool_output:LongToolOutputMiddleware",
             "params": {"max_output_chars": int(mw_p.get("long_tool_output_max_chars", 8000)),
                        "head_lines": 40, "tail_lines": 20,
                        "head_chars": 4000, "tail_chars": 4000,
                        "bypass_tool_names": ["finish", "LoadSkill"]}},
            {"import": "nexau.archs.main_sub.execution.middleware.round_and_token_reminder:RoundAndTokenReminderMiddleware",
             "params": {"max_context_tokens": 131072,
                        "desired_max_tokens": int(sampling.get("max_tokens", 8192))}},
        ],
        "tracers": [{"import": "nexau.archs.tracer.adapters.in_memory:InMemoryTracer"}],
    }
    (cand_dir / "agent.yaml").write_text(_yaml_str(agent))

    # --- provenance --- #
    if raw_spec_text:
        (cand_dir / "spec.yaml").write_text(raw_spec_text.rstrip() + "\n")
    (cand_dir / "meta.json").write_text(json.dumps(meta or {}, indent=2))
    # note: the candidate's spec sampling top_k is applied at runtime via extra_body
    return cand_dir
