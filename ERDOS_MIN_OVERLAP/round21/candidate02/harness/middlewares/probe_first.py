"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    evals_used = state.get("evals_used", 0)
    has_pending_edit = "pending_edit" in hook_input
    if evals_left >= 3 and not has_pending_edit:
        return (
            "You have 3+ evals left. Don't call evaluate_solution yet!\n"
            "First call analyze_h_structure to prototype structures.\n"
            "Only evaluate after analyzing and confirming c5 < 0.375.\n"
        )
    elif evals_left >= 1 and evals_used < 10:
        return (
            f"{evals_left} evals remaining. Use them wisely.\n"
            "Have you analyzed candidate structures with analyze_h_structure?\n"
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
