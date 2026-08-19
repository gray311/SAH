"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    score = hook_input.get("current_score")
    if score is None or score <= 1.0:
        return "CRITICAL: Seed gradient-descent trapped at 0.999641. DO NOT use it. Instead: construct step functions via patterns A-E (single pulse, two pulses, three-level, bimodal, center). Enumerate combinatorial heights. Test 5-20 candidates. Start n=50, refine n=800. Optimal is SIMPLE STRUCTURED PATTERN. Use construct_step_function or enumerate_heights tools."
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
