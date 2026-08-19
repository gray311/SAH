"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    last_score = hook_input.get("last_score")
    evaluations_left = hook_input.get("evaluations_left", 999)
    
    reminder = None
    if evaluations_left > 5 and last_score is not None:
        reminder = f"EVALUATIONS LEFT: {evaluations_left}. Use probe_solution to rank variants before calling evaluate_solution! Each full eval costs 1 of your limited budget."
    elif evaluations_left <= 5:
        reminder = f"URGENT: Only {evaluations_left} evaluations left! Use probe_solution extensively before final evaluations."
    
    return reminder
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
