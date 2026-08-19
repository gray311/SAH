"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    edit_count = state.get("edit_count", 0)
    if evals_left >= 3 and edit_count < 5:
        return (
            "You have evals left and haven't edited much.\\n"
            "Call generate_pattern_edit to get new pattern code.\\n"
            "Insert it into _get_best_initialization and edit the EVOLVE-BLOCK.\\n"
            "Don't waste evals on analytical screening.\\n"
            "Test concentrated peaks at centers 0.25, 0.5, 0.75, 1.25, 1.5, 1.75."
        )
    elif evals_left >= 1:
        return (
            f"{evals_left} eval left.\\n"
            "Edit to add a new pattern.\\n"
            "Or try a new pattern center value."
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
