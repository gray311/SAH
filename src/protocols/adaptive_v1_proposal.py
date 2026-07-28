"""Adaptive v1 proposal adapter for SAH.

This half of the protocol owns:

* one outer LLM proposer, sampled sequentially K times;
* deterministic context/analyzer, action compiler, validation, and dedup;
* SAH's existing H2 package materializer and Adaptive-only package overlay.

It intentionally does not introduce Analyzer/Builder/Reviewer LLM agents.
Those names belonged to an earlier Codex pipeline.  The v1 reviewer was
explicitly disabled; compilation and validation here are deterministic.
Reward/frontier/update control lives in ``adaptive_v1_controller``.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import statistics
import time
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence

import yaml

from outer import harness_spec as hs
from outer.materialize import materialize

PROTOCOL = "adaptive_v1"
STATE_SCHEMA = "sah.adaptive-v1-state/1"
ACTION_AXES = {"prompt", "search", "inference", "context", "profiles"}
ACTION_FIELDS = {
    "proposal_id",
    "axis",
    "hypothesis",
    "edit_atoms",
    "expected_effect",
    "evidence_ids",
    "preserve",
    "metadata",
}
ATOM_KINDS = {
    "set",
    "prompt_upsert_section",
    "prompt_delete_section",
    "profile_add",
    "profile_remove",
    "profile_swap",
}
ATOM_FIELDS = {"kind", "field", "value"}
PROMPT_SECTION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
EPS = 1e-12

# Frozen verbatim from ModelHarnessActionPolicy.SYSTEM_PROMPT in Adaptive v1.
PROPOSER_SYSTEM_PROMPT = """\
You are the proposal policy inside HarnessOpt. Produce exactly one sparse,
evidence-grounded intervention on the mutable agent harness.

One response maps to one executable candidate and one reward. Do not combine
unrelated experiments. Prefer one edit atom; use at most two when a cross-field
invariant requires it. Never modify the model, evaluator, tasks, tools,
credentials, budgets, or protected implementation.

Treat optimizer_memory.recent_attempts as tested interventions, including
zero-credit and negative results. Do not retry the same target and causal
mechanism by changing wording, thresholds, or examples. Move to a different
field, axis, or genuinely different mechanism when an archived direction lacks
statistically positive reward.

In optimizer_memory.operator_statistics, raw_mean_reward describes observed
score direction while mean_learning_reward is confidence-adjusted credit.
Never treat a positive raw mean with zero confidence-adjusted credit as a
proven improvement.

Allowed edit atoms:
- {"kind":"set","field":"<exact mutable_set_fields JSON Pointer or declared logical alias>","value":<typed value>}
- {"kind":"prompt_upsert_section","field":"<stable-section-id>","value":"<instructions>"}
- {"kind":"prompt_delete_section","field":"<stable-section-id>"}
- {"kind":"profile_add","value":"<registered profile id>"}
- {"kind":"profile_remove","value":"<registered profile id>"}
- {"kind":"profile_swap","field":"<old id>","value":"<new id>"}

For a managed prompt section, field is a short stable section ID and value is
only the new instruction delta (at most 4000 characters). Never copy or restate
the full current prompt inside a managed section.

For evidence_ids, copy IDs only from known_evidence_ids (equivalently,
evidence[*].evidence_id). Never cite state_id, checkpoint IDs, component
digests, or any other identifier. Use an empty list when no listed evidence
supports the action.

Return only one JSON object:
{
  "axis": "prompt|search|inference|context|profiles",
  "hypothesis": "causal, falsifiable explanation",
  "expected_effect": "measurable expected outcome",
  "evidence_ids": ["only IDs present in the context"],
  "edit_atoms": [{"kind":"...", "field":"...", "value":"..."}],
  "preserve": ["important successful behavior to retain"]
}
"""

OBJECTIVE = (
    "Maximize expected verifier-valid score at fixed inner rollout budget. "
    "A behavior-equivalent attempt has exactly zero causal reward even if "
    "an independently sampled score differs; do not repeat such no-op edits. "
    "Use learning_reward and statistically_positive in optimizer memory; "
    "raw reward inside its paired uncertainty margin is not success evidence. "
    "Treat iteration-limit termination as neutral unless the trace shows "
    "waste, repeated invalid candidates, or loss of the saved best."
)

ALIASES = {
    "system_prompt": "/system_prompt",
    "max_context_tokens": "/max_context_tokens",
    "max_iterations": "/max_iterations",
    "tool_call_mode": "/tool_call_mode",
    "temperature": "/llm/temperature",
    "max_tokens": "/llm/max_tokens",
    "compaction.threshold": "/context_compaction/threshold",
    "compaction.max_context_tokens": "/context_compaction/max_context_tokens",
    "compaction.keep_iterations": "/context_compaction/keep_iterations",
    "compaction.compaction_strategy": "/context_compaction/compaction_strategy",
    "skills": "/skills",
}

MUTABLE_POINTERS = (
    "/system_prompt",
    "/max_context_tokens",
    "/max_iterations",
    "/tool_call_mode",
    "/llm/temperature",
    "/llm/max_tokens",
    "/context_compaction/max_context_tokens",
    "/context_compaction/threshold",
    "/context_compaction/keep_iterations",
    "/context_compaction/compaction_strategy",
)


def _json_clone(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value).encode()).hexdigest()[:16]


def _extract_json_object(text: str) -> Mapping[str, Any]:
    decoder = json.JSONDecoder()
    source = str(text or "").strip()
    for index, character in enumerate(source):
        if character != "{":
            continue
        try:
            value, _ = decoder.raw_decode(source[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, Mapping):
            return value
    raise ValueError("model response contains no JSON object")


def _clip_json(value: Any, limit: int) -> Any:
    rendered = json.dumps(value, ensure_ascii=False, default=str)
    if len(rendered) <= limit:
        return _json_clone(value)
    return {"truncated": True, "chars": len(rendered), "preview": rendered[:limit]}


@dataclass(frozen=True)
class EditAtom:
    kind: str
    field: str = ""
    value: Any = None

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "EditAtom":
        kind = str(value.get("kind") or "")
        if kind not in ATOM_KINDS:
            raise ValueError(f"unsupported edit atom kind: {kind!r}")
        field_name = str(value.get("field") or "")
        if kind in {"set", "prompt_upsert_section", "prompt_delete_section"} and not field_name:
            raise ValueError(f"edit atom {kind!r} requires field")
        if kind in {"profile_add", "profile_remove"} and not isinstance(value.get("value"), str):
            raise ValueError(f"edit atom {kind!r} requires string value")
        if kind == "profile_swap" and (
            not field_name or not isinstance(value.get("value"), str)
        ):
            raise ValueError("profile_swap requires old profile in field and new profile in value")
        return cls(kind=kind, field=field_name, value=value.get("value"))

    def to_dict(self) -> Dict[str, Any]:
        return {"kind": self.kind, "field": self.field, "value": self.value}


@dataclass(frozen=True)
class HarnessAction:
    proposal_id: str
    axis: str
    hypothesis: str
    edit_atoms: tuple[EditAtom, ...]
    expected_effect: str = ""
    evidence_ids: tuple[str, ...] = ()
    preserve: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "HarnessAction":
        proposal_id = str(value.get("proposal_id") or "")
        axis = str(value.get("axis") or "")
        hypothesis = str(value.get("hypothesis") or "")
        if not proposal_id or not hypothesis or axis not in ACTION_AXES:
            raise ValueError("action requires proposal_id, hypothesis, and a supported axis")
        raw_atoms = value.get("edit_atoms")
        if not isinstance(raw_atoms, list) or not raw_atoms:
            raise ValueError("action requires a non-empty edit_atoms list")
        if len(raw_atoms) > 4:
            raise ValueError("action may contain at most four edit atoms")
        if not all(isinstance(item, Mapping) for item in raw_atoms):
            raise ValueError("all edit_atoms must be mappings")
        evidence = value.get("evidence_ids", [])
        preserve = value.get("preserve", [])
        if not isinstance(evidence, list) or not all(isinstance(x, str) for x in evidence):
            raise ValueError("evidence_ids must be a string list")
        if not isinstance(preserve, list) or not all(isinstance(x, str) for x in preserve):
            raise ValueError("preserve must be a string list")
        return cls(
            proposal_id=proposal_id,
            axis=axis,
            hypothesis=hypothesis,
            edit_atoms=tuple(EditAtom.from_dict(item) for item in raw_atoms),
            expected_effect=str(value.get("expected_effect") or ""),
            evidence_ids=tuple(evidence),
            preserve=tuple(preserve),
            metadata=dict(value.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "axis": self.axis,
            "hypothesis": self.hypothesis,
            "expected_effect": self.expected_effect,
            "evidence_ids": list(self.evidence_ids),
            "edit_atoms": [atom.to_dict() for atom in self.edit_atoms],
            "preserve": list(self.preserve),
            "metadata": dict(self.metadata),
        }


@dataclass
class CandidateRecord:
    k: int
    valid: bool
    errors: List[str] = field(default_factory=list)
    raw_submission: str = ""
    effective: Optional[Dict[str, Any]] = None
    changed_fields: List[str] = field(default_factory=list)
    spec_hash: str = ""
    trajectory: List[Dict[str, Any]] = field(default_factory=list)
    llm_calls: int = 1
    stop_reason: str = ""
    review_log: List[Dict[str, Any]] = field(default_factory=list)
    action: Optional[Dict[str, Any]] = None
    user_message: str = ""
    training_response: str = ""
    dropped_unknown_action_fields: List[str] = field(default_factory=list)
    dropped_unknown_edit_atom_fields: Dict[str, List[str]] = field(default_factory=dict)


def _compaction_params(agent: Mapping[str, Any]) -> Dict[str, Any]:
    for middleware in agent.get("middlewares", []) or []:
        if "context_compaction" in str(middleware.get("import", "")):
            return dict(middleware.get("params") or {})
    return {}


def read_adaptive_base(package_dir: Path) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """Read SAH's full H2 spec plus Adaptive-only runtime pointers."""
    package_dir = Path(package_dir)
    base = hs.read_base_spec(package_dir)
    agent = yaml.safe_load((package_dir / "agent.yaml").read_text()) or {}
    compaction = _compaction_params(agent)
    compaction_enabled = bool(compaction)
    max_context = int(agent.get("max_context_tokens", 131072))
    view = {
        "/system_prompt": base["system_prompt"],
        "/max_context_tokens": max_context,
        "/max_iterations": int(base["agent"]["max_iterations"]),
        "/tool_call_mode": str(agent.get("tool_call_mode", "structured")),
        "/llm/temperature": float(base["sampling"]["temperature"]),
        "/llm/max_tokens": int(base["sampling"]["max_tokens"]),
        "/context_compaction/max_context_tokens": int(
            compaction.get("max_context_tokens", max_context)
        ),
        "/context_compaction/threshold": float(compaction.get("threshold", 0.8)),
        "/context_compaction/keep_iterations": int(compaction.get("keep_iterations", 4)),
        "/context_compaction/compaction_strategy": str(
            compaction.get("compaction_strategy", "tool_result_compaction")
        ),
        # Visible for honest capability reporting, but not in mutable_set_fields:
        # SAH has no stable profile registry, so profile edits fail closed.
        "/skills": [str(item) for item in agent.get("skills", []) or []],
    }
    base["adaptive_runtime"] = {
        "max_context_tokens": view["/max_context_tokens"],
        "tool_call_mode": view["/tool_call_mode"],
        "context_compaction": {
            "enabled": compaction_enabled,
            "max_context_tokens": view["/context_compaction/max_context_tokens"],
            "threshold": view["/context_compaction/threshold"],
            "keep_iterations": view["/context_compaction/keep_iterations"],
            "compaction_strategy": view[
                "/context_compaction/compaction_strategy"
            ],
        },
    }
    return base, view


def _validate_pointer(pointer: str, value: Any) -> Any:
    def integer(lo: int, hi: int) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or not lo <= value <= hi:
            raise ValueError(f"{pointer}: expected integer in [{lo}, {hi}]")
        return int(value)

    def number(lo: float, hi: float) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{pointer}: expected number")
        out = float(value)
        if not lo <= out <= hi:
            raise ValueError(f"{pointer}: expected number in [{lo}, {hi}]")
        return out

    if pointer == "/system_prompt":
        if not isinstance(value, str) or not 40 <= len(value.strip()) <= 16000:
            raise ValueError("/system_prompt: expected 40..16000 characters")
        return value.strip()
    if pointer in {"/max_context_tokens", "/context_compaction/max_context_tokens"}:
        return integer(8192, 200000)
    if pointer == "/max_iterations":
        return integer(8, 80)
    if pointer == "/tool_call_mode":
        if value not in {"structured", "xml"}:
            raise ValueError("/tool_call_mode: expected structured or xml")
        return value
    if pointer == "/llm/temperature":
        return number(0.0, 1.5)
    if pointer == "/llm/max_tokens":
        return integer(1024, 16384)
    if pointer == "/context_compaction/threshold":
        return number(0.5, 0.9)
    if pointer == "/context_compaction/keep_iterations":
        return integer(1, 8)
    if pointer == "/context_compaction/compaction_strategy":
        if value not in {"tool_result_compaction", "llm_summary"}:
            raise ValueError(
                "/context_compaction/compaction_strategy: unsupported strategy"
            )
        return value
    raise ValueError(f"unknown or non-mutable HarnessOpt field: {pointer!r}")


def _section_markers(section_id: str) -> tuple[str, str]:
    if PROMPT_SECTION_ID.fullmatch(section_id) is None:
        raise ValueError(f"invalid HarnessOpt prompt section ID: {section_id!r}")
    return (
        f"<!-- HARNESSOPT:{section_id} -->",
        f"<!-- /HARNESSOPT:{section_id} -->",
    )


def _upsert_prompt_section(prompt: str, section_id: str, content: Any) -> str:
    if not isinstance(content, str) or not content.strip() or len(content) > 4000:
        raise ValueError("prompt_upsert_section requires 1..4000 characters")
    start, end = _section_markers(section_id)
    block = f"{start}\n{content.strip()}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    updated, count = pattern.subn(block, prompt)
    if count > 1:
        raise ValueError(f"prompt contains duplicate managed section {section_id!r}")
    return updated if count == 1 else prompt.rstrip() + "\n\n" + block + "\n"


def _delete_prompt_section(prompt: str, section_id: str) -> str:
    start, end = _section_markers(section_id)
    pattern = re.compile(
        r"\n{0,2}" + re.escape(start) + r".*?" + re.escape(end) + r"\n{0,2}",
        re.DOTALL,
    )
    updated, count = pattern.subn("\n\n", prompt)
    if count != 1:
        raise ValueError(
            f"prompt_delete_section expected one section {section_id!r}, found {count}"
        )
    return updated.strip() + "\n"


def compile_action(
    action: HarnessAction,
    *,
    base_spec: Mapping[str, Any],
    base_view: Mapping[str, Any],
) -> tuple[Dict[str, Any], List[str]]:
    """Compile one semantic action into a full SAH H2 spec plus runtime overlay."""
    working = _json_clone(base_view)
    for atom in action.edit_atoms:
        if atom.kind == "set":
            pointer = ALIASES.get(atom.field, atom.field)
            if not pointer.startswith("/"):
                pointer = "/" + pointer.replace(".", "/")
            if pointer not in MUTABLE_POINTERS:
                raise ValueError(f"unknown or non-mutable HarnessOpt field: {atom.field!r}")
            working[pointer] = _validate_pointer(pointer, atom.value)
        elif atom.kind in {"prompt_upsert_section", "prompt_delete_section"}:
            prompt = str(working["/system_prompt"])
            working["/system_prompt"] = (
                _upsert_prompt_section(prompt, atom.field, atom.value)
                if atom.kind == "prompt_upsert_section"
                else _delete_prompt_section(prompt, atom.field)
            )
            _validate_pointer("/system_prompt", working["/system_prompt"])
        else:
            raise ValueError(
                "SAH adapter has no stable registered-profile catalog; "
                f"{atom.kind} fails closed"
            )

    if (
        working["/max_context_tokens"]
        != working["/context_compaction/max_context_tokens"]
    ):
        raise ValueError(
            "max_context_tokens must match context_compaction.max_context_tokens; "
            "use two edit atoms for this cross-field invariant"
        )
    changed = [
        pointer for pointer in MUTABLE_POINTERS
        if working.get(pointer) != base_view.get(pointer)
    ]
    if not changed:
        raise ValueError("HarnessAction compiles to no state change")

    effective = _json_clone(base_spec)
    effective["system_prompt"] = working["/system_prompt"]
    effective.setdefault("agent", {})["max_iterations"] = working["/max_iterations"]
    effective.setdefault("sampling", {})["temperature"] = working["/llm/temperature"]
    effective.setdefault("sampling", {})["max_tokens"] = working["/llm/max_tokens"]
    effective["adaptive_runtime"] = {
        "max_context_tokens": working["/max_context_tokens"],
        "tool_call_mode": working["/tool_call_mode"],
        "context_compaction": {
            "enabled": bool(
                (base_spec.get("adaptive_runtime") or {})
                .get("context_compaction", {})
                .get("enabled", False)
                or any(
                    pointer.startswith("/context_compaction/")
                    for pointer in changed
                )
            ),
            "max_context_tokens": working[
                "/context_compaction/max_context_tokens"
            ],
            "threshold": working["/context_compaction/threshold"],
            "keep_iterations": working["/context_compaction/keep_iterations"],
            "compaction_strategy": working[
                "/context_compaction/compaction_strategy"
            ],
        },
    }
    return effective, changed


def patch_materialized_package(candidate_dir: Path, effective: Mapping[str, Any]) -> None:
    """Apply Adaptive-only runtime fields after SAH's materializer has run."""
    runtime = dict(effective.get("adaptive_runtime") or {})
    if not runtime:
        return
    candidate_dir = Path(candidate_dir)
    agent_file = candidate_dir / "agent.yaml"
    agent = yaml.safe_load(agent_file.read_text()) or {}
    max_context = int(runtime.get("max_context_tokens", 131072))
    agent["max_context_tokens"] = max_context
    agent["tool_call_mode"] = str(runtime.get("tool_call_mode", "structured"))

    compaction = dict(runtime.get("context_compaction") or {})
    middlewares = [
        item for item in agent.get("middlewares", []) or []
        if "context_compaction" not in str(item.get("import", ""))
    ]
    if compaction.get("enabled", False):
        compaction_entry = {
            "import": (
                "nexau.archs.main_sub.execution.middleware.context_compaction:"
                "ContextCompactionMiddleware"
            ),
            "params": {
                "max_context_tokens": int(
                    compaction.get("max_context_tokens", max_context)
                ),
                "auto_compact": True,
                "threshold": float(compaction.get("threshold", 0.8)),
                "compaction_strategy": str(
                    compaction.get("compaction_strategy", "tool_result_compaction")
                ),
                "keep_iterations": int(compaction.get("keep_iterations", 4)),
            },
        }
        middlewares = [compaction_entry, *middlewares]
    agent["middlewares"] = middlewares
    for item in agent["middlewares"]:
        if "round_and_token_reminder" in str(item.get("import", "")):
            item.setdefault("params", {})["max_context_tokens"] = max_context
    agent_file.write_text(
        yaml.safe_dump(agent, sort_keys=False, allow_unicode=True, width=100)
    )


def default_state() -> Dict[str, Any]:
    return {
        "schema": STATE_SCHEMA,
        "protocol": PROTOCOL,
        "created": time.strftime("%Y%m%d-%H%M%S"),
        "tasks": {},
        "active_adapter": None,
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
) -> Dict[str, Any]:
    existing = dict((state.get("tasks") or {}).get(task_id) or {})
    return {
        "working": dict(
            existing.get("working")
            or {"package": base_package, "score": base_score, "from": "initial"}
        ),
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
        "shared_runtime": "SAH h2spec/1.0 materializer + frozen inner executor",
        "mutable_set_fields": list(MUTABLE_POINTERS),
        "declared_aliases": dict(ALIASES),
        "registered_profiles": [],
        "profile_note": (
            "SAH currently has no stable profile registry; profile operations "
            "are therefore rejected by the deterministic compiler."
        ),
        "constraints": {
            "/system_prompt": {"type": "string", "min_length": 40, "max_length": 16000},
            "/max_context_tokens": {"type": "integer", "min": 8192, "max": 200000},
            "/max_iterations": {"type": "integer", "min": 8, "max": 80},
            "/tool_call_mode": {"enum": ["structured", "xml"]},
            "/llm/temperature": {"type": "number", "min": 0.0, "max": 1.5},
            "/llm/max_tokens": {"type": "integer", "min": 1024, "max": 16384},
            "/context_compaction/max_context_tokens": {
                "type": "integer", "min": 8192, "max": 200000
            },
            "/context_compaction/threshold": {"type": "number", "min": 0.5, "max": 0.9},
            "/context_compaction/keep_iterations": {"type": "integer", "min": 1, "max": 8},
            "/context_compaction/compaction_strategy": {
                "enum": ["tool_result_compaction", "llm_summary"]
            },
        },
        "always_protected": [
            "budgets", "evaluator", "ledger", "model", "policy", "splits",
            "tasks", "tools", "credentials", "implementation",
        ],
    }


def _operator_statistics(attempts: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    buckets: Dict[str, List[Mapping[str, Any]]] = {}
    for attempt in attempts:
        action = attempt.get("action")
        if not isinstance(action, Mapping):
            continue
        keys = {f"axis:{action.get('axis')}"}
        for atom in action.get("edit_atoms", []) or []:
            if isinstance(atom, Mapping):
                keys.add(f"kind:{atom.get('kind')}")
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
    max_prompt_chars: int = 48000,
) -> tuple[str, Dict[str, Any]]:
    archive = dict(task_state.get("archive") or {})
    attempts = list(archive.get("attempts") or [])
    evidence = [
        {
            "evidence_id": item.get("evidence_id"),
            "task_id": task_id,
            "reward": item.get("learning_reward"),
            "metrics": {
                "outcome_score": item.get("outcome_score"),
                "outcome_score_sem": item.get("outcome_score_sem"),
                "relative_delta": (item.get("reward_components") or {}).get(
                    "relative_delta"
                ),
            },
            "feedback": {
                "valid": item.get("valid"),
                "behavior_equivalent": item.get("outcome_behavior_equivalent"),
                "failure_reason": item.get("failure_reason"),
            },
        }
        for item in attempts[-12:]
    ]
    controller = dict(task_state.get("controller") or {})
    payload: Dict[str, Any] = {
        "round_index": round_index,
        "current_harness": _json_clone(current_harness),
        "mutable_set_fields": list(MUTABLE_POINTERS),
        "update_summary": {
            "task_id": task_id,
            "task_spec": task_spec,
            "seed_program": seed_program,
            "seed_score": seed_score,
            "working_score": base_score,
            "max_evaluator_calls": max_evals,
            "rounds_since_confirmed_record": controller.get(
                "rounds_since_confirmed_record", 0
            ),
            "confirmed_record": controller.get("confirmed_record"),
            "policy_updates": controller.get("policy_updates", 0),
        },
        "known_evidence_ids": [
            item["evidence_id"] for item in evidence if item.get("evidence_id")
        ],
        "evidence": evidence,
        "capability_contract": _capability_contract(),
        "optimizer_memory": {
            "operator_statistics": archive.get("operator_statistics", {}),
            "recent_attempts": attempts[-12:],
            "successful_actions": list(archive.get("successful_actions") or [])[-8:],
            "invalid_signatures": list(archive.get("invalid_signatures") or [])[-16:],
        },
        "objective": OBJECTIVE,
    }
    rendered = json.dumps(payload, ensure_ascii=False, default=str)
    if len(rendered) > max_prompt_chars:
        payload = {
            "round_index": round_index,
            "current_harness": payload["current_harness"],
            "update_summary": payload["update_summary"],
            "evidence": _clip_json(payload["evidence"], 16000),
            "capability_contract": payload["capability_contract"],
            "optimizer_memory": _clip_json(payload["optimizer_memory"], 8000),
        }
        rendered = json.dumps(payload, ensure_ascii=False, default=str)
    return rendered, payload


GenerationFn = Callable[[str, str, Mapping[str, Any]], tuple[str, Mapping[str, Any]]]


def make_openai_generator(
    *, base_url: str, model: str, api_key: str = "EMPTY", timeout: float = 600.0
) -> GenerationFn:
    from openai import OpenAI

    client = OpenAI(base_url=base_url, api_key=api_key or "EMPTY", timeout=timeout)

    def generate(
        system: str, user: str, generation: Mapping[str, Any]
    ) -> tuple[str, Mapping[str, Any]]:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=float(generation["temperature"]),
            max_tokens=int(generation["max_tokens"]),
            extra_body={
                "seed": int(generation["seed"]),
                "chat_template_kwargs": {"enable_thinking": False},
            },
        )
        usage = response.usage.model_dump() if response.usage is not None else {}
        return response.choices[0].message.content or "", usage

    return generate


def propose_group(
    *,
    count: int,
    round_index: int,
    base_seed: int,
    base_spec: Mapping[str, Any],
    base_view: Mapping[str, Any],
    base_user_context: str,
    known_evidence_ids: Iterable[str],
    generate: GenerationFn,
    temperature: float = 0.8,
    max_tokens: int = 2048,
) -> List[CandidateRecord]:
    """Sequential K sampling so later samples see prior valid actions."""
    records: List[CandidateRecord] = []
    valid_actions: List[HarnessAction] = []
    seen_hashes = {_digest(base_spec)}
    known_evidence = set(known_evidence_ids)
    for sample_index in range(count):
        proposal_id = f"hopt-r{round_index:03d}-s{sample_index:02d}"
        diversity = {
            "batch_sample": sample_index + 1,
            "batch_size": count,
            "prior_valid_actions": [
                {
                    "proposal_id": action.proposal_id,
                    "axis": action.axis,
                    "hypothesis": action.hypothesis,
                    "edit_targets": [
                        {"kind": atom.kind, "field": atom.field}
                        for atom in action.edit_atoms
                    ],
                }
                for action in valid_actions
            ],
            "requirement": (
                "Propose a causally distinct intervention. Do not merely "
                "paraphrase a prior trigger, threshold, target field, or "
                "algorithm example. Prefer a different mutable axis or "
                "field; if the same target is necessary, use a genuinely "
                "different mechanism and falsifiable hypothesis."
            ),
        }
        user = (
            base_user_context
            + "\n\nBATCH_DIVERSITY:\n"
            + json.dumps(diversity, ensure_ascii=False, default=str)
        )
        generation = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "seed": base_seed + round_index * 1000 + sample_index,
        }
        try:
            response, usage = generate(PROPOSER_SYSTEM_PROMPT, user, generation)
        except Exception as exc:
            records.append(
                CandidateRecord(
                    k=sample_index,
                    valid=False,
                    errors=[f"{type(exc).__name__}: {exc}"],
                    stop_reason="model_error",
                    user_message=user,
                )
            )
            continue
        record = CandidateRecord(
            k=sample_index,
            valid=False,
            raw_submission=response,
            stop_reason="invalid",
            user_message=user,
            trajectory=[
                {"role": "system", "content": PROPOSER_SYSTEM_PROMPT},
                {"role": "user", "content": user},
                {"role": "assistant", "content": response},
            ],
            llm_calls=1,
        )
        try:
            parsed = dict(_extract_json_object(response))
            parsed["proposal_id"] = proposal_id
            record.dropped_unknown_action_fields = sorted(set(parsed) - ACTION_FIELDS)
            for name in record.dropped_unknown_action_fields:
                parsed.pop(name, None)
            raw_atoms = parsed.get("edit_atoms")
            if isinstance(raw_atoms, list):
                clean_atoms = []
                for atom_index, atom in enumerate(raw_atoms):
                    if not isinstance(atom, Mapping):
                        clean_atoms.append(atom)
                        continue
                    unknown = sorted(set(atom) - ATOM_FIELDS)
                    if unknown:
                        record.dropped_unknown_edit_atom_fields[str(atom_index)] = unknown
                    clean_atoms.append(
                        {key: value for key, value in atom.items() if key in ATOM_FIELDS}
                    )
                parsed["edit_atoms"] = clean_atoms
            action = HarnessAction.from_dict(parsed)
            unknown_evidence = sorted(set(action.evidence_ids) - known_evidence)
            if unknown_evidence:
                action = replace(
                    action,
                    evidence_ids=tuple(
                        item for item in action.evidence_ids if item in known_evidence
                    ),
                    metadata={
                        **dict(action.metadata),
                        "dropped_unknown_evidence_ids": unknown_evidence,
                    },
                )
            # A parseable action remains a real proposer transition even when
            # deterministic compilation rejects it. Preserve it so fail-closed
            # candidates receive negative credit instead of disappearing.
            record.action = action.to_dict()
            record.training_response = json.dumps(
                {
                    key: value
                    for key, value in action.to_dict().items()
                    if key != "proposal_id"
                },
                ensure_ascii=False,
                sort_keys=True,
            )
            effective, changed = compile_action(
                action, base_spec=base_spec, base_view=base_view
            )
            candidate_hash = _digest(effective)
            if candidate_hash in seen_hashes:
                raise ValueError("duplicate of another candidate (or of the base)")
            seen_hashes.add(candidate_hash)
            valid_actions.append(action)
            record.valid = True
            record.effective = effective
            record.changed_fields = changed
            record.spec_hash = candidate_hash
            record.stop_reason = "submitted"
            record.review_log = [
                {
                    "name": "adaptive_v1_deterministic_compiler",
                    "ok": True,
                    "rounds": 0,
                    "error": None,
                }
            ]
            if usage:
                record.review_log[0]["usage"] = dict(usage)
        except (TypeError, ValueError) as exc:
            record.errors = [f"{type(exc).__name__}: {exc}"]
        records.append(record)
    return records


def cmd_propose(args, *, load_bases: Callable[..., Dict[str, Dict[str, Any]]]) -> None:
    """Adaptive implementation of ``outer.outer_round propose``."""
    from inner.eft_task import get_task

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
        task = get_task(tid)
        base_package = str(bases[tid]["package"])
        base_score = float(bases[tid]["score"])
        task_state = _task_state(
            state, tid, base_package=base_package, base_score=base_score
        )
        base_spec, base_view = read_adaptive_base(Path(base_package))
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
        base_context, payload = build_user_context(
            task_id=tid,
            round_index=protocol_round,
            task_spec=task.spec,
            seed_program=seed_program,
            seed_score=seed_score,
            base_score=base_score,
            max_evals=args.max_evals,
            current_harness=base_view,
            task_state=task_state,
        )
        prompts[tid] = base_context
        generator = make_openai_generator(
            base_url=base_urls[task_index % len(base_urls)],
            model=args.model,
            api_key="EMPTY",
            timeout=600.0,
        )
        records = propose_group(
            count=args.k,
            round_index=protocol_round,
            base_seed=seed0,
            base_spec=base_spec,
            base_view=base_view,
            base_user_context=base_context,
            known_evidence_ids=payload.get("known_evidence_ids", []),
            generate=generator,
        )
        candidates = []
        for record in records:
            candidate = {
                "k": record.k,
                "proposal_id": f"hopt-r{protocol_round:03d}-s{record.k:02d}",
                "valid": record.valid,
                "errors": record.errors,
                "spec_hash": record.spec_hash,
                "changed_fields": record.changed_fields,
                "stop_reason": record.stop_reason,
                "llm_calls": record.llm_calls,
                "review_log": record.review_log,
                "action": record.action,
                "dropped_unknown_action_fields": record.dropped_unknown_action_fields,
                "dropped_unknown_edit_atom_fields": (
                    record.dropped_unknown_edit_atom_fields
                ),
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
                        "proposal_id": candidate["proposal_id"],
                        "spec_hash": record.spec_hash,
                        "changed_fields": record.changed_fields,
                        "base_package": base_package,
                        "semantic_action": record.action,
                        "effective": record.effective,
                    },
                )
                patch_materialized_package(candidate_dir, record.effective)
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
                    # Keep the actual proposal trace for SAH-compatible audit.
                    # Adaptive replay is still explicitly serialized as plain
                    # system/user/assistant rows by the controller.
                    "trajectory": record.trajectory,
                }
            )
        champion = task_state["champion"]
        per_task[tid] = {
            "base_package": base_package,
            "base_score": base_score,
            "seed_score": bases[tid]["seed_score"],
            "base_spec_hash": _digest(base_spec),
            "champion_package": champion["package"],
            "champion_score": champion["score"],
            "candidates": candidates,
        }
        print(
            f"  {tid}: {sum(item['valid'] for item in candidates)}/{len(candidates)} "
            "valid (sequential Adaptive v1 samples)"
        )

    metadata = {
        "round": args.round,
        "protocol_round": protocol_round,
        "created": time.strftime("%Y%m%d-%H%M%S"),
        "mode": "instance_wise",
        "protocol": PROTOCOL,
        "protocol_state": str(state_path),
        "proposer_topology": {
            "llm_agents": 1,
            "proposer": "ModelHarnessActionPolicy-compatible plain JSON",
            "samples": args.k,
            "analyzer": "deterministic_context_builder",
            "builder": "deterministic_action_compiler",
            "validator": "deterministic_fail_closed",
            "reviewer": "disabled_in_v1",
        },
        "proposer": {
            "base_urls": base_urls,
            "model": args.model,
            "seed": args.seed,
            "temperature": 0.8,
            "max_tokens": 2048,
        },
        "tasks_order": args.tasks,
        "max_evals": args.max_evals,
        "k": args.k,
        "total_rounds": getattr(args, "total_rounds", None),
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
        f"candidates -> {round_dir}"
    )
