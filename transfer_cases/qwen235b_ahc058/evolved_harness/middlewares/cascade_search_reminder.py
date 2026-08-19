"""Generated middleware (h2spec/1.0), lifecycle-audited."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock
from inner.harness.middleware.generated_context import GeneratedHookTracker
from inner.harness.tools.runtime import get_session

# --USER-HOOK-START--
def before_model(hook_input):
    return (
        "Current apple count: use action_analyzer to prune to top 20 actions.\n"
        "Then search with 100-turn lookahead and SMART policy:\n"
        "- apples < 1000: prioritize level 0\n"
        "- 1000 <= apples < 100000: invest in level 3 if affordable\n"
        "- apples >= 100000: balance level 3 and level 0\n"
        "NEVER use 25-turn lookahead or simple greedy without cascade awareness.\n"
        "Use probe_solution to rank before full evaluation."
    )
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def __init__(self):
        self._name = 'cascade_search_reminder'
        self._hook = 'before_model'
        self._tracker = GeneratedHookTracker()
        self._reported_errors = set()
        try:
            get_session().register_middleware(self._name, self._hook)
        except Exception:
            # The rollout-level participation check will report a mount failure.
            pass

    def _audit(self, text):
        try:
            get_session().history_note("[middleware:" + 'cascade_search_reminder' + "] " + str(text)[:320])
        except Exception:
            pass

    def _ensure_registered(self):
        try:
            session = get_session()
            row = session.middleware_audit.get(self._name)
            if row is None or int(row.get("mounts", 0)) < 1:
                session.register_middleware(self._name, self._hook)
        except Exception:
            pass

    def _record(self, event, iteration, error=None):
        # AgentConfig may instantiate middleware before session_scope starts.
        # Retry registration lazily on the first real hook invocation.
        self._ensure_registered()
        try:
            get_session().record_middleware_event(
                self._name, event, iteration=iteration, error=error)
        except Exception:
            pass

    def before_model(self, hook_input):
        iteration = int(getattr(hook_input, "current_iteration", 0) or 0)
        self._record("invoked", iteration)
        try:
            context = self._tracker.snapshot(hook_input, get_session())
            result = before_model(context)
        except Exception as exc:
            self._record("error", iteration, error=str(exc))
            key = (type(exc).__name__, str(exc)[:200])
            if key not in self._reported_errors:
                self._reported_errors.add(key)
                self._audit("ERROR " + key[0] + ": " + key[1])
            return HookResult.no_changes()
        if not result:
            return HookResult.no_changes()
        # The hook stays a pure function.  It may return either an advisory
        # note (str) or a dict {"note": str?, "require_tools": [tool, ...]?}.
        # The trusted wrapper applies effects; malformed shapes are hook
        # errors, never silent no-ops.
        note = None
        require_tools = None
        if isinstance(result, dict):
            unknown = set(result) - {"note", "require_tools"}
            if unknown:
                self._record("error", iteration,
                             error="unknown hook-result keys: " + repr(sorted(unknown)))
                self._audit("ERROR unknown hook-result keys " + repr(sorted(unknown)))
                return HookResult.no_changes()
            note = result.get("note")
            require_tools = result.get("require_tools")
        else:
            note = result
        fired = False
        if require_tools:
            try:
                get_session().request_tool_gate(self._name, require_tools)
                fired = True
                self._audit("ENFORCED iteration=" + str(iteration)
                            + " require_tools=" + repr(list(require_tools)))
            except Exception as exc:
                self._record("error", iteration, error=str(exc))
                self._audit("ENFORCE_ERROR " + type(exc).__name__ + ": " + str(exc)[:200])
                return HookResult.no_changes()
        if not note and not fired:
            return HookResult.no_changes()
        try:
            if fired:
                self._record("fired", iteration)
            if note:
                if not fired:
                    self._record("fired", iteration)
                self._audit("FIRED iteration=" + str(context.get("iteration", 0))
                            + " note=" + str(note)[:180])
                messages = getattr(hook_input, "messages", None)
                if messages is not None:
                    msg = Message(role=Role.FRAMEWORK,
                                  content=[TextBlock(text=str(note)[:2000])])
                    return HookResult.with_modifications(messages=[*messages, msg])
                # Tool-hook inputs have no conversation messages in NexAU.
                # The advisory is still lifecycle-audited, while the trusted
                # tool gate (when requested by the hook) is applied above.
                return HookResult.no_changes()
            return HookResult.no_changes()
        except Exception as exc:
            self._record("error", iteration, error=str(exc))
            self._audit("EMIT_ERROR " + type(exc).__name__ + ": " + str(exc)[:200])
            return HookResult.no_changes()
