"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    probes_left = state.get("probes_left", 0)
    evals_left = state.get("evals_left", 0)
    
    if probes_left > 10 and (evals_left > 3 or "simple" not in hook_input.get("last_action", "")):
        return (
            "NOTICE: You have many probes left. HAVE YOU TRIED SIMPLE 2-3 SEGMENT STEP FUNCTIONS YET?\\n"
            "Before optimizing 800-interval functions, create and test simple piecewise functions using create_piecewise_init.\\n"
            "Use num_intervals=10-20 for simple functions, not 800.\\n"
            "Only after exhausting all simple candidates should you try the seed optimizer."
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
