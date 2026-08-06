"""Run H2 (M0 + the declarative NexAU harness package) on one EFT task.

Loads ``inner/harness/agent.yaml`` (the harness surface: system prompt + tools +
skills + middlewares + sampling), injects the frozen-executor serving endpoint
and the eval budget at runtime, and drives one task's edit->evaluate loop.

The harness *definition* lives entirely in ``inner/harness/`` — this module only
wires the endpoint/budget and collects results, so the outer proposer can later
mutate the package without touching this code.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# ensure `inner...` (and the agent.yaml tool/middleware bindings) are importable
_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from inner.eft_task import EFTTask  # noqa: E402
from inner.session import BudgetLedger, InnerSession, session_scope  # noqa: E402

AGENT_YAML = Path(__file__).resolve().parent / "harness" / "agent.yaml"


@dataclass
class LLMEndpoint:
    model: str = "qwen3.5-9b"
    base_url: str = "http://127.0.0.1:8800/v1"
    api_key: str = "EMPTY"
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: Optional[int] = 20
    max_tokens: int = 8192
    timeout: float = 600.0
    max_retries: int = 2
    enable_thinking: bool = False  # Qwen3.5: keep outputs clean/fast (matches Weave)
    seed: Optional[int] = None


@dataclass
class H2Config:
    max_evaluator_calls: int = 10
    max_iterations: Optional[int] = None  # None -> keep agent.yaml's value
    eval_timeout_s: Optional[float] = None
    python_exe: Optional[str] = None      # interpreter with task deps for eval subprocess


@dataclass
class InnerResult:
    task_id: str
    source: str
    best_score: float
    seed_score: float
    best_metrics: Dict[str, float]
    best_program: str
    stop_reason: str
    ledger: Dict[str, Any]
    steps: List[Dict[str, Any]] = field(default_factory=list)
    middleware_audit: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    tool_audit: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    skill_audit: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    decode_seed: Optional[int] = None
    score_eligible: bool = True
    trajectory: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


def _expected_generated_middlewares(agent_yaml: Path) -> List[str]:
    """Names of generated middleware that must mount and enter their hook."""

    payload = yaml.safe_load(Path(agent_yaml).read_text()) or {}
    names: List[str] = []
    for row in payload.get("middlewares", []):
        if not isinstance(row, dict):
            continue
        binding = str(row.get("import", ""))
        if not binding.endswith(":GeneratedMiddleware"):
            continue
        module = binding.split(":", 1)[0]
        names.append(module.rsplit(".", 1)[-1])
    return names


def _expected_generated_components(agent_yaml: Path) -> Dict[str, Dict[str, str]]:
    payload = yaml.safe_load(Path(agent_yaml).read_text()) or {}
    tools: Dict[str, str] = {}
    for row in payload.get("tools", []):
        if isinstance(row, dict) and "custom_runtime" in str(row.get("binding", "")):
            tools[str(row.get("name"))] = str((row.get("extra_kwargs") or {}).get("py_path", ""))
    skills: Dict[str, str] = {}
    for source in payload.get("skills", []):
        name = Path(str(source)).name
        if name != "discovery-optimization":
            skills[name] = str(source)
    return {"tools": tools, "skills": skills}


def _is_score_eligible(stop_reason: str, participation_issues: List[str]) -> bool:
    """Publish only a completed harness route with participating middleware."""

    return stop_reason != "harness_error" and not participation_issues


def _record_skill_loads(session: InnerSession, trajectory: Optional[List[Dict[str, Any]]]) -> None:
    def walk(value):
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)

    for node in walk(trajectory or []):
        if not any(str(value) == "LoadSkill" for value in node.values()):
            continue
        encoded = str(node)
        for name in session.skill_audit:
            if name in encoded:
                session.record_skill_load(name)


def _initial_message(task: EFTTask, seed_score: float, seed_valid: float, budget: int) -> str:
    msg = (
        f"# Task\n{task.spec.strip()}\n\n"
        f"# Current program\n```python\n{task.initial_program}\n```\n\n"
        f"# Baseline\nThe seed program scores combined_score = {seed_score:.6g} "
        f"(validity {seed_valid:g}). Beat it. You have {budget} evaluations.\n\n"
    )
    parents = getattr(task, "crossover_parents", None)
    if parents:
        msg += "# Alternative high-scoring approaches (different search basins)\n"
        msg += ("These reached similar scores via DIFFERENT strategies. Consider "
                "hybridizing their ideas with the current program — crossover often "
                "escapes local optima that pure mutation cannot:\n")
        for i, par in enumerate(parents):
            msg += (f"\n## Alternative {i+1} (score {par.get('score', 0):.6g})\n"
                    f"```python\n{par.get('program', '')[:4000]}\n```\n")
        msg += "\n"
    msg += ("Load the discovery-optimization skill, then start by proposing an "
            "improved EVOLVE-BLOCK with edit_solution and scoring it with "
            "evaluate_solution.")
    return msg


def _override_llm(config, ep: LLMEndpoint, *, preserve_sampling: bool = False,
                  top_k_override: Optional[int] = None) -> None:
    """Inject the serving endpoint into the loaded agent config.

    preserve_sampling: keep the agent.yaml's temperature/top_p/max_tokens
    (candidate H2 packages own their sampling — it is part of the genome);
    only the endpoint/model/timeouts are injected. top_k_override applies the
    candidate's top_k (which lives outside agent.yaml, in its meta.json).
    """
    llm = config.llm_config
    llm.model = ep.model
    llm.base_url = ep.base_url
    llm.api_key = ep.api_key
    llm.timeout = ep.timeout
    llm.max_retries = ep.max_retries
    if not preserve_sampling:
        llm.temperature = ep.temperature
        llm.top_p = ep.top_p
        llm.max_tokens = ep.max_tokens
    extra = getattr(llm, "extra_params", None)
    if not isinstance(extra, dict):
        extra = {}
        try:
            llm.extra_params = extra
        except Exception:
            return
    extra_body = extra.setdefault("extra_body", {})
    top_k = top_k_override if top_k_override is not None else ep.top_k
    if top_k is not None:
        extra_body["top_k"] = top_k
    extra_body.setdefault("chat_template_kwargs", {})["enable_thinking"] = ep.enable_thinking
    if ep.seed is not None:
        extra_body["seed"] = int(ep.seed)


def _extract_trajectory(agent) -> List[Dict[str, Any]]:
    traj: List[Dict[str, Any]] = []
    try:
        for msg in agent.history:
            try:
                traj.append(msg.model_dump())
            except Exception:
                traj.append({"role": str(getattr(msg, "role", "?")),
                             "content": str(getattr(msg, "content", ""))})
    except Exception:
        pass
    return traj


def _count_llm_calls(agent) -> int:
    n = 0
    try:
        for msg in agent.history:
            if str(getattr(msg, "role", "")).lower().endswith("assistant"):
                n += 1
    except Exception:
        pass
    return n


def run_task(
    task: EFTTask,
    *,
    endpoint: LLMEndpoint,
    h2: H2Config,
    keep_trajectory: bool = True,
    checkpoint_path: Optional[str] = None,
    harness_dir: Optional[Path] = None,
) -> InnerResult:
    """Run H2 on one EFT task; return best program + full ledger/trajectory.

    harness_dir: run a *candidate* H2 package (outer loop) instead of the
    built-in ``inner/harness``. The dir must contain ``agent.yaml``; it is put
    first on ``sys.path`` so its ``middlewares/`` package resolves. One
    candidate per process — different candidates may define the same module
    names, so never load two candidate packages into one interpreter.
    """
    from nexau import Agent, AgentConfig  # lazy: needs the nexau env

    agent_yaml = AGENT_YAML
    cand_top_k: Optional[int] = None
    if harness_dir is not None:
        harness_dir = Path(harness_dir).resolve()
        agent_yaml = harness_dir / "agent.yaml"
        if str(harness_dir) not in sys.path:
            sys.path.insert(0, str(harness_dir))
        meta_file = harness_dir / "meta.json"
        if meta_file.exists():
            try:
                import json as _json
                cand_top_k = (_json.loads(meta_file.read_text())
                              .get("effective", {}).get("sampling", {}).get("top_k"))
            except Exception:
                cand_top_k = None
    expected_middlewares = (
        _expected_generated_middlewares(agent_yaml) if harness_dir is not None else []
    )
    expected_components = (
        _expected_generated_components(agent_yaml) if harness_dir is not None
        else {"tools": {}, "skills": {}}
    )

    ledger = BudgetLedger(max_evaluator_calls=h2.max_evaluator_calls)
    session = InnerSession(task=task, ledger=ledger,
                           eval_timeout_s=h2.eval_timeout_s, python_exe=h2.python_exe,
                           checkpoint_path=checkpoint_path,
                           harness_dir=str(harness_dir) if harness_dir is not None else None)
    for name, source in expected_components["tools"].items():
        session.register_tool(name, source)
    for name, source in expected_components["skills"].items():
        session.register_skill(name, source)
    seed = session.seed_baseline()
    seed_score = seed.combined_score

    config = AgentConfig.from_yaml(agent_yaml)
    _override_llm(config, endpoint,
                  preserve_sampling=harness_dir is not None,
                  top_k_override=cand_top_k)
    if h2.max_iterations is not None:
        config.max_iterations = h2.max_iterations

    stop_reason, err, trajectory = "completed", None, None
    agent = None
    with session_scope(session):
        try:
            agent = Agent(config=config)
            agent.run(message=_initial_message(task, seed_score, seed.validity,
                                               h2.max_evaluator_calls))
        except Exception as e:  # a harness failure must not lose the seed baseline
            stop_reason, err = "harness_error", f"{type(e).__name__}: {e}"
        finally:
            # Preserve partial histories too.  Executor failures are often the
            # most useful case-study evidence, so an exception must not discard
            # the assistant/tool transcript accumulated before it occurred.
            if agent is not None:
                ledger.llm_calls = _count_llm_calls(agent)
                if keep_trajectory:
                    trajectory = _extract_trajectory(agent)

    participation_issues = session.middleware_participation_issues(
        expected_middlewares
    )
    _record_skill_loads(session, trajectory)
    # A harness exception may leave the evaluator's seed checkpoint in the
    # session.  Keep that diagnostic value, but never publish it as a scored
    # executor trajectory: no completed executor action produced it.
    score_eligible = _is_score_eligible(stop_reason, participation_issues)
    if participation_issues:
        participation_error = (
            "MiddlewareParticipationError: " + "; ".join(participation_issues)
        )
        session.history_note(participation_error)
        if trajectory is not None:
            trajectory.append({
                "role": "framework",
                "content": participation_error,
            })
        err = f"{err}; {participation_error}" if err else participation_error
        if stop_reason == "completed":
            stop_reason = "middleware_participation_failed"

    s = session.summary()
    return InnerResult(
        task_id=task.task_id, source=task.source,
        best_score=session.best_score if session.best_score != float("-inf") else seed_score,
        seed_score=seed_score, best_metrics=session.best_metrics,
        best_program=session.best_program or task.initial_program,
        stop_reason=stop_reason, ledger=s["ledger"], steps=s["steps"],
        middleware_audit=s["middleware_audit"], tool_audit=s["tool_audit"],
        skill_audit=s["skill_audit"], decode_seed=endpoint.seed,
        score_eligible=score_eligible,
        trajectory=trajectory, error=err,
    )
