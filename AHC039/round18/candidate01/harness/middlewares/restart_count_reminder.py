"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def after_model(hook_input):
    if hook_input is None:
        return None
    # After model generates some code, remind to do more restarts if not done
    return "If < 30 restarts done, expand to 35 restarts to exhaust search budget."
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def after_model(self, hook_input):
        try:
            note = after_model(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
