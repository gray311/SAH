"""NexAU tool bindings for H1's fixed action space.

Bound by ``outer.harness.tools.design:<fn>`` in agent.yaml. Plain functions
(str in, str out) reaching the active ProposeSession through the runtime
bridge.
"""
from __future__ import annotations

from outer.harness.tools.runtime import get_session


def validate_spec(spec_yaml: str) -> str:
    """Validate a draft H2 spec; report changed fields or exact errors."""
    return get_session().validate(spec_yaml)


def submit_spec(spec_yaml: str) -> str:
    """Submit the final candidate H2 spec (stop tool)."""
    return get_session().submit(spec_yaml)
