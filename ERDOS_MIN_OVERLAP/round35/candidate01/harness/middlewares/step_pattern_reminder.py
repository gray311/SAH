"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    # Early game: remind to use step_function_builder
    if len(history) <= 3:
        return "Start by calling step_function_builder with pattern=bipartite_left to create a simple step function with integral=1."
    
    # Check if step_function_builder was used
    has_builder = any("step_function_builder" in str(turn.get("tools_used", [])) for turn in history)
    if not has_builder:
        return "You have not used step_function_builder yet. Call it to generate step function code directly."
    
    # If used bipartite, suggest trying other patterns
    used_bipartite = any("bipartite_left" in str(turn.get("tools_used", [])) or "bipartite_right" in str(turn.get("tools_used", [])) for turn in history)
    if used_bipartite and len(history) <= 10:
        return "You have tried bipartite patterns. Next, try step_function_builder with pattern=two_plateaus_left for a tri-partite function."
    
    # If exhausted bipartite, suggest alternating
    if len(history) > 15:
        return "Consider trying alternating patterns: step_function_builder(pattern=alternating) to spread the on-regions."
    
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
