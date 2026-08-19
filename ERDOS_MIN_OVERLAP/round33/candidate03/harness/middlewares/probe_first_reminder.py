"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    last_turn = history[-1] if history else None
    
    if last_turn is None:
        return "First turn: Use step_function_generator to create a step function, then probe_solution to screen."
    
    tools_used = str(last_turn.get("tools_used", []))
    
    if "evaluate_solution" in tools_used and "probe_solution" not in tools_used:
        return "You just called evaluate_solution without probing first. Use probe_solution to screen candidates before full evaluation."
    
    if "step_function_generator" not in tools_used:
        return "You haven't called step_function_generator yet. Use it to construct step functions from templates."
    
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
