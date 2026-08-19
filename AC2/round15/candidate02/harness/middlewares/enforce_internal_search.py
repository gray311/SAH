"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool_name = hook_input.get("tool_name", "")
    
    if tool_name == "evaluate_solution":
        return "WARNING: Calling evaluate_solution without prior local_search_optimizer? " \
               "This wastes evaluation budget! Use local_search_optimizer first to probe variants."
    
    if tool_name == "probe_solution" and "local_search_optimizer" not in hook_input.get("call_history", ""):
        return "Remember: probe_solution should be used within local_search_optimizer for variant ranking."
    
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def before_tool(self, hook_input):
        try:
            note = before_tool(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
