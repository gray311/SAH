"""Adaptive V1 proposal path built on SAH's native H2 surface.

Adaptive owns the evidence memory, sequential exploration policy, dual-frontier
controller, policy-update schedule, context-analysis team, and standalone NexAU
H1 proposer. Candidate construction still reuses SAH's ``h2spec/1.0``
validator, submitter, generated-code safety gates, materializer, and native
NexAU H2 package format.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import os
import re
import statistics
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence

import yaml

from outer import harness_spec as hs
from outer import propose as sah_propose
from outer import proposer_io as pio
from outer.materialize import materialize
from outer.propose_session import ProposeSession, propose_scope
from protocols.adaptive_v1_analysis import (
    ANALYSIS_VERSION,
    analysis_package_hash,
    build_analysis_dossier,
    run_context_analysis,
    write_analysis_artifacts,
)
from protocols.adaptive_v1_tokens import count_chat_tokens

PROTOCOL = "adaptive_v1"
STATE_SCHEMA = "sah.adaptive-v1-state/1"
H1_VERSION = "adaptive-h1/3.4-diverse-native-contracts"
EPS = 1e-12
ADAPTIVE_CONTEXT_SCHEMA = "sah.adaptive-v1-proposer-context/2"
ADAPTIVE_CONTEXT_MAX_CHARS = 12_000
ADAPTIVE_CONTEXT_MAX_ESTIMATED_TOKENS = 4_000
ADAPTIVE_CONTEXT_HISTORY_LIMIT = 8
PROPOSER_MAX_INPUT_TOKENS = 23_000
PROPOSER_PROMPT_INJECTION_MARGIN = 1_024
_ADAPTIVE_CTX_CAPABILITIES = {
    "get_program",
    "get_best_program",
    "best_score",
    "stage_edit",
    "probe",
    "evaluate",
    "budget_left",
    "list_task_inputs",
    "read_input_sample",
    "read_input_df",
    "scratch_write",
    "scratch_read",
    "log",
}
_DYNAMIC_ATTRIBUTE_BUILTINS = {
    "getattr",
    "setattr",
    "delattr",
    "hasattr",
    "dir",
    "vars",
}

# Adaptive has its own NexAU H1 root so its prompt/context budgets can evolve
# without modifying SAH's native H1. It deliberately reuses SAH's validator,
# submitter, reviewer, materializer, and harness-design skill.
ADAPTIVE_H1_PACKAGE = (
    Path(__file__).resolve().parent / "adaptive_v1_proposer_harness"
)
PROPOSER_SYSTEM_PROMPT = (ADAPTIVE_H1_PACKAGE / "system.md").read_text()

OBJECTIVE = (
    "Maximize expected verifier-valid score at fixed inner rollout budget. "
    "A behavior-equivalent attempt has exactly zero causal reward even if an "
    "independently sampled score differs. Explore the complete native SAH "
    "h2spec/1.0 surface, including prompts, skills, tool descriptions, "
    "generated tools, generated middlewares, sampling, and agent controls. "
    "Use learning_reward and statistically_positive evidence; do not repeat "
    "archived no-op or harmful designs."
)

# These are preferences, not action-space restrictions.  The rotating hint
# keeps a small batch from collapsing into four prompt paraphrases while the
# proposer remains free to compose any valid native h2spec/1.0 fields.
_DIVERSITY_DOMAINS = (
    "system_prompt_or_solver_skills",
    "sampling_or_agent_controls",
    "middleware_or_tool_descriptions",
    "generated_capability_or_cross_field_composition",
)

# Public capability inventory used in prompts, artifacts, and tests.  Wildcards
# denote typed collections validated by outer.harness_spec, not arbitrary file
# writes.  Model/evaluator/budget/credentials remain external invariants.
MUTABLE_POINTERS = (
    "/system_prompt",
    "/skill_description",
    "/skill_body",
    "/tool_descriptions/*",
    "/sampling/temperature",
    "/sampling/top_p",
    "/sampling/top_k",
    "/sampling/max_tokens",
    "/agent/max_iterations",
    "/middleware/budget_reminder_from_left",
    "/middleware/long_tool_output_max_chars",
    "/new_tools/*",
    "/remove_tools/*",
    "/new_skills/*",
    "/new_middlewares/*",
)

def _json_clone(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def _canonical(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value).encode()).hexdigest()[:16]


def _clip_json(value: Any, limit: int) -> Any:
    rendered = json.dumps(value, ensure_ascii=False, default=str)
    if len(rendered) <= limit:
        return _json_clone(value)
    return {"truncated": True, "chars": len(rendered), "preview": rendered[:limit]}


def _rounded(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return round(float(value), 8)
    except (TypeError, ValueError):
        return None


def _clip_text(value: Any, limit: int) -> Optional[str]:
    if value in (None, ""):
        return None
    text = str(value)
    return text if len(text) <= limit else text[:limit] + "…"


def _estimate_text_tokens(text: str) -> int:
    """Conservative tokenizer-independent estimate for the context guard.

    The live Qwen tokenizer used 10,649 tokens for the failed 38,028-character
    appendix (~3.57 chars/token).  Counting ASCII at 3 chars/token and every
    non-ASCII codepoint as one token intentionally leaves additional margin.
    """
    ascii_chars = sum(ord(char) < 128 for char in text)
    non_ascii_chars = len(text) - ascii_chars
    return (ascii_chars + 2) // 3 + non_ascii_chars


def _finalize_context_budget(
    payload: Dict[str, Any],
    *,
    max_prompt_chars: int,
    max_prompt_tokens: int,
) -> str:
    """Reach a fixed point so context metadata describes final JSON bytes."""
    budget = payload["context_budget"]
    for _ in range(8):
        rendered = _canonical(payload)
        values = (len(rendered), _estimate_text_tokens(rendered))
        previous = (
            budget.get("rendered_chars"),
            budget.get("rendered_estimated_tokens"),
        )
        if previous == values:
            break
        budget["rendered_chars"] = values[0]
        budget["rendered_estimated_tokens"] = values[1]
    else:
        raise ValueError("Adaptive proposer context budget did not stabilize")
    rendered = _canonical(payload)
    if (
        len(rendered) > max_prompt_chars
        or _estimate_text_tokens(rendered) > max_prompt_tokens
    ):
        raise ValueError(
            "Adaptive context budget metadata exceeded the configured limit: "
            f"chars={len(rendered)}/{max_prompt_chars}, "
            f"estimated_tokens={_estimate_text_tokens(rendered)}/"
            f"{max_prompt_tokens}"
        )
    return rendered


def _compact_attempt(item: Mapping[str, Any]) -> Dict[str, Any]:
    """Keep decision evidence without replaying a full historical h2spec."""
    action = item.get("action")
    action = action if isinstance(action, Mapping) else {}
    reward_components = item.get("reward_components")
    reward_components = (
        reward_components if isinstance(reward_components, Mapping) else {}
    )
    telemetry = item.get("rollout_telemetry")
    telemetry = telemetry if isinstance(telemetry, Mapping) else {}
    return {
        "evidence_id": item.get("evidence_id"),
        "round": item.get("round_index"),
        "proposal_id": item.get("proposal_id"),
        "signature": item.get("signature"),
        "valid": bool(item.get("valid")),
        "changed_fields": list(action.get("changed_fields") or []),
        "hypothesis": _clip_text(action.get("hypothesis"), 240),
        "learning_reward": _rounded(item.get("learning_reward")),
        "outcome_score": _rounded(item.get("outcome_score")),
        "outcome_score_sem": _rounded(item.get("outcome_score_sem")),
        "relative_delta": _rounded(reward_components.get("relative_delta")),
        "statistically_positive": bool(item.get("statistically_positive")),
        "behavior_equivalent": bool(item.get("outcome_behavior_equivalent")),
        "rollout_telemetry": {
            "error_counts": dict(telemetry.get("error_counts") or {}),
            "invalid_steps": int(telemetry.get("invalid_steps", 0) or 0),
            "evaluated_steps": int(telemetry.get("evaluated_steps", 0) or 0),
            "edit_mode_counts": dict(telemetry.get("edit_mode_counts") or {}),
            "custom_tool_call_counts": dict(
                telemetry.get("custom_tool_call_counts") or {}
            ),
        },
        "failure_reason": _clip_text(item.get("failure_reason"), 240),
    }


def _compact_operator_statistics(
    statistics_by_operator: Mapping[str, Any],
    *,
    limit: int = 24,
) -> List[Dict[str, Any]]:
    """Render stable, compact operator summaries instead of verbose dicts."""
    rows: List[Dict[str, Any]] = []
    for name, raw in statistics_by_operator.items():
        stats = raw if isinstance(raw, Mapping) else {}
        rows.append(
            {
                "operator": str(name),
                "n": int(stats.get("count", 0) or 0),
                "mean_learning_reward": _rounded(
                    stats.get("mean_learning_reward")
                ),
                "valid": int(stats.get("valid_count", 0) or 0),
                "invalid": int(stats.get("invalid_count", 0) or 0),
                "positive": int(
                    stats.get("statistically_positive_count", 0) or 0
                ),
            }
        )
    rows.sort(
        key=lambda row: (
            -abs(float(row["mean_learning_reward"] or 0.0)),
            str(row["operator"]),
        )
    )
    return rows[:limit]


def _compact_action_reference(item: Any) -> Any:
    if not isinstance(item, Mapping):
        return _clip_text(item, 160)
    action = item.get("action")
    if isinstance(action, Mapping):
        return _compact_attempt(item)
    return {
        "proposal_id": item.get("proposal_id"),
        "signature": item.get("signature") or _digest(item),
        "changed_fields": list(item.get("changed_fields") or []),
        "hypothesis": _clip_text(item.get("hypothesis"), 200),
    }


def h1_package_hash() -> str:
    """Hash Adaptive H1 plus every shared SAH component it references."""
    hasher = hashlib.sha256()
    runtime = Path(__file__).resolve()
    source_root = runtime.parents[1]
    runtime_files = (
        runtime,
        source_root / "outer" / "harness_spec.py",
        source_root / "outer" / "materialize.py",
        source_root / "outer" / "propose.py",
        source_root / "outer" / "propose_session.py",
        source_root / "outer" / "proposer_io.py",
        source_root / "outer" / "static_gates.py",
        source_root / "outer" / "harness" / "tools" / "design.py",
        source_root / "outer" / "reviewer" / "reviewer.py",
    )
    for file_path in runtime_files:
        hasher.update(str(file_path.relative_to(source_root)).encode())
        hasher.update(file_path.read_bytes())
    roots = (
        ADAPTIVE_H1_PACKAGE,
        pio.H1_PACKAGE / "tools",
        pio.H1_PACKAGE / "skills" / "harness-design",
        pio.H1_PACKAGE / "middlewares",
    )
    for root in roots:
        for file_path in sorted(root.rglob("*")):
            if file_path.is_file() and "__pycache__" not in file_path.parts:
                hasher.update(str(file_path.relative_to(root)).encode())
                hasher.update(file_path.read_bytes())
    return "sha256:" + hasher.hexdigest()[:16]


@dataclass
class CandidateRecord:
    k: int
    valid: bool
    errors: List[str] = field(default_factory=list)
    raw_submission: str = ""
    partial_spec: Optional[Dict[str, Any]] = None
    effective: Optional[Dict[str, Any]] = None
    changed_fields: List[str] = field(default_factory=list)
    spec_hash: str = ""
    trajectory: List[Dict[str, Any]] = field(default_factory=list)
    llm_calls: int = 0
    stop_reason: str = ""
    review_log: List[Dict[str, Any]] = field(default_factory=list)
    action: Optional[Dict[str, Any]] = None
    user_message: str = ""
    training_response: str = ""
    training_response_reviewed: bool = False
    input_tokens: Optional[int] = None
    token_counter: Optional[str] = None
    intervention_family: str = ""


def _adaptive_tool_schema_errors(spec: Mapping[str, Any]) -> List[str]:
    """Validate generated-tool schemas without changing SAH's default gate."""
    errors: List[str] = []
    try:
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError
    except ImportError:
        return ["generated-tool validation requires jsonschema"]
    for index, tool in enumerate(spec.get("new_tools") or []):
        if not isinstance(tool, Mapping):
            continue
        label = f"new_tools[{index}].input_schema"
        schema = tool.get(
            "input_schema", {"type": "object", "properties": {}}
        )
        if not isinstance(schema, Mapping):
            errors.append(f"{label}: must be a JSON-schema mapping")
            continue
        if schema.get("type") != "object":
            errors.append(f"{label}: root type must be 'object'")
            continue
        try:
            Draft202012Validator.check_schema(dict(schema))
        except SchemaError as exc:
            message = str(exc.message or exc).replace("\n", " ")[:300]
            errors.append(f"{label}: invalid JSON Schema: {message}")
    return errors


def _adaptive_tool_capability_errors(
    spec: Mapping[str, Any],
) -> List[str]:
    """Enforce the public ``ToolContext`` boundary for Adaptive declarations."""
    errors: List[str] = []
    for index, tool in enumerate(spec.get("new_tools") or []):
        if not isinstance(tool, Mapping):
            continue
        code = tool.get("implementation_py")
        if not isinstance(code, str):
            continue
        label = f"new_tools[{index}].implementation_py"
        try:
            tree = ast.parse(code)
        except SyntaxError:
            # The shared generated-code reviewer reports syntax details.
            continue
        parents = {
            child: parent
            for parent in ast.walk(tree)
            for child in ast.iter_child_nodes(parent)
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == "ctx":
                parent = parents.get(node)
                direct_public_receiver = (
                    isinstance(node.ctx, ast.Load)
                    and isinstance(parent, ast.Attribute)
                    and parent.value is node
                    and parent.attr in _ADAPTIVE_CTX_CAPABILITIES
                )
                if not direct_public_receiver:
                    errors.append(
                        f"{label}: ctx may only be used as the direct receiver "
                        "of a documented capability"
                    )
            elif isinstance(node, ast.Attribute):
                if node.attr.startswith("_"):
                    errors.append(
                        f"{label}: private attribute access is forbidden: "
                        f".{node.attr}"
                    )
                elif (
                    isinstance(node.value, ast.Name)
                    and node.value.id == "ctx"
                    and node.attr not in _ADAPTIVE_CTX_CAPABILITIES
                ):
                    errors.append(
                        f"{label}: ctx.{node.attr} is outside the public "
                        "capability API"
                    )
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in _DYNAMIC_ATTRIBUTE_BUILTINS
            ):
                errors.append(
                    f"{label}: dynamic attribute builtin is forbidden: "
                    f"{node.func.id}"
                )
    return sorted(set(errors))


class AdaptiveProposeSession(ProposeSession):
    """SAH proposal session plus Adaptive-only generated-schema preflight."""

    def _check(self, spec_yaml: str):
        validation = hs.parse_and_validate(spec_yaml)
        if not validation.valid or validation.spec is None:
            return None, None, [], validation.errors
        spec = validation.spec
        effective = hs.merge_with_base(spec, self.base_spec)
        changed = _adaptive_changed_fields(effective, self.base_spec)
        if not changed:
            return spec, effective, [], [
                "spec is identical to the current harness (no-op)"
            ]
        generated_errors = [
            *_adaptive_tool_schema_errors(spec),
            *_adaptive_tool_capability_errors(spec),
        ]
        if generated_errors:
            return None, None, [], generated_errors
        return spec, effective, changed, []


def _adaptive_changed_fields(
    effective: Mapping[str, Any],
    base: Mapping[str, Any],
) -> List[str]:
    """Diff a ratcheted Adaptive package without charging inherited capabilities.

    SAH's historical helper treats every ``new_*`` entry as a mutation because
    its original contract assumed the base never carried generated
    capabilities. Modern packages deliberately ratchet generated tools,
    skills, and middleware across rounds. Adaptive therefore compares those
    collections against the actual base while leaving SAH's default diff
    semantics untouched.
    """
    _, shared_changed = hs.differs_from_base(dict(effective), dict(base))
    generated_roots = {
        "new_tools",
        "new_skills",
        "new_middlewares",
        "remove_tools",
    }
    changed = [
        item
        for item in shared_changed
        if item.split(".", 1)[0] not in generated_roots
    ]
    for root in ("new_tools", "new_skills", "new_middlewares"):
        effective_items = list(effective.get(root) or [])
        base_items = list(base.get(root) or [])
        if _canonical(effective_items) == _canonical(base_items):
            continue
        names = {
            str(item.get("name", "?"))
            for item in [*base_items, *effective_items]
            if isinstance(item, Mapping)
        }
        changed.extend(f"{root}.{name}" for name in sorted(names))
    if _canonical(list(effective.get("remove_tools") or [])) != _canonical(
        list(base.get("remove_tools") or [])
    ):
        changed.append("remove_tools")
    return changed


def _review_rejection_errors(
    review_log: Sequence[Mapping[str, Any]],
) -> List[str]:
    """Reject a candidate if any declared generated capability was dropped.

    Other edited fields may refer to that capability. Materializing the
    surviving subset would therefore create a structurally loadable but
    semantically inconsistent harness.
    """
    return [
        "generated capability failed review: "
        f"{item.get('name', 'unknown')}: "
        f"{item.get('error') or 'review rejected'}"
        for item in review_log
        if not item.get("ok")
    ]


def _reviewed_training_submission(
    partial_spec: Mapping[str, Any],
    effective_spec: Mapping[str, Any],
) -> str:
    """Render the submitted partial with reviewer-repaired tool code.

    The raw model submission remains in trace artifacts. Positive policy
    credit, however, must target the implementation that actually ran.
    """
    reviewed = _json_clone(partial_spec)
    effective_tools = {
        str(item.get("name")): item
        for item in effective_spec.get("new_tools") or []
        if isinstance(item, Mapping) and item.get("name")
    }
    if isinstance(reviewed.get("new_tools"), list):
        for tool in reviewed["new_tools"]:
            if not isinstance(tool, dict):
                continue
            replacement = effective_tools.get(str(tool.get("name")))
            if replacement is not None:
                tool["implementation_py"] = replacement["implementation_py"]
    return yaml.safe_dump(reviewed, sort_keys=False)


def _submitted_effective_capabilities(
    session: ProposeSession,
    field: str,
) -> List[Dict[str, Any]]:
    """Resolve only capabilities declared by this proposal into effective rows.

    Inherited generated code was already reviewed before its package was
    accepted. Re-reviewing it on every unrelated proposal can silently mutate
    the base capability and misattribute that mutation to a prompt/sampling
    intervention.
    """
    if (
        not session.submitted
        or not session.partial_spec
        or not session.effective
    ):
        return []
    declared = list(session.partial_spec.get(field) or [])
    effective_by_name = {
        str(item.get("name")): item
        for item in session.effective.get(field) or []
        if isinstance(item, dict) and item.get("name")
    }
    resolved: List[Dict[str, Any]] = []
    for item in declared:
        name = str(item.get("name")) if isinstance(item, Mapping) else ""
        if not name or name not in effective_by_name:
            raise ValueError(
                f"submitted {field} capability is missing from effective spec: "
                f"{name or '<unnamed>'}"
            )
        resolved.append(effective_by_name[name])
    return resolved


def default_state() -> Dict[str, Any]:
    return {
        "schema": STATE_SCHEMA,
        "protocol": PROTOCOL,
        "created": time.strftime("%Y%m%d-%H%M%S"),
        "tasks": {},
        "active_adapter": None,
        "pending_training": None,
        "committed_batches": [],
    }


def load_state(path: Optional[str | Path]) -> Dict[str, Any]:
    if not path or not Path(path).exists():
        return default_state()
    state = json.loads(Path(path).read_text())
    if state.get("schema") != STATE_SCHEMA:
        raise ValueError(f"unsupported Adaptive state schema: {state.get('schema')!r}")
    return state


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False))
    os.replace(tmp, path)


def resolve_state_path(round_dir: Path, configured: Optional[str]) -> Path:
    return (
        Path(configured)
        if configured
        else Path(round_dir).parent / "adaptive_v1_state.json"
    )


def _task_state(
    state: Mapping[str, Any],
    task_id: str,
    *,
    base_package: str,
    base_score: float,
    seed_score: Optional[float] = None,
) -> Dict[str, Any]:
    existing = dict((state.get("tasks") or {}).get(task_id) or {})
    working = dict(
        existing.get("working")
        or {"package": base_package, "score": base_score, "from": "initial"}
    )
    if seed_score is not None:
        working.setdefault("seed_score", float(seed_score))
    return {
        "working": working,
        "champion": dict(
            existing.get("champion")
            or {"package": base_package, "score": base_score, "from": "initial"}
        ),
        "archive": dict(
            existing.get("archive")
            or {
                "attempts": [],
                "successful_actions": [],
                "invalid_signatures": [],
                "operator_statistics": {},
            }
        ),
        "controller": dict(
            existing.get("controller")
            or {
                "rounds_seen": 0,
                "rounds_since_confirmed_record": 0,
                "confirmed_record": None,
                "pending_examples": [],
                "replay_examples": [],
                "policy_updates": 0,
                "last_training_decision": "not_started",
                "training_history": [],
            }
        ),
        "collected_rounds": list(existing.get("collected_rounds") or []),
    }


def _capability_contract() -> Dict[str, Any]:
    return {
        "protocol": PROTOCOL,
        "shared_runtime": (
            "SAH h2spec/1.0 validator/materializer + NexAU frozen H2; "
            "Adaptive uses a separate NexAU H1"
        ),
        "schema": "h2spec/1.0",
        "mutable_surface": list(MUTABLE_POINTERS),
        "generated_capabilities": {
            "new_tools": {
                "max_items": 3,
                "implementation": "Python def run(ctx, args), safety-gated",
            },
            "new_skills": {"max_items": 2, "format": "SKILL.md"},
            "new_middlewares": {
                "max_items": 2,
                "implementation": "safety-gated NexAU hook",
            },
            "remove_tools": ["probe_solution"],
        },
        "always_protected": [
            "model_identity",
            "model_endpoint",
            "evaluator",
            "evaluation_budget",
            "ledger",
            "credentials",
            "task_definition",
            "data_splits",
            "builtin_runtime_bindings",
        ],
        "note": (
            "All behaviorally meaningful fields supported by native SAH "
            "h2spec/1.0 are mutable. Infrastructure invariants stay fixed so "
            "candidate scores remain comparable."
        ),
    }


def _operator_statistics(
    attempts: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    buckets: Dict[str, List[Mapping[str, Any]]] = {}
    for attempt in attempts:
        action = attempt.get("action")
        if not isinstance(action, Mapping):
            continue
        keys = {f"axis:{action.get('axis', 'unknown')}"}
        for atom in action.get("edit_atoms", []) or []:
            if isinstance(atom, Mapping):
                keys.add(f"field:{atom.get('field', 'unknown')}")
        for key in keys:
            buckets.setdefault(key, []).append(attempt)
    output: Dict[str, Any] = {}
    for key, rows in buckets.items():
        raw = [float(row.get("reward", 0.0) or 0.0) for row in rows]
        learned = [float(row.get("learning_reward", 0.0) or 0.0) for row in rows]
        output[key] = {
            "count": len(rows),
            "raw_mean_reward": sum(raw) / len(raw),
            "raw_reward_std": statistics.pstdev(raw) if len(raw) > 1 else 0.0,
            "mean_learning_reward": sum(learned) / len(learned),
            "learning_reward_std": (
                statistics.pstdev(learned) if len(learned) > 1 else 0.0
            ),
            "valid_count": sum(bool(row.get("valid")) for row in rows),
            "invalid_count": sum(not bool(row.get("valid")) for row in rows),
            "statistically_positive_count": sum(
                bool(row.get("statistically_positive")) for row in rows
            ),
        }
    return output


def build_user_context(
    *,
    task_id: str,
    round_index: int,
    task_spec: str,
    seed_program: str,
    seed_score: float,
    base_score: float,
    max_evals: int,
    current_harness: Mapping[str, Any],
    task_state: Mapping[str, Any],
    max_prompt_chars: int = ADAPTIVE_CONTEXT_MAX_CHARS,
    max_prompt_tokens: int = ADAPTIVE_CONTEXT_MAX_ESTIMATED_TOKENS,
) -> tuple[str, Dict[str, Any]]:
    """Build a bounded evidence appendix for the standalone Adaptive H1.

    Adaptive reuses SAH's native user-message layout, which already contains
    the public task, seed program, and complete current harness. Repeating those
    values in the optimizer appendix caused it to grow by roughly 8K tokens
    after one round. Historical full specs remain in round artifacts/state,
    while H1 receives only compact decision evidence and content hashes.
    """
    archive = dict(task_state.get("archive") or {})
    attempts = list(archive.get("attempts") or [])
    evidence = [
        _compact_attempt(item)
        for item in attempts[-ADAPTIVE_CONTEXT_HISTORY_LIMIT:]
        if isinstance(item, Mapping)
    ]
    controller = dict(task_state.get("controller") or {})
    payload: Dict[str, Any] = {
        "schema": ADAPTIVE_CONTEXT_SCHEMA,
        "round": round_index,
        "references": {
            "task_id": task_id,
            "task_spec_hash": _digest(task_spec),
            "seed_program_hash": _digest(seed_program),
            "current_harness_hash": hs.spec_hash(dict(current_harness)),
            "note": (
                "Full task, seed, and current harness are already present in "
                "the native SAH user message."
            ),
        },
        "status": {
            "seed_score": seed_score,
            "working_score": base_score,
            "max_evaluator_calls": max_evals,
            "rounds_since_confirmed_record": controller.get(
                "rounds_since_confirmed_record", 0
            ),
            "confirmed_record": controller.get("confirmed_record"),
            "policy_updates": controller.get("policy_updates", 0),
            "last_training_decision": controller.get("last_training_decision"),
        },
        "evidence": evidence,
        "capability_contract": _capability_contract(),
        "optimizer_memory": {
            "operator_statistics": _compact_operator_statistics(
                archive.get("operator_statistics") or {}
            ),
            "successful_actions": [
                _compact_action_reference(item)
                for item in list(archive.get("successful_actions") or [])[-4:]
            ],
            "invalid_signatures": [
                _compact_action_reference(item)
                for item in list(archive.get("invalid_signatures") or [])[-8:]
            ],
        },
        "objective": OBJECTIVE,
        "context_budget": {
            "max_chars": max_prompt_chars,
            "max_estimated_tokens": max_prompt_tokens,
            "history_items": len(evidence),
            "full_historical_specs_included": False,
            "duplicate_task_seed_harness_included": False,
            "fallback_level": 0,
            "rendered_chars": 0,
            "rendered_estimated_tokens": 0,
        },
    }
    rendered = _canonical(payload)
    if (
        len(rendered) > max_prompt_chars
        or _estimate_text_tokens(rendered) > max_prompt_tokens
    ):
        payload["evidence"] = evidence[-4:]
        payload["optimizer_memory"]["operator_statistics"] = payload[
            "optimizer_memory"
        ]["operator_statistics"][:8]
        payload["optimizer_memory"]["successful_actions"] = payload[
            "optimizer_memory"
        ]["successful_actions"][-2:]
        payload["optimizer_memory"]["invalid_signatures"] = payload[
            "optimizer_memory"
        ]["invalid_signatures"][-4:]
        payload["context_budget"]["fallback_level"] = 1
        payload["context_budget"]["history_items"] = len(payload["evidence"])
        rendered = _canonical(payload)
    if (
        len(rendered) > max_prompt_chars
        or _estimate_text_tokens(rendered) > max_prompt_tokens
    ):
        payload["evidence"] = [
            {
                "proposal_id": item.get("proposal_id"),
                "signature": item.get("signature"),
                "valid": item.get("valid"),
                "changed_fields": list(item.get("changed_fields") or [])[:8],
                "learning_reward": item.get("learning_reward"),
                "outcome_score": item.get("outcome_score"),
                "failure_reason": _clip_text(item.get("failure_reason"), 120),
            }
            for item in payload["evidence"][-2:]
        ]
        payload["optimizer_memory"] = {
            "operator_statistics": payload["optimizer_memory"][
                "operator_statistics"
            ][:4],
            "successful_actions": [],
            "invalid_signatures": payload["optimizer_memory"][
                "invalid_signatures"
            ][-2:],
        }
        payload["context_budget"]["fallback_level"] = 2
        payload["context_budget"]["history_items"] = len(payload["evidence"])
        rendered = _canonical(payload)
    if (
        len(rendered) > max_prompt_chars
        or _estimate_text_tokens(rendered) > max_prompt_tokens
    ):
        # The minimum useful appendix is still structured and parseable.
        payload = {
            "schema": ADAPTIVE_CONTEXT_SCHEMA,
            "round": round_index,
            "references": payload["references"],
            "status": payload["status"],
            "evidence": payload["evidence"][-1:],
            "capability_contract": {
                "schema": "h2spec/1.0",
                "mutable_surface": list(MUTABLE_POINTERS),
                "always_protected": payload["capability_contract"][
                    "always_protected"
                ],
            },
            "objective": _clip_text(OBJECTIVE, 360),
            "context_budget": {
                "max_chars": max_prompt_chars,
                "max_estimated_tokens": max_prompt_tokens,
                "history_items": min(1, len(payload["evidence"])),
                "full_historical_specs_included": False,
                "duplicate_task_seed_harness_included": False,
                "fallback_level": 3,
                "rendered_chars": 0,
                "rendered_estimated_tokens": 0,
            },
        }
        rendered = _canonical(payload)
    estimated_tokens = _estimate_text_tokens(rendered)
    if len(rendered) > max_prompt_chars or estimated_tokens > max_prompt_tokens:
        raise ValueError(
            "Adaptive context budget is smaller than the minimum structured "
            f"appendix: chars={len(rendered)}/{max_prompt_chars}, "
            f"estimated_tokens={estimated_tokens}/{max_prompt_tokens}"
        )
    rendered = _finalize_context_budget(
        payload,
        max_prompt_chars=max_prompt_chars,
        max_prompt_tokens=max_prompt_tokens,
    )
    return rendered, payload


def _load_h1_training_tools() -> List[Dict[str, Any]]:
    tools: List[Dict[str, Any]] = []
    for name in ("validate_spec", "submit_spec"):
        document = yaml.safe_load(
            (pio.H1_PACKAGE / "tools" / f"{name}.tool.yaml").read_text()
        )
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": document["name"],
                    "description": document["description"],
                    "parameters": document["input_schema"],
                },
            }
        )
    return tools


H1_TRAINING_TOOLS = _load_h1_training_tools()


def _axis_for_changed(changed_fields: Sequence[str]) -> str:
    families = set()
    for field_name in changed_fields:
        root = str(field_name).split(".", 1)[0]
        if root in {"system_prompt"}:
            families.add("prompt")
        elif root in {"skill_description", "skill_body", "new_skills"}:
            families.add("skills")
        elif root in {"tool_descriptions", "new_tools", "remove_tools"}:
            families.add("tools")
        elif root in {"middleware", "new_middlewares"}:
            families.add("middlewares")
        elif root in {"sampling", "agent"}:
            families.add("agent")
        else:
            families.add("harness")
    return next(iter(families)) if len(families) == 1 else "mixed"


def _intervention_family(changed_fields: Sequence[str]) -> str:
    """Normalize field names so paraphrases share a batch-level family."""
    roots = sorted(
        {
            str(field_name).split(".", 1)[0]
            for field_name in changed_fields
            if str(field_name)
        }
    )
    return "+".join(roots) if roots else "invalid"


def _assistant_hypothesis(
    trajectory: Sequence[Mapping[str, Any]], changed_fields: Sequence[str]
) -> str:
    for message in trajectory:
        if str(message.get("role", "")).lower().endswith("assistant"):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                clean = re.sub(r"\s+", " ", content).strip()
                if clean:
                    return clean[:1200]
    fields = ", ".join(changed_fields) or "an invalid native spec"
    return f"Test a native SAH h2spec/1.0 intervention over {fields}."


def _cited_evidence(
    trajectory: Sequence[Mapping[str, Any]],
    raw_submission: str,
    known_evidence_ids: Iterable[str],
) -> List[str]:
    haystack = json.dumps(list(trajectory), ensure_ascii=False, default=str)
    haystack += "\n" + raw_submission
    return sorted(evidence_id for evidence_id in known_evidence_ids if evidence_id in haystack)


def _training_tool_call(raw_submission: str, trajectory: Sequence[Mapping[str, Any]]) -> str:
    """Render the final submit action in Qwen3 XML tool-call format.

    The shared SAH replay/training stack tokenizes this response with the
    native H1 tool schemas, matching vLLM's ``qwen3_xml`` parser.
    """
    if raw_submission.strip():
        return (
            "<tool_call>\n"
            "<function=submit_spec>\n"
            "<parameter=spec_yaml>\n"
            f"{raw_submission.strip()}\n"
            "</parameter>\n"
            "</function>\n"
            "</tool_call>"
        )
    for message in reversed(trajectory):
        if str(message.get("role", "")).lower().endswith("assistant"):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()
    return "<tool_call>\n<function=submit_spec>\n</function>\n</tool_call>"


def _semantic_action(
    *,
    proposal_id: str,
    native: sah_propose.CandidateRecord,
    known_evidence_ids: Iterable[str],
) -> Dict[str, Any]:
    changed = list(native.changed_fields or [])
    partial = _json_clone(native.spec) if isinstance(native.spec, Mapping) else None
    return {
        "proposal_id": proposal_id,
        "axis": _axis_for_changed(changed),
        "hypothesis": _assistant_hypothesis(native.trajectory, changed),
        "expected_effect": (
            "Improve verifier-valid outcome score under the unchanged evaluator "
            "and rollout budget."
        ),
        "evidence_ids": _cited_evidence(
            native.trajectory, native.raw_submission, known_evidence_ids
        ),
        "edit_atoms": [
            {"kind": "h2spec_patch", "field": field_name}
            for field_name in changed
        ],
        "changed_fields": changed,
        "native_partial_spec": partial,
        "preserve": [
            "model identity",
            "evaluator",
            "evaluation budget",
            "runtime ledger",
        ],
        "metadata": {
            "schema": "h2spec/1.0",
            "spec_hash": native.spec_hash,
            "submission_valid": bool(native.valid),
        },
    }


NativeRunner = Callable[..., sah_propose.CandidateRecord]


def run_adaptive_once(
    k: int,
    *,
    base_spec: Dict[str, Any],
    user_message: str,
    base_url: str,
    model: str,
    api_key: str,
    seed: Optional[int],
    timeout: float,
) -> sah_propose.CandidateRecord:
    """Run the separate Adaptive NexAU H1 over the shared SAH h2spec surface."""
    from nexau import Agent, AgentConfig
    from outer.reviewer.reviewer import review_tool_code

    config = AgentConfig.from_yaml(ADAPTIVE_H1_PACKAGE / "agent.yaml")
    llm = config.llm_config
    llm.model = model
    llm.base_url = base_url
    llm.api_key = api_key
    llm.timeout = timeout
    extra = getattr(llm, "extra_params", None)
    if not isinstance(extra, dict):
        extra = {}
        llm.extra_params = extra
    body = extra.setdefault("extra_body", {})
    body.setdefault("chat_template_kwargs", {})["enable_thinking"] = False
    if seed is not None:
        body["seed"] = seed

    session = AdaptiveProposeSession(base_spec=base_spec)
    trajectory: List[Dict[str, Any]] = []
    err: Optional[str] = None
    agent = None
    with propose_scope(session):
        try:
            agent = Agent(config=config)
            agent.run(message=user_message)
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
        finally:
            if agent is not None:
                trajectory = sah_propose._dump_history(agent)

    review_log: List[Dict[str, Any]] = []
    submitted_tools = _submitted_effective_capabilities(session, "new_tools")
    if submitted_tools:
        repair_fn = sah_propose._make_repair_fn(
            base_url, model, api_key, timeout
        )
        for tool in submitted_tools:
            try:
                outcome = review_tool_code(
                    tool["implementation_py"], repair_fn=repair_fn, max_rounds=2
                )
            except Exception as exc:
                review_log.append(
                    {
                        "name": tool["name"],
                        "ok": False,
                        "rounds": 0,
                        "error": f"reviewer crashed: {exc}",
                        "history": [],
                    }
                )
                continue
            reviewed_capability_errors = _adaptive_tool_capability_errors(
                {
                    "new_tools": [
                        {**tool, "implementation_py": outcome.code}
                    ]
                }
            )
            review_log.append(
                {
                    "name": tool["name"],
                    "ok": outcome.ok and not reviewed_capability_errors,
                    "rounds": outcome.rounds,
                    "error": outcome.final_error
                    or "; ".join(reviewed_capability_errors)
                    or None,
                    "history": outcome.history,
                }
            )
            if review_log[-1]["ok"]:
                tool["implementation_py"] = outcome.code

    submitted_middlewares = _submitted_effective_capabilities(
        session, "new_middlewares"
    )
    if submitted_middlewares:
        from outer.static_gates import check_middleware_code

        for middleware in submitted_middlewares:
            ok, errors = check_middleware_code(
                middleware["implementation_py"], middleware["hook"]
            )
            review_log.append(
                {
                    "name": "mw:" + middleware["name"],
                    "ok": ok,
                    "rounds": 0,
                    "error": None if ok else "; ".join(errors),
                    "history": [],
                }
            )

    review_errors = _review_rejection_errors(review_log)
    record = sah_propose.CandidateRecord(
        k=k,
        valid=bool(
            session.submitted
            and session.effective is not None
            and session.changed_fields
            and not review_errors
        ),
        raw_submission=session.raw_submission,
        spec=session.partial_spec,
        effective=session.effective,
        changed_fields=session.changed_fields,
        spec_hash=hs.spec_hash(session.effective) if session.effective else "",
        trajectory=trajectory,
        llm_calls=sum(
            1
            for message in trajectory
            if str(message.get("role", "")).lower().endswith("assistant")
        ),
        stop_reason=(
            "harness_error"
            if err
            else "review_rejected"
            if review_errors
            else ("submitted" if session.submitted else "no_submission")
        ),
    )
    record.review_log = review_log
    if err:
        record.errors = [err]
    elif review_errors:
        record.errors = review_errors
    elif not session.submitted:
        record.errors = ["proposer never called submit_spec"]
    elif session.errors:
        record.errors = session.errors
    record.training_submission = session.raw_submission
    record.training_submission_reviewed = record.valid and any(
        item.get("ok") and int(item.get("rounds", 0) or 0) > 0
        for item in review_log
    )
    if (
        record.valid
        and record.training_submission_reviewed
        and session.partial_spec is not None
        and session.effective is not None
    ):
        record.training_submission = _reviewed_training_submission(
            session.partial_spec,
            session.effective,
        )
    return record


def propose_group(
    *,
    count: int,
    round_index: int,
    base_seed: int,
    base_spec: Mapping[str, Any],
    base_user_context: str,
    known_evidence_ids: Iterable[str],
    base_url: str,
    model: str,
    api_key: str = "EMPTY",
    timeout: float = 600.0,
    force_tool_frac: float = 0.0,
    tokenizer_path: Optional[str] = None,
    historical_spec_hashes: Iterable[str] = (),
    run_candidate: Optional[NativeRunner] = None,
) -> List[CandidateRecord]:
    """Sequentially sample standalone Adaptive H1 candidates with memory."""
    runner = run_candidate or run_adaptive_once
    records: List[CandidateRecord] = []
    seen_hashes = {
        hs.spec_hash(dict(base_spec)),
        *(str(item) for item in historical_spec_hashes if item),
    }
    seen_families: set[str] = set()
    force_count = min(
        count,
        max(0, math.ceil(count * max(0.0, force_tool_frac))),
    )

    for sample_index in range(count):
        proposal_id = f"hopt-r{round_index:03d}-s{sample_index:02d}"
        diversity = {
            "batch_sample": sample_index + 1,
            "batch_size": count,
            "prior_valid_actions": [
                {
                    "proposal_id": f"hopt-r{round_index:03d}-s{item.k:02d}",
                    "axis": (item.action or {}).get("axis"),
                    "intervention_family": item.intervention_family,
                    "changed_fields": item.changed_fields,
                    "spec_hash": item.spec_hash,
                }
                for item in records
                if item.valid
            ],
            "requirement": (
                "Submit a causally distinct native h2spec/1.0 intervention. "
                "A candidate with the same normalized intervention_family as "
                "an earlier valid candidate is rejected; use a different part "
                "of the complete action surface, not a paraphrase."
            ),
            "preferred_distinct_domain": (
                "generated_tool_capability"
                if sample_index < force_count
                else _DIVERSITY_DOMAINS[
                    (sample_index - force_count) % len(_DIVERSITY_DOMAINS)
                ]
            ),
            "domain_is_guidance_not_restriction": True,
        }
        if sample_index < force_count:
            diversity["required_capability"] = (
                "This candidate must include at least one useful new_tools entry "
                "with safety-gated implementation_py."
            )
        user_message = (
            base_user_context
            + "\n\n## Adaptive batch diversity constraint\n```json\n"
            + json.dumps(diversity, ensure_ascii=False, default=str)
            + "\n```"
        )
        seed = base_seed + round_index * 1000 + sample_index
        input_tokens, token_counter = count_chat_tokens(
            system=PROPOSER_SYSTEM_PROMPT,
            user=user_message,
            tools=H1_TRAINING_TOOLS,
            tokenizer_path=tokenizer_path,
        )
        input_tokens += PROPOSER_PROMPT_INJECTION_MARGIN
        if input_tokens > PROPOSER_MAX_INPUT_TOKENS:
            records.append(
                CandidateRecord(
                    k=sample_index,
                    valid=False,
                    errors=[
                        "Adaptive proposer input exceeds hard token budget: "
                        f"{input_tokens}>{PROPOSER_MAX_INPUT_TOKENS}"
                    ],
                    stop_reason="context_preflight_rejected",
                    user_message=user_message,
                    input_tokens=input_tokens,
                    token_counter=token_counter,
                )
            )
            continue
        try:
            native = runner(
                sample_index,
                base_spec=dict(base_spec),
                user_message=user_message,
                base_url=base_url,
                model=model,
                api_key=api_key,
                seed=seed,
                timeout=timeout,
            )
        except Exception as exc:
            records.append(
                CandidateRecord(
                    k=sample_index,
                    valid=False,
                    errors=[f"{type(exc).__name__}: {exc}"],
                    stop_reason="model_error",
                    user_message=user_message,
                    input_tokens=input_tokens,
                    token_counter=token_counter,
                )
            )
            continue

        action = _semantic_action(
            proposal_id=proposal_id,
            native=native,
            known_evidence_ids=known_evidence_ids,
        )
        valid = bool(native.valid)
        errors = list(native.errors)
        candidate_hash = native.spec_hash
        family = _intervention_family(native.changed_fields)
        rejection_reason = ""
        if (
            valid
            and sample_index < force_count
            and not (native.spec or {}).get("new_tools")
        ):
            valid = False
            rejection_reason = "constraint_rejected"
            errors = [
                "required generated-tool capability was not present after "
                "validation/review"
            ]
        elif valid and candidate_hash in seen_hashes:
            valid = False
            rejection_reason = "duplicate"
            errors = ["duplicate of another candidate (or of the base)"]
        elif valid and family in seen_families:
            valid = False
            rejection_reason = "duplicate"
            errors = [
                "semantic duplicate of an earlier batch intervention family: "
                f"{family}"
            ]
        elif valid:
            seen_hashes.add(candidate_hash)
            seen_families.add(family)

        training_submission = str(
            getattr(native, "training_submission", native.raw_submission)
        )
        training_submission_reviewed = bool(
            getattr(native, "training_submission_reviewed", False)
        )
        record = CandidateRecord(
            k=sample_index,
            valid=valid,
            errors=errors,
            raw_submission=native.raw_submission,
            partial_spec=_json_clone(native.spec) if native.spec else None,
            effective=_json_clone(native.effective) if native.effective else None,
            changed_fields=list(native.changed_fields),
            spec_hash=candidate_hash,
            trajectory=list(native.trajectory),
            llm_calls=int(native.llm_calls),
            stop_reason=(
                native.stop_reason
                if valid or native.stop_reason != "submitted"
                else rejection_reason or "validation_rejected"
            ),
            review_log=list(native.review_log),
            action=action,
            user_message=user_message,
            training_response=_training_tool_call(
                training_submission, native.trajectory
            ),
            training_response_reviewed=training_submission_reviewed,
            input_tokens=input_tokens,
            token_counter=token_counter,
            intervention_family=family,
        )
        records.append(record)
    return records


def cmd_propose(
    args, *, load_bases: Callable[..., Dict[str, Dict[str, Any]]]
) -> None:
    """Adaptive implementation of ``outer.outer_round propose``."""
    from inner import eft_task

    adaptive_dataset_root = os.environ.get("ADAPTIVE_V1_DATASET_ROOT")
    if adaptive_dataset_root:
        eft_task.configure_dataset_root(adaptive_dataset_root)

    if int(args.max_evals) != 30:
        raise ValueError(
            "Adaptive V1 requires max_evals=30 for matched comparable runs"
        )
    round_dir = Path(args.round_dir)
    round_dir.mkdir(parents=True, exist_ok=True)
    bases = load_bases(args.bases_file, args.tasks)
    state_path = resolve_state_path(round_dir, getattr(args, "protocol_state", None))
    state = load_state(state_path)
    base_urls = (
        [f"http://127.0.0.1:{8800 + g}/v1" for g in range(args.n_replicas)]
        if args.n_replicas > 0
        else [args.base_url]
    )
    tokenizer_path = (
        getattr(args, "adaptive_tokenizer_path", None)
        or os.environ.get("ADAPTIVE_TOKENIZER_PATH")
        or None
    )

    inherited: Dict[str, Any] = {}
    if getattr(args, "seed_programs_file", None):
        try:
            inherited = json.loads(Path(args.seed_programs_file).read_text())
        except Exception as exc:
            print(f"[adaptive_v1:propose] WARNING seed programs unreadable: {exc}")

    per_task: Dict[str, Any] = {}
    prompts: Dict[str, str] = {}
    trajectories: List[Dict[str, Any]] = []
    total_valid = 0
    seed0 = int(args.seed if args.seed is not None else 0)
    protocol_round = (
        int(args.protocol_round)
        if getattr(args, "protocol_round", None) is not None
        else int(args.round)
    )

    for task_index, tid in enumerate(args.tasks):
        task = eft_task.get_task(tid)
        base_package = str(bases[tid]["package"])
        base_score = float(bases[tid]["score"])
        task_state = _task_state(
            state,
            tid,
            base_package=base_package,
            base_score=base_score,
            seed_score=float(bases[tid]["seed_score"]),
        )
        base_spec = hs.read_base_spec(Path(base_package))
        entry = inherited.get(tid)
        if entry:
            seed_program = entry["program"] if isinstance(entry, Mapping) else entry
            seed_score = (
                float(entry.get("score", bases[tid]["seed_score"]))
                if isinstance(entry, Mapping)
                else float(bases[tid]["seed_score"])
            )
        else:
            seed_program = task.initial_program
            seed_score = float(bases[tid]["seed_score"])

        _, payload = build_user_context(
            task_id=tid,
            round_index=protocol_round,
            task_spec=task.spec,
            seed_program=seed_program,
            seed_score=seed_score,
            base_score=base_score,
            max_evals=args.max_evals,
            current_harness=base_spec,
            task_state=task_state,
        )
        native_context = pio.build_user_message(
            task_id=tid,
            task_spec=task.spec,
            seed_program=seed_program,
            seed_score=seed_score,
            base_score=base_score,
            base_spec=base_spec,
            max_evals=args.max_evals,
        )
        dossier_text, dossier_payload = build_analysis_dossier(
            task_id=tid,
            round_index=protocol_round,
            task_spec=task.spec,
            seed_program=seed_program,
            seed_score=seed_score,
            base_score=base_score,
            max_evals=args.max_evals,
            current_harness=base_spec,
            adaptive_payload=payload,
        )
        analysis = run_context_analysis(
            dossier_text=dossier_text,
            dossier_payload=dossier_payload,
            base_url=base_urls[task_index % len(base_urls)],
            model=args.model,
            api_key="EMPTY",
            timeout=600.0,
            seed=seed0 + protocol_round * 1000 + 900,
            tokenizer_path=tokenizer_path,
        )
        write_analysis_artifacts(
            round_dir / "analysis" / tid,
            dossier_payload=dossier_payload,
            result=analysis,
        )
        native_context += (
            "\n\n## Adaptive V1 analyst brief\n"
            "This bounded JSON was produced by the read-only performance and "
            "design analyzer team. Treat it as evidence, preserve uncertainty, "
            "and retain final design judgment.\n```json\n"
            + json.dumps(analysis.brief, ensure_ascii=False, separators=(",", ":"))
            + "\n```"
        )
        prompts[tid] = native_context
        records = propose_group(
            count=args.k,
            round_index=protocol_round,
            base_seed=seed0,
            base_spec=base_spec,
            base_user_context=native_context,
            known_evidence_ids=[
                str(item["evidence_id"])
                for item in payload.get("evidence", [])
                if item.get("evidence_id")
            ],
            historical_spec_hashes=[
                str(
                    ((item.get("action") or {}).get("metadata") or {}).get(
                        "spec_hash"
                    )
                    or item.get("signature")
                    or ""
                )
                for item in (task_state.get("archive") or {}).get(
                    "attempts", []
                )
                if isinstance(item, Mapping)
            ],
            base_url=base_urls[task_index % len(base_urls)],
            model=args.model,
            api_key="EMPTY",
            timeout=600.0,
            force_tool_frac=float(getattr(args, "force_tool_frac", 0.0) or 0.0),
            tokenizer_path=tokenizer_path,
        )

        candidates = []
        for record in records:
            proposal_id = f"hopt-r{protocol_round:03d}-s{record.k:02d}"
            candidate = {
                "k": record.k,
                "proposal_id": proposal_id,
                "valid": record.valid,
                "errors": record.errors,
                "spec_hash": record.spec_hash,
                "changed_fields": record.changed_fields,
                "intervention_family": record.intervention_family,
                "stop_reason": record.stop_reason,
                "llm_calls": record.llm_calls,
                "input_tokens": record.input_tokens,
                "token_counter": record.token_counter,
                "review_log": record.review_log,
                "action": record.action,
            }
            if record.valid and record.effective is not None:
                candidate_dir = round_dir / "tasks" / tid / f"cand{record.k:02d}"
                materialize(
                    record.effective,
                    candidate_dir,
                    raw_spec_text=record.raw_submission,
                    meta={
                        "protocol": PROTOCOL,
                        "round": args.round,
                        "protocol_round": protocol_round,
                        "task_id": tid,
                        "k": record.k,
                        "proposal_id": proposal_id,
                        "spec_hash": record.spec_hash,
                        "changed_fields": record.changed_fields,
                        "base_package": base_package,
                        "native_partial_spec": record.partial_spec,
                        "adaptive_action": record.action,
                        "effective": record.effective,
                    },
                )
                candidate["dir"] = str(candidate_dir)
                total_valid += 1
            candidates.append(candidate)
            trajectories.append(
                {
                    "task_id": tid,
                    "k": record.k,
                    "system": PROPOSER_SYSTEM_PROMPT,
                    "user": record.user_message,
                    "raw_submission": record.raw_submission,
                    "training_response": record.training_response,
                    "training_response_reviewed": (
                        record.training_response_reviewed
                    ),
                    "training_tools": H1_TRAINING_TOOLS,
                    "trajectory": record.trajectory,
                    "input_tokens": record.input_tokens,
                    "token_counter": record.token_counter,
                }
            )

        champion = task_state["champion"]
        per_task[tid] = {
            "base_package": base_package,
            "base_score": base_score,
            "seed_score": bases[tid]["seed_score"],
            "base_spec_hash": hs.spec_hash(base_spec),
            "champion_package": champion["package"],
            "champion_score": champion["score"],
            "adaptive_context_budget": payload["context_budget"],
            "analysis": {
                "valid": analysis.valid,
                "source": analysis.source,
                "errors": analysis.errors,
                "dossier_budget": analysis.dossier_budget,
                "artifacts": str(round_dir / "analysis" / tid),
            },
            "candidates": candidates,
        }
        print(
            f"  {tid}: {sum(item['valid'] for item in candidates)}/"
            f"{len(candidates)} valid (Adaptive NexAU -> native h2spec/1.0; "
            f"analysis={analysis.source})"
        )

    h1_document = yaml.safe_load(
        (ADAPTIVE_H1_PACKAGE / "agent.yaml").read_text()
    ) or {}
    from protocols.adaptive_v1_controller import (
        CONTROLLER_VERSION,
        controller_package_hash,
    )
    from protocols.adaptive_v1_provenance import (
        RUNTIME_VERSION,
        runtime_package_hash,
    )

    h1_sampling = dict(h1_document.get("llm_config") or {})
    metadata = {
        "round": args.round,
        "protocol_round": protocol_round,
        "created": time.strftime("%Y%m%d-%H%M%S"),
        "mode": "instance_wise",
        "protocol": PROTOCOL,
        "protocol_state": str(state_path),
        "h1_version": H1_VERSION,
        "h1_package_hash": h1_package_hash(),
        "analysis_version": ANALYSIS_VERSION,
        "analysis_package_hash": analysis_package_hash(),
        "controller_version": CONTROLLER_VERSION,
        "controller_package_hash": controller_package_hash(),
        "runtime_version": RUNTIME_VERSION,
        "runtime_package_hash": runtime_package_hash(),
        "action_surface": "native_sah_h2spec/1.0_full",
        "proposer_topology": {
            "analysis_agents_per_task": 3,
            "analysis_coordinator": "adaptive_v1_context_coordinator",
            "analysis_subagents": [
                "performance_analyzer",
                "design_analyzer",
            ],
            "proposer_agents_per_task": args.k,
            "proposer": "standalone Adaptive V1 NexAU H1",
            "runtime": "nexau.AgentConfig.from_yaml",
            "package": "src/protocols/adaptive_v1_proposer_harness",
            "samples": args.k,
            "sampling": "sequential_with_bounded_analysis_brief",
            "analyzer": (
                "Adaptive NexAU coordinator with performance/design subagents; "
                "deterministic fail-closed fallback"
            ),
            "builder": "SAH ProposeSession merge_with_base",
            "validator": "SAH validate_spec fail-closed",
            "reviewer": "SAH static gates + same-model generated-tool repair",
        },
        "proposer": {
            "base_urls": base_urls,
            "model": args.model,
            "seed": args.seed,
            "temperature": h1_sampling.get("temperature"),
            "top_p": h1_sampling.get("top_p"),
            "max_tokens": h1_sampling.get("max_tokens"),
            "tokenizer_path": tokenizer_path,
            "hard_max_input_tokens": PROPOSER_MAX_INPUT_TOKENS,
        },
        "tasks_order": args.tasks,
        "max_evals": args.max_evals,
        "k": args.k,
        "total_rounds": getattr(args, "total_rounds", None),
        "force_tool_frac": float(
            getattr(args, "force_tool_frac", 0.0) or 0.0
        ),
        "bases_in": bases,
        "per_task": per_task,
    }
    (round_dir / "round.json").write_text(json.dumps(metadata, indent=2))
    (round_dir / "prompts.json").write_text(json.dumps(prompts, indent=2))
    (round_dir / "trajectories.json").write_text(
        json.dumps(trajectories, indent=2)
    )
    print(
        f"[adaptive_v1:propose] {total_valid}/{len(args.tasks) * args.k} valid "
        f"native candidates -> {round_dir}"
    )
