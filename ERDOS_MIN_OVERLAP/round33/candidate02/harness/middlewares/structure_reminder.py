"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    if not history:
        return "FIRST: Call step_function_generator with pattern='bipartite' to create a simple threshold function. Don't start with random latents."
    
    # Check if we've only tried random/init patterns
    has_structured = any("step_function_generator" in str(turn.get("tools_used", [])) for turn in history)
    
    if not has_structured:
        return "Reminder: You haven't called step_function_generator yet. Try generating structured step functions (bipartite, multi_peak, or golomb) before tuning hyperparameters."
    
    # If we've only called it once, encourage trying more patterns
    count = sum(1 for turn in history if "step_function_generator" in str(turn.get("tools_used", [])))
    if count == 1:
        return "You've called step_function_generator once. Try other patterns: 'multi_peak' with 2-4 peaks, or 'golomb' for sparse marks."
    
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
