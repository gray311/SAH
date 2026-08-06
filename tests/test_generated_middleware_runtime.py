from __future__ import annotations

import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from inner.harness.middleware.generated_context import GeneratedHookTracker  # noqa: E402
from inner.harness.tools.runtime import session_scope  # noqa: E402
from inner.harness_runner import _expected_generated_middlewares  # noqa: E402
from inner.session import BudgetLedger, InnerSession  # noqa: E402
from outer.harness_spec import parse_and_validate  # noqa: E402
from outer.materialize import _build_custom_middlewares  # noqa: E402
from outer.static_gates import check_middleware_code  # noqa: E402


def _session(program: str = "x = 1"):
    session = InnerSession(
        task=SimpleNamespace(initial_program=program),
        ledger=BudgetLedger(max_evaluator_calls=20, max_probe_calls=30),
    )
    session.best_score = 1.0
    return session


class GeneratedMiddlewareRuntimeTest(unittest.TestCase):
    def test_tracks_structural_family_not_literal_values(self) -> None:
        tracker = GeneratedHookTracker()
        session = _session("x = 1")

        first = tracker.snapshot(SimpleNamespace(current_iteration=0), session)
        session.current_program = "x = 2"
        second = tracker.snapshot(SimpleNamespace(current_iteration=1), session)
        session.current_program = "x = [2]"
        third = tracker.snapshot(SimpleNamespace(current_iteration=2), session)

        self.assertEqual(first["family_streak"], 1)
        self.assertEqual(second["family_streak"], 2)
        self.assertEqual(len(second["families_explored"]), 1)
        self.assertEqual(third["family_streak"], 1)
        self.assertEqual(len(third["families_explored"]), 2)

    def test_exposes_stall_and_last_error(self) -> None:
        tracker = GeneratedHookTracker()
        session = _session()
        tracker.snapshot(SimpleNamespace(current_iteration=0), session)

        session.ledger.evaluator_calls = 2
        session.history.append(SimpleNamespace(
            kind="edit_eval", error=None, validity=1.0, combined_score=1.0,
        ))
        session.history.extend([
            SimpleNamespace(kind="probe", error=None, validity=1.0,
                            combined_score=0.9),
            SimpleNamespace(kind="probe", error="SyntaxError: bad candidate",
                            validity=0.0, combined_score=0.0),
        ])
        view = tracker.snapshot(SimpleNamespace(current_iteration=3), session)

        self.assertEqual(view["stalled_evals"], 2)
        self.assertEqual(view["last_error"], "SyntaxError: bad candidate")
        self.assertEqual(view["evaluations_remaining"], 18)
        self.assertEqual(view["evals_done"], 2)
        self.assertEqual(view["probes_since_eval"], 2)
        self.assertEqual(view["last_family"], view["families_explored"][0])
        self.assertEqual(view["state"]["iteration"], 3)

    def test_gate_accepts_documented_diversity_state(self) -> None:
        code = '''
def before_model(hook_input):
    state = hook_input.get("state", {})
    if state.get("family_streak", 0) >= 5:
        return "switch structure"
    return None
'''
        ok, errors = check_middleware_code(code, "before_model")
        self.assertTrue(ok, errors)

    def test_gate_rejects_undefined_state_and_framework_attributes(self) -> None:
        undefined = '''
def before_model(hook_input):
    state = hook_input.get("state", {})
    return "switch" if state.get("magic_counter", 0) else None
'''
        direct_framework_access = '''
def before_model(hook_input):
    return str(hook_input.current_iteration)
'''

        ok, errors = check_middleware_code(undefined, "before_model")
        self.assertFalse(ok)
        self.assertTrue(any("magic_counter" in e for e in errors))
        ok, errors = check_middleware_code(direct_framework_access, "before_model")
        self.assertFalse(ok)
        self.assertTrue(any("unsupported hook_input attribute" in e for e in errors))

    def test_spec_rejects_unadapted_non_model_hooks(self) -> None:
        result = parse_and_validate('''
schema: h2spec/1.0
new_middlewares:
  - name: unsafe_tool_hook
    hook: after_tool
    description: unsupported framework contract
    implementation_py: |
      def after_tool(hook_input):
          return "note"
''')
        self.assertFalse(result.valid)
        self.assertTrue(any("hook" in error for error in result.errors))

    def test_materialized_diversity_hook_fires_and_is_audited(self) -> None:
        class HookResult:
            @staticmethod
            def no_changes():
                return {"changed": False}

            @staticmethod
            def with_modifications(**kwargs):
                return {"changed": True, **kwargs}

        class Middleware:
            pass

        class Message:
            def __init__(self, role, content):
                self.role, self.content = role, content

        class Role:
            FRAMEWORK = "framework"

        class TextBlock:
            def __init__(self, text):
                self.text = text

        modules = {
            "nexau": types.ModuleType("nexau"),
            "nexau.archs": types.ModuleType("nexau.archs"),
            "nexau.archs.main_sub": types.ModuleType("nexau.archs.main_sub"),
            "nexau.archs.main_sub.execution": types.ModuleType(
                "nexau.archs.main_sub.execution"
            ),
            "nexau.archs.main_sub.execution.hooks": types.ModuleType(
                "nexau.archs.main_sub.execution.hooks"
            ),
            "nexau.core": types.ModuleType("nexau.core"),
            "nexau.core.messages": types.ModuleType("nexau.core.messages"),
        }
        hooks = modules["nexau.archs.main_sub.execution.hooks"]
        hooks.BeforeModelHookInput = object
        hooks.HookResult = HookResult
        hooks.Middleware = Middleware
        messages = modules["nexau.core.messages"]
        messages.Message = Message
        messages.Role = Role
        messages.TextBlock = TextBlock
        previous = {name: sys.modules.get(name) for name in modules}
        sys.modules.update(modules)

        try:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                code = '''
def before_model(hook_input):
    state = hook_input.get("state", {})
    if state.get("iteration", 0) >= 5 and state.get("family_streak", 0) >= 5:
        return "DIVERSIFICATION_STALLED"
    return None
'''
                _build_custom_middlewares({"new_middlewares": [{
                    "name": "enforce_diversification",
                    "hook": "before_model",
                    "implementation_py": code,
                }]}, root)
                path = root / "middlewares" / "enforce_diversification.py"
                spec = importlib.util.spec_from_file_location("generated_mw_test", path)
                module = importlib.util.module_from_spec(spec)
                assert spec.loader is not None
                spec.loader.exec_module(module)

                session = _session()
                with session_scope(session):
                    middleware = module.GeneratedMiddleware()
                    outcomes = [
                        middleware.before_model(SimpleNamespace(
                            current_iteration=i, messages=[]
                        ))
                        for i in range(6)
                    ]

                self.assertEqual(
                    [row["changed"] for row in outcomes],
                    [False, False, False, False, False, True],
                )
                notes = [row.edit_note for row in session.history if row.kind == "note"]
                self.assertTrue(any("FIRED iteration=5" in note for note in notes))
                audit = session.middleware_audit["enforce_diversification"]
                self.assertEqual(audit["mounts"], 1)
                self.assertEqual(audit["invocations"], 6)
                self.assertEqual(audit["fires"], 1)
                self.assertEqual(audit["errors"], 0)
                self.assertEqual(
                    session.middleware_participation_issues(
                        ["enforce_diversification"]
                    ),
                    [],
                )
        finally:
            for name, old in previous.items():
                if old is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = old

    def test_middleware_may_be_ineffective_but_must_be_invoked(self) -> None:
        session = _session()
        session.register_middleware("quiet_hook", "before_model")
        for iteration in range(3):
            session.record_middleware_event(
                "quiet_hook", "invoked", iteration=iteration
            )

        self.assertEqual(session.middleware_audit["quiet_hook"]["fires"], 0)
        self.assertEqual(
            session.middleware_participation_issues(["quiet_hook"]), []
        )

    def test_missing_or_crashing_middleware_is_not_participating(self) -> None:
        session = _session()
        self.assertIn(
            "not mounted",
            session.middleware_participation_issues(["missing_hook"])[0],
        )

        session.register_middleware("broken_hook", "before_model")
        session.record_middleware_event("broken_hook", "invoked", iteration=0)
        session.record_middleware_event(
            "broken_hook", "error", iteration=0, error="boom"
        )
        issue = session.middleware_participation_issues(["broken_hook"])[0]
        self.assertIn("execution error", issue)

    def test_expected_middleware_names_come_from_materialized_agent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "agent.yaml"
            path.write_text('''
middlewares:
  - import: middlewares.enforce_diversification:GeneratedMiddleware
    params: {}
  - import: middlewares.budget_reminder:BudgetReminderMiddleware
    params: {}
''')
            self.assertEqual(
                _expected_generated_middlewares(path),
                ["enforce_diversification"],
            )




class GeneratedMiddlewareGateTest(unittest.TestCase):
    """Dict-return hooks: require_tools enforcement and malformed shapes."""

    def _stub_modules(self):
        class HookResult:
            @staticmethod
            def no_changes():
                return {"changed": False}

            @staticmethod
            def with_modifications(**kwargs):
                return {"changed": True, **kwargs}

        class Middleware:
            pass

        class Message:
            def __init__(self, role, content):
                self.role, self.content = role, content

        class Role:
            FRAMEWORK = "framework"

        class TextBlock:
            def __init__(self, text):
                self.text = text

        modules = {
            "nexau": types.ModuleType("nexau"),
            "nexau.archs": types.ModuleType("nexau.archs"),
            "nexau.archs.main_sub": types.ModuleType("nexau.archs.main_sub"),
            "nexau.archs.main_sub.execution": types.ModuleType(
                "nexau.archs.main_sub.execution"
            ),
            "nexau.archs.main_sub.execution.hooks": types.ModuleType(
                "nexau.archs.main_sub.execution.hooks"
            ),
            "nexau.core": types.ModuleType("nexau.core"),
            "nexau.core.messages": types.ModuleType("nexau.core.messages"),
        }
        hooks = modules["nexau.archs.main_sub.execution.hooks"]
        hooks.BeforeModelHookInput = object
        hooks.HookResult = HookResult
        hooks.Middleware = Middleware
        messages = modules["nexau.core.messages"]
        messages.Message = Message
        messages.Role = Role
        messages.TextBlock = TextBlock
        return modules

    def _materialize(self, root: Path, code: str):
        _build_custom_middlewares({"new_middlewares": [{
            "name": "probe_gate",
            "hook": "before_model",
            "implementation_py": code,
        }]}, root)
        path = root / "middlewares" / "probe_gate.py"
        spec = importlib.util.spec_from_file_location("generated_mw_gate", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module

    def test_require_tools_return_sets_the_session_gate(self) -> None:
        modules = self._stub_modules()
        previous = {name: sys.modules.get(name) for name in modules}
        sys.modules.update(modules)
        try:
            with tempfile.TemporaryDirectory() as td:
                code = (
                    "def before_model(hook_input):\n"
                    "    state = hook_input.get(\"state\", {})\n"
                    "    if state.get(\"iteration\", 0) >= 1:\n"
                    "        return {\"note\": \"probe first\","
                    " \"require_tools\": [\"probe_solution\"]}\n"
                    "    return None\n"
                )
                module = self._materialize(Path(td), code)
                session = _session()
                with session_scope(session):
                    middleware = module.GeneratedMiddleware()
                    middleware.before_model(SimpleNamespace(
                        current_iteration=0, messages=[]))
                    out = middleware.before_model(SimpleNamespace(
                        current_iteration=1, messages=[]))
                self.assertTrue(out["changed"])
                self.assertIsNotNone(session.tool_gate)
                self.assertEqual(session.tool_gate["require"], ("probe_solution",))
                audit = session.middleware_audit["probe_gate"]
                self.assertEqual(audit["fires"], 1)
                self.assertEqual(audit["errors"], 0)
                self.assertEqual(audit["gate"]["enforced"], 1)
        finally:
            for name, mod in previous.items():
                if mod is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = mod

    def test_unknown_dict_keys_are_hook_errors_without_effects(self) -> None:
        modules = self._stub_modules()
        previous = {name: sys.modules.get(name) for name in modules}
        sys.modules.update(modules)
        try:
            with tempfile.TemporaryDirectory() as td:
                code = (
                    "def before_model(hook_input):\n"
                    "    return {\"force_tool\": \"probe_solution\"}\n"
                )
                module = self._materialize(Path(td), code)
                session = _session()
                with session_scope(session):
                    middleware = module.GeneratedMiddleware()
                    out = middleware.before_model(SimpleNamespace(
                        current_iteration=0, messages=[]))
                self.assertFalse(out["changed"])
                self.assertIsNone(session.tool_gate)
                audit = session.middleware_audit["probe_gate"]
                self.assertEqual(audit["errors"], 1)
                self.assertIn("unknown hook-result keys", audit["last_error"])
        finally:
            for name, mod in previous.items():
                if mod is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = mod


if __name__ == "__main__":
    unittest.main()
