"""Run H1 (the proposer NexAU agent) to sample candidate H2 specs (instance-wise).

Each candidate = one full H1 agent run (draft -> validate_spec -> submit_spec)
against the M_phi endpoint, conditioned on ONE task instance. The K runs for a
task share that task's user message (= one GRPO group); diversity comes from
H1's temperature (1.0, fixed in its agent.yaml) plus per-run sampling seeds.
outer_round threads run_once across all (task, k) jobs and serving replicas;
the propose-session contextvar is thread-local, so sessions never collide.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from outer import harness_spec as hs
from outer.proposer_io import H1_PACKAGE  # noqa: F401 (used by run_once)
from outer.propose_session import ProposeSession, propose_scope
from outer.reviewer.reviewer import review_tool_code


@dataclass
class CandidateRecord:
    k: int
    valid: bool
    errors: List[str] = field(default_factory=list)
    raw_submission: str = ""
    spec: Optional[Dict[str, Any]] = None        # validated partial spec
    effective: Optional[Dict[str, Any]] = None   # spec folded over base
    review_log: list = field(default_factory=list)  # per-tool gate/repair outcomes
    changed_fields: List[str] = field(default_factory=list)
    spec_hash: str = ""
    trajectory: List[Dict[str, Any]] = field(default_factory=list)
    llm_calls: int = 0
    stop_reason: str = ""


def _dump_history(agent) -> List[Dict[str, Any]]:
    out = []
    try:
        for msg in agent.history:
            try:
                out.append(msg.model_dump())
            except Exception:
                out.append({"role": str(getattr(msg, "role", "?")),
                            "content": str(getattr(msg, "content", ""))[:4000]})
    except Exception:
        pass
    return out


def _make_repair_fn(base_url: str, model: str, api_key: str, timeout: float):
    """Repair callable bound to the SAME frozen served model (capability
    parity — never a stronger external model)."""
    from openai import OpenAI
    client = OpenAI(base_url=base_url, api_key=api_key or "EMPTY", timeout=timeout)

    def repair(system: str, user: str) -> str:
        resp = client.chat.completions.create(
            model=model, temperature=0.2, max_tokens=2048,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            extra_body={"chat_template_kwargs": {"enable_thinking": False}})
        return resp.choices[0].message.content or ""

    return repair


def run_once(k: int, *, base_spec: Dict[str, Any], user_message: str,
              base_url: str, model: str, api_key: str, seed: Optional[int],
              timeout: float) -> CandidateRecord:
    from nexau import Agent, AgentConfig

    config = AgentConfig.from_yaml(H1_PACKAGE / "agent.yaml")
    llm = config.llm_config
    llm.model = model
    llm.base_url = base_url
    llm.api_key = api_key
    llm.timeout = timeout
    # H1's own sampling (temperature 1.0 etc.) is part of the fixed harness —
    # only endpoint + per-run seed + thinking-off are injected here.
    extra = getattr(llm, "extra_params", None)
    if not isinstance(extra, dict):
        extra = {}
        try:
            llm.extra_params = extra
        except Exception:
            pass
    eb = extra.setdefault("extra_body", {})
    eb.setdefault("chat_template_kwargs", {})["enable_thinking"] = False
    if seed is not None:
        eb["seed"] = seed

    session = ProposeSession(base_spec=base_spec)
    trajectory: List[Dict[str, Any]] = []
    err: Optional[str] = None
    with propose_scope(session):
        try:
            agent = Agent(config=config)
            agent.run(message=user_message)
            trajectory = _dump_history(agent)
        except Exception as e:
            err = f"{type(e).__name__}: {e}"

    # h2spec/1.0: gate + reviewer-repair every generated tool BEFORE the
    # candidate is accepted. The repairer MUST be the FROZEN M0 — under split
    # serving `base_url` is the trained proposer M_phi, so a repair on it would
    # break capability parity (the reviewer could then "fix" tool code using the
    # trained policy, not the frozen executor that actually runs it). The worker
    # exports SAH_ANALYSIS_BASE_URL = a frozen replica; use it, falling back to
    # base_url only when every replica is the frozen base (step 1). Tools that
    # never pass are dropped; if that leaves no real mutation the candidate is
    # invalid (fail-closed).
    import os as _os
    repair_url = _os.environ.get("SAH_ANALYSIS_BASE_URL") or base_url
    review_log: List[Dict[str, Any]] = []
    if session.submitted and session.effective and session.effective.get("new_tools"):
        repair_fn = _make_repair_fn(repair_url, model, api_key, timeout)
        kept = []
        for tool in session.effective["new_tools"]:
            try:
                outcome = review_tool_code(tool["implementation_py"],
                                           repair_fn=repair_fn, max_rounds=2)
            except Exception as e:  # a reviewer failure drops one tool, never the round
                review_log.append({"name": tool["name"], "ok": False, "rounds": 0,
                                   "error": f"reviewer crashed: {e}", "history": []})
                continue
            review_log.append({"name": tool["name"], "ok": outcome.ok,
                               "rounds": outcome.rounds,
                               "error": outcome.final_error,
                               "history": outcome.history})
            if outcome.ok:
                tool["implementation_py"] = outcome.code  # accept repaired code
                kept.append(tool)
        if kept:
            session.effective["new_tools"] = kept
        else:
            session.effective.pop("new_tools", None)
            session.changed_fields = [c for c in session.changed_fields
                                      if not c.startswith("new_tools")]

    # h2spec/1.0: generated middlewares run IN-PROCESS — gate them (stricter),
    # drop any that fail. (Skills are pure text: no gate needed.)
    if session.submitted and session.effective and session.effective.get("new_middlewares"):
        from outer.static_gates import check_middleware_code
        kept_mw = []
        for mw in session.effective["new_middlewares"]:
            ok, errs = check_middleware_code(mw["implementation_py"], mw["hook"])
            review_log.append({"name": "mw:" + mw["name"], "ok": ok, "rounds": 0,
                               "error": None if ok else "; ".join(errs), "history": []})
            if ok:
                kept_mw.append(mw)
        if kept_mw:
            session.effective["new_middlewares"] = kept_mw
        else:
            session.effective.pop("new_middlewares", None)
            session.changed_fields = [c for c in session.changed_fields
                                      if not c.startswith("new_middlewares")]

    rec = CandidateRecord(
        k=k, valid=bool(session.submitted and session.effective is not None
                        and session.changed_fields),
        raw_submission=session.raw_submission,
        spec=session.partial_spec, effective=session.effective,
        changed_fields=session.changed_fields,
        spec_hash=hs.spec_hash(session.effective) if session.effective else "",
        trajectory=trajectory,
        llm_calls=sum(1 for m in trajectory
                      if str(m.get("role", "")).lower().endswith("assistant")),
        stop_reason="harness_error" if err else
                    ("submitted" if session.submitted else "no_submission"),
    )
    rec.review_log = review_log
    if err:
        rec.errors = [err]
    elif not session.submitted:
        rec.errors = ["proposer never called submit_spec"]
    elif session.errors:
        rec.errors = session.errors
    return rec


def dedup_group(records: List[CandidateRecord], base_spec: Dict[str, Any]) -> None:
    """Invalidate duplicates within one task's GRPO group (in place)."""
    seen = {hs.spec_hash(base_spec)}
    for rec in sorted(records, key=lambda r: r.k):
        if not rec.valid:
            continue
        if rec.spec_hash in seen:
            rec.valid = False
            rec.errors = ["duplicate of another candidate (or of the base)"]
        else:
            seen.add(rec.spec_hash)
