"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    if not history:
        return "Start with construct_step_function: generate threshold, symmetric, and two_threshold candidates. Probe all, evaluate the best."
    
    last_turn = history[-1]
    tools_used = last_turn.get("tools_used", [])
    
    if "construct_step_function" not in tools_used:
        return "Reminder: Use construct_step_function to generate complete step function candidates. Don't try to analyze the current solution first."
    
    if len(history) > 1:
        prev_turn = history[-2]
        if "construct_step_function" not in prev_turn.get("tools_used", []) and "probe_solution" not in prev_turn.get("tools_used", []) and "evaluate_solution" not in prev_turn.get("tools_used", []):
            return "You haven't generated any candidates yet. Call construct_step_function first to create step function programs."
    
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
