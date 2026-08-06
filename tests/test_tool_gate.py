"""Mechanical middleware tool gate: enforcement, exemption, auto-lift."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from inner.harness.tools import discovery  # noqa: E402
from inner.harness.tools.runtime import session_scope  # noqa: E402
from inner.session import BudgetLedger, InnerSession  # noqa: E402


def _session() -> InnerSession:
    session = InnerSession(
        task=SimpleNamespace(initial_program="x = 1"),
        ledger=BudgetLedger(max_evaluator_calls=5, max_probe_calls=5),
    )
    session.best_score = 1.0
    return session


class ToolGateTest(unittest.TestCase):
    def test_refusal_consumes_no_budget_and_probe_satisfies(self) -> None:
        session = _session()
        session.request_tool_gate("g1", ["probe_solution"])
        with session_scope(session):
            out = discovery.evaluate_solution()
        self.assertIn("GATED by middleware 'g1'", out)
        self.assertEqual(session.ledger.evaluator_calls, 0)
        self.assertIsNotNone(session.tool_gate)
        # satisfying tool clears the gate
        self.assertIsNone(session.check_tool_gate("probe_solution"))
        self.assertIsNone(session.tool_gate)
        gate = session.middleware_audit["g1"]["gate"]
        self.assertEqual(gate["enforced"], 1)
        self.assertEqual(gate["refused"], 1)
        self.assertEqual(gate["satisfied"], 1)
        self.assertEqual(gate["auto_lifted"], 0)

    def test_finish_is_never_gated(self) -> None:
        session = _session()
        session.request_tool_gate("g1", ["probe_solution"])
        self.assertIsNone(session.check_tool_gate("finish"))
        self.assertIsNotNone(session.tool_gate)

    def test_auto_lift_after_repeated_refusals(self) -> None:
        session = _session()
        session.request_tool_gate("g1", ["probe_solution"])
        self.assertIsNotNone(session.check_tool_gate("evaluate_solution"))
        self.assertIsNotNone(session.check_tool_gate("edit_solution"))
        # two refusals -> lifted
        self.assertIsNone(session.tool_gate)
        self.assertIsNone(session.check_tool_gate("evaluate_solution"))
        gate = session.middleware_audit["g1"]["gate"]
        self.assertEqual(gate["auto_lifted"], 1)

    def test_invalid_gate_requests_are_rejected(self) -> None:
        session = _session()
        with self.assertRaises(ValueError):
            session.request_tool_gate("g1", [])
        with self.assertRaises(ValueError):
            session.request_tool_gate("g1", ["finish"])
        with self.assertRaises(ValueError):
            session.request_tool_gate("g1", ["not_a_tool"])

    def test_snapshot_exposes_active_gate(self) -> None:
        from inner.harness.middleware.generated_context import GeneratedHookTracker
        session = _session()
        tracker = GeneratedHookTracker()
        session.request_tool_gate("g1", ["probe_solution"])
        state = tracker.snapshot(SimpleNamespace(current_iteration=0), session)
        self.assertEqual(state["active_tool_gate"]["require"], ("probe_solution",))


if __name__ == "__main__":
    unittest.main()
