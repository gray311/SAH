"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    history = hook_input.get("history", [])
    current_turn = history[-1] if history else {}
    tools_used = current_turn.get("tools_used", [])
    
    if "evaluate_solution" in tools_used and "structural_analyzer" not in tools_used:
        return "WARNING: You are about to call evaluate_solution without calling structural_analyzer first. This may produce candidates with invalid constraints (integral(h)!=1 or h outside [0,1]). Call structural_analyzer first to verify constraints!"
    
    if "evaluate_solution" in tools_used and tools_used.count("structural_analyzer") < tools_used.count("evaluate_solution"):
        return "REMINDER: Call structural_analyzer once per evaluation to verify constraint satisfaction."
    
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
