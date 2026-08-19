"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    if not history:
        return "First call: Use search_patterns to generate diverse initializations."
    
    # Check if we've used search_patterns
    has_patterns = any("search_patterns" in str(turn.get("tools_used", [])) for turn in history)
    
    if not has_patterns:
        return "Reminder: Call search_patterns FIRST to generate diverse initializations before refining."
    
    # Check if we have a candidate to refine
    if has_patterns and not any("explore_neighbors" in str(turn.get("tools_used", [])) for turn in history):
        return "You've generated patterns. Consider using explore_neighbors to refine the best candidate before hyperparameter tuning."
    
    # Check if we've exhausted refinement strategies
    pattern_count = sum(1 for turn in history if "search_patterns" in str(turn.get("tools_used", [])))
    neighbor_count = sum(1 for turn in history if "explore_neighbors" in str(turn.get("tools_used", [])))
    
    if pattern_count >= 2 and neighbor_count >= 4:
        return "You've exhausted pattern generation and refinement. Now you can try hyperparameter tuning."
    
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
