"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    probes_used = state.get("probes_used", 0)
    last_tool = state.get("last_tool", "")
    
    if probes_used < 2 and evals_left >= 3:
        return (
            "You have 3+ evals left and only used 1-2 probes.\n"
            "CALL jump_to_pattern with different structures (two-level, three-level, golomb).\n"
            "Evaluate 3-4 candidates with c5 < 0.36.\n"
        )
    elif evals_left >= 2:
        return (
            f"{evals_left} evals left. Use them to evaluate jump_to_pattern results.\n"
            "Look for c5 < 0.35 for full evaluation.\n"
        )
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def before_model(self, hook_input):
        try:
            note = before_model(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
