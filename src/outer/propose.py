"""Run H1 to edit private candidate H2 packages (instance-wise).

Each candidate = one full H1 agent run (inspect -> edit -> validate -> submit)
against the M_phi endpoint, conditioned on ONE task instance. The K runs for a
task share that task's user message (= one GRPO group); diversity comes from
H1's temperature (1.0, fixed in its agent.yaml) plus per-run sampling seeds.
outer_round threads run_once across all (task, k) jobs and serving replicas;
the propose-session contextvar is thread-local, so sessions never collide.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional

from outer import harness_spec as hs
from outer.proposer_io import H1_PACKAGE  # noqa: F401 (used by run_once)
from outer.propose_session import ProposeSession, propose_scope
from outer.materialize import materialize


@dataclass
class CandidateRecord:
    k: int
    valid: bool
    errors: List[str] = field(default_factory=list)
    raw_submission: str = ""
    spec: Optional[Dict[str, Any]] = None        # validated partial spec
    effective: Optional[Dict[str, Any]] = None   # spec folded over base
    review_log: list = field(default_factory=list)  # validate_harness component audit
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

    trajectory: List[Dict[str, Any]] = []
    err: Optional[str] = None
    # Every parallel proposer gets a complete private copy.  H1 can inspect and
    # edit real H2 files, but can never mutate the shared accepted package or
    # another candidate's draft.
    with TemporaryDirectory(prefix=f"h1_candidate_{k:02d}_") as td:
        draft_dir = Path(td) / "h2"
        try:
            materialize(
                base_spec,
                draft_dir,
                meta={"effective": base_spec},
                # Historical parents may predate proposer-owned component
                # catalogs. Preserve their prompt byte-for-byte in the private
                # draft so H1—not runtime—must repair it before submission.
                validate_prompt=False,
            )
        except Exception as e:
            return CandidateRecord(
                k=k,
                valid=False,
                errors=[f"cannot initialize private H2 workspace: {type(e).__name__}: {e}"],
                stop_reason="workspace_error",
            )
        session = ProposeSession(base_spec=base_spec, draft_dir=draft_dir)
        with propose_scope(session):
            agent = None
            try:
                agent = Agent(config=config)
                agent.run(message=user_message)
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
            finally:
                if agent is not None:
                    trajectory = _dump_history(agent)

    rec = CandidateRecord(
        k=k, valid=bool(session.submitted and session.effective is not None
                        and session.changed_fields and not session.errors),
        raw_submission=session.raw_submission,
        spec=session.partial_spec, effective=session.effective,
        changed_fields=session.changed_fields,
        spec_hash=hs.spec_hash(session.effective) if session.effective else "",
        trajectory=trajectory,
        llm_calls=sum(1 for m in trajectory
                      if str(m.get("role", "")).lower().endswith("assistant")),
        stop_reason="harness_error" if err else
                    ("submitted" if session.submitted and session.effective
                     else "invalid_submission" if session.submitted
                     else "no_submission"),
    )
    rec.review_log = list(session.component_audit)
    if err:
        rec.errors = [err]
    elif not session.submitted:
        rec.errors = ["proposer never called submit_harness"]
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
