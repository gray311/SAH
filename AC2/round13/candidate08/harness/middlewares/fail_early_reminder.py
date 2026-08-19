"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def after_tool(hook_input):
    tool_name = hook_input.get("tool_name", "")
    score = hook_input.get("score", None)
    iteration = hook_input.get("iteration", 0)
    combined_score = hook_input.get("combined_score", None)
    
    # If evaluation failed or scored poorly, remind to discard
    if tool_name == "evaluate_solution":
        if combined_score is not None and combined_score < 1.02:
            return "DISCARD: This variant scored " + str(combined_score) + ", below the threshold of 1.02. Do NOT refine this failed architecture further. Either try a different proposal from this family or SWITCH TO A COMPLETELY NEW FAMILY immediately. You have 30 evals - spread them across multiple architectures."
    
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def after_tool(self, hook_input):
        try:
            note = after_tool(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
