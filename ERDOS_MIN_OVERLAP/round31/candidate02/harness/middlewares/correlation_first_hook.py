"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    recent_calls = [str(turn.get("tools_used", [])) for turn in history[-3:]]
    
    has_correlation = any("get_correlation_profile" in s for s in recent_calls)
    has_targeted = any("targeted_h_optimizer" in s for s in recent_calls)
    
    if has_correlation and not has_targeted:
        return "You've called get_correlation_profile but haven't yet used targeted_h_optimizer. Call targeted_h_optimizer to generate mutations based on the correlation analysis."
    
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
