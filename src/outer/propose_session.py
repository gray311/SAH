"""Per-run proposer session: state behind H1's validate_spec/submit_spec tools.

Mirrors inner/session.py: the propose driver sets the active session in a
contextvar for the duration of one H1 agent run; the tool bindings and the
submit-reminder middleware resolve it via get_session(). Thread-safe: each
proposer thread runs in its own context.
"""
from __future__ import annotations

import contextvars
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from outer import harness_spec as hs


@dataclass
class ProposeSession:
    base_spec: Dict[str, Any]
    validations: int = 0
    submitted: bool = False
    raw_submission: str = ""
    partial_spec: Optional[Dict[str, Any]] = None
    effective: Optional[Dict[str, Any]] = None
    changed_fields: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def _check(self, spec_yaml: str):
        v = hs.parse_and_validate(spec_yaml)
        if not v.valid:
            return None, None, [], v.errors
        eff = hs.merge_with_base(v.spec, self.base_spec)
        differs, changed = hs.differs_from_base(eff, self.base_spec)
        if not differs:
            return v.spec, eff, [], ["spec is identical to the current harness (no-op)"]
        return v.spec, eff, changed, []

    def validate(self, spec_yaml: str) -> str:
        self.validations += 1
        _, _, changed, errors = self._check(spec_yaml)
        if errors:
            return "INVALID:\n- " + "\n- ".join(errors)
        return ("VALID. This spec changes: " + ", ".join(changed) +
                ". You can refine further or submit_spec now.")

    def submit(self, spec_yaml: str) -> str:
        self.submitted = True
        self.raw_submission = spec_yaml
        spec, eff, changed, errors = self._check(spec_yaml)
        if errors:
            self.errors = errors
            return "SUBMITTED but INVALID (minimum reward):\n- " + "\n- ".join(errors)
        self.partial_spec, self.effective, self.changed_fields = spec, eff, changed
        return f"SUBMITTED. Candidate spec accepted; changes: {', '.join(changed)}."


_CURRENT: "contextvars.ContextVar[Optional[ProposeSession]]" = contextvars.ContextVar(
    "propose_session", default=None
)


def get_session() -> ProposeSession:
    s = _CURRENT.get()
    if s is None:
        raise RuntimeError("no active ProposeSession (tool called outside propose_scope)")
    return s


@contextmanager
def propose_scope(session: ProposeSession):
    token = _CURRENT.set(session)
    try:
        yield session
    finally:
        _CURRENT.reset(token)
