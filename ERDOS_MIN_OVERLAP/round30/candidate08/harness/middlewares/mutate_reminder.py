"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    # Check if we've called search_patterns
    has_patterns = any("search_patterns" in str(turn.get("tools_used", [])) for turn in history)
    
    if not has_patterns:
        return "First call: Use search_patterns to generate 5 diverse patterns."
    
    # Check if we've identified and mutated the best pattern
    has_mutate = any("mutate_best_pattern" in str(turn.get("tools_used", [])) for turn in history)
    has_evaluate = any("evaluate_solution" in str(turn.get("tools_used", [])) for turn in history)
    
    if has_patterns and not has_mutate:
        return "You've called search_patterns but haven't called mutate_best_pattern. Find the best pattern and call mutate_best_pattern to create refined variants."
    
    if has_mutate and not has_evaluate:
        return "You've called mutate_best_pattern but haven't evaluated any variants. Use probe_solution to screen, then evaluate the best candidate with c5_bound < 0.375."
    
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
