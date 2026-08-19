"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    prog = hook_input.get("program", "")
    # Check if program has time-based loop
    has_timer = "timer" in prog.lower() or "chrono" in prog.lower()
    has_loop = "while" in prog.lower() and "for" in prog.lower()
    has_search = "swap" in prog.lower() or "hill" in prog.lower() or "candidate" in prog.lower()
    if not (has_timer and (has_loop or has_search)):
        return "ADD a time-based search loop with vertex modifications (swap/add/remove). The evaluator REQUIRES active search, not static polygons."
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
