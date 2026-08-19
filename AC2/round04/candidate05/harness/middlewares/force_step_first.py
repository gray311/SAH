"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    step_tried = state.get("step_tried", False)
    family = state.get("current_family", "")
    if iteration < 3 and not step_tried and "step" not in family.lower():
        return "STEP_FUNCTION_REQUIRED: The current record (0.8963) is achieved by step functions. You must implement a step function variant before exploring other families. Start with: single step 0.25n-0.75n height=1.0, or multi-level 3 segments."
    probes_used = state.get("probes_used", 0)
    if probes_used < 5 and iteration > 0:
        return "PROBE_REMINDER: You've only used {} probes. Test 3-5 step function variants with probe_solution before using evaluate_solution.".format(probes_used)
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
