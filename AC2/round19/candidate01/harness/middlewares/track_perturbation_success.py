"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def after_tool(hook_input):
    tool_name = hook_input.get("tool_name", "")
    result = hook_input.get("result", {})
    score = result.get("score", result.get("combined_score", 0))
    
    # If evaluation succeeded, remind about tracking
    if score > 1.0 and tool_name == "evaluate_solution":
        return "Great! Track which perturbation (height/width/pos change) achieved this score. Reuse it in next iteration."
    
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
