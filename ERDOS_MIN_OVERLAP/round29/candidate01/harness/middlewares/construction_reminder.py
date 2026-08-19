"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    has_construction = any(
        "construct_bipartite" in str(turn.get("tools_used", [])) or
        "construct_multipeak" in str(turn.get("tools_used", [])) or
        "construct_sparse" in str(turn.get("tools_used", []))
        for turn in history
    )
    if not has_construction:
        return "Reminder: Use construct_bipartite, construct_multipeak, or construct_sparse to generate step functions with integral=1 before tuning hyperparameters."
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
