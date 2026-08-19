"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get("current_code", "")
    recent_tool_calls = hook_input.get("recent_tool_calls", [])
    
    # Check if analyze_step_patterns was called recently
    analyzed = False
    for call in recent_tool_calls[-3:]:  # Check last 3 calls
        if "analyze_step_patterns" in call.get("tool", ""):
            analyzed = True
            break
    
    if not analyzed:
        return "CALL analyze_step_patterns FIRST to understand your function's step structure before editing. This tool analyzes heights, widths, symmetry and recommends improvements."
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
