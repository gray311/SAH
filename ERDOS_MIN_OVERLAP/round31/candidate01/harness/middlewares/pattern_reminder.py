"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    if not history:
        return "First call: USE search_patterns to generate 5 diverse initializations before tuning hyperparameters."
    
    # Check if search_patterns has been called in this run
    has_patterns = any("search_patterns" in str(turn.get("tools_used", [])) for turn in history)
    if not has_patterns:
        return "Reminder: You have not yet called search_patterns. Call it to generate diverse initial step functions before tuning hyperparameters."
    
    # Check if we've exhausted search_patterns (2 max)
    pattern_count = sum(1 for turn in history if "search_patterns" in str(turn.get("tools_used", [])))
    if pattern_count >= 2:
        return "You've called search_patterns twice. Now it's okay to tune hyperparameters, but prioritize evaluating the best pattern candidates first."
    
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
