"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_strategy = state.get("last_strategy", "unknown")
    strategy_counts = state.get("strategy_counts", {})
    
    if last_strategy != "unknown":
        strategy_counts[last_strategy] = strategy_counts.get(last_strategy, 0) + 1
        state["strategy_counts"] = strategy_counts
    
    if iteration >= 5 and last_strategy in strategy_counts:
        count = strategy_counts[last_strategy]
        if count >= 3:
            return "WARNING: You have used " + last_strategy + " " + str(count) + " times. Try a DIFFERENT approach now! The seed's gradient-based optimization is stuck. Try evolutionary search, coarse-to-fine, or alternative representations."
    
    if iteration <= 2 and "evolutionary" not in state.get("strategies_tried", ""):
        strategies_tried = state.get("strategies_tried", [])
        strategies_tried.append("evolutionary")
        state["strategies_tried"] = strategies_tried
        return None
    
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
