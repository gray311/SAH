"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    current_iter = hook_input.get("iteration", 0)
    if current_iter % 2 == 0 or current_iter < 10:
        return "Use COARSE discretization (n=20-50) with MULTIPLE seeds. Do NOT use n=800 yet. Save best coarse results for refinement later."
    elif current_iter < 25:
        return "Vary the structural pattern each iteration (bimodal, plateau, periodic, Golomb, random). Save diverse variants."
    else:
        return "Refine best coarse winner to n=200-400 intervals. Use shorter optimization cycles to explore alternatives."
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
