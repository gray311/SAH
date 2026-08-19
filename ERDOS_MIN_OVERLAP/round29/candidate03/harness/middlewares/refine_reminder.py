"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    if not history:
        return "First call: Use search_patterns to generate diverse candidates."
    
    # Check if we're about to evaluate without refinement
    last_action = history[-1].get("tool_used", "")
    if last_action == "search_patterns":
        return "You called search_patterns. Next: screen with probe_solution, then refine candidates with c5_bound < 0.375 using refine_candidate before evaluation."
    
    # Check if we're about to evaluate without refinement
    if last_action == "evaluate_solution":
        has_refined = any("refine_candidate" in str(t.get("tools_used", [])) for t in history[-3:])
        if not has_refined:
            return "WARNING: You're evaluating without refinement! Call refine_candidate 2-3 times on candidates with c5_bound < 0.375 first."
    
    # Check pattern usage
    pattern_count = sum(1 for t in history if "search_patterns" in str(t.get("tools_used", [])))
    if pattern_count >= 2 and last_action == "probe_solution":
        return "You've called search_patterns twice. It's okay to evaluate now if you've refined promising candidates."
    
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
