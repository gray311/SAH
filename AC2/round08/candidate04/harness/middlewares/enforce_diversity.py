"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_family = state.get("last_family", "")
    step_count = state.get("step_exploration_count", 0)
    
    # After 5 iterations of step exploration, force new family
    if iteration >= 5 and last_family == "step" and step_count > 2:
        return "FORCE: You've been exploring step functions too long. The seed already optimized those. Call generate_function_candidate with family='spline' or family='mixture' to try a completely different approach."
    
    # Track step exploration
    if last_family in ["step", "analyze_step"]:
        step_count += 1
        state["step_exploration_count"] = step_count
    
    # Warn if only using probes without variety
    used_families = set(state.get("explored_families", []))
    if len(used_families) <= 1 and iteration > 10:
        missing = set(["spline", "mixture", "hybrid"]) - used_families
        return "DIVERSITY ALERT: You've only tried " + str(len(used_families)) + " function family(ies). Try " + missing.pop() + " next! Call generate_function_candidate with family='" + missing.pop() + "'"
    
    if last_family == "generate_function_candidate":
        state["last_family"] = last_family
        if "family" in hook_input.get("args", {}):
            state["explored_families"] = state.get("explored_families", []) + [hook_input["args"]["family"]]
    
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
