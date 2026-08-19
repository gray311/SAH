"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    current_tool = hook_input.get("current_tool", "")
    if current_tool == "evaluate_solution":
        # Check if we've just edited
        history = hook_input.get("history", [])
        recent_edits = [h for h in history[-3:] if h.get("action") == "edit"]
        if len(recent_edits) >= 1:
            # Check how many probes we've used recently (if available)
            # For now, just add a gentle reminder
            return " REMINDER: Before full evaluation, consider generating 2-3 variants and using probe_solution to rank them. Only evaluate the top candidate."
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
