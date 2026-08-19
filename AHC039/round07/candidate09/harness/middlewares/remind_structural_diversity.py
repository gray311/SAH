"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    eval_num = hook_input.get('iteration', 0)
    eval_total = hook_input.get('max_iterations', 60)
    
    approaches = [
        "Try a base bounding box variant",
        "Try bite-out variants near top sardine clusters",
        "Try multi-rectangular shape for separated mackerel clusters",
        "Try stepped polygon following density contours",
        "Try a different bite-out position on left/right/bottom/top edge",
        "Try combining bite-out with stepped edges",
    ]
    
    approach = approaches[eval_num % len(approaches)]
    return f"STRUCTURAL DIVERSITY REMINDER: This is evaluation {eval_num+1}/{eval_total}. Try {approach}. Do NOT just perturb edge positions - create a structurally different polygon."
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
