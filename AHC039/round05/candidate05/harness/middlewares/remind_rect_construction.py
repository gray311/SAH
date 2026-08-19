"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    best_score = hook_input.get("best_score", 0)
    if iteration == 0:
        return "START: Call analyze_fish_distribution first, then build a 4-vertex rectangle around mackerel bounds. Format: count then 'x y' pairs."
    elif iteration % 5 == 0:
        return "REMEMBER: Try a fresh 4-vertex rectangle. Output: 'm', then 'x1 y1', 'x2 y2', 'x3 y3', 'x4 y4' for axis-aligned rectangle vertices."
    elif best_score < 300:
        return "LOW SCORE: Simplify to a bounding rectangle. Don't overcomplicate."
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
