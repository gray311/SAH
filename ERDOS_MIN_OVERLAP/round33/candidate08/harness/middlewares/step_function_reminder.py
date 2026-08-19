"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    # Track if step_function_generator has been called
    has_step_gen = any(
        "step_function_generator" in str(turn.get("tools_used", []))
        for turn in history
    )
    
    # Track if we've tried multiple patterns
    patterns_tried = []
    for turn in history:
        used_tools = str(turn.get("tools_used", []))
        if "bipolar" in used_tools or "tripolar" in used_tools or "golomb" in used_tools:
            patterns_tried.append(used_tools)
    
    # If we haven't tried step function generator, remind
    if not has_step_gen and len(history) < 3:
        return (
            "FIRST TRY: Call step_function_generator with pattern_type=\"tripolar\"\n"
            "Generate 3-5 diverse step functions (bipolar, tripolar, golomb).\n"
            "Use probe_solution to screen for c5_bound < 0.382.\n"
            "Random sigmoids rarely work - use structural step functions!"
        )
    
    # If we've tried patterns but no evaluation yet, remind to evaluate
    elif len(patterns_tried) > 0 and has_step_gen:
        eval_count = sum(
            1 for turn in history
            if "evaluate_solution" in str(turn.get("tools_used", []))
        )
        if eval_count == 0:
            return (
                "You've generated step functions. NOW CALL evaluate_solution\n"
                "on the best candidate with c5_bound < 0.382."
            )
    
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
