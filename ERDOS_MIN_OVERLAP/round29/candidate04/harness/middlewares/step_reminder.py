"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    if not history:
        return "First call: USE discrete_step_search to generate true step functions before gradient optimization."
    
    # Check if discrete_step_search has been called in this run
    has_steps = any("discrete_step_search" in str(turn.get("tools_used", [])) for turn in history)
    if not has_steps:
        return "Reminder: You have not yet called discrete_step_search. Call it to generate true step functions before tuning hyperparameters."
    
    # Check if we've exhausted discrete_step_search (2 max)
    step_count = sum(1 for turn in history if "discrete_step_search" in str(turn.get("tools_used", [])))
    if step_count >= 2:
        return "You've called discrete_step_search twice. Now it's okay to use gradient optimization, but prioritize evaluating the best step function candidates first."
    
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
