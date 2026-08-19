"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    last_eval = history[-1] if history else None
    
    if last_eval:
        last_action = last_eval.get("action", "")
        if last_action == "evaluate_solution":
            probes_remaining = hook_input.get("budget_left", {}).get("probes", 0)
            if probes_remaining > 2:
                return "Reminder: You just did a full evaluation. Before making your next edit, consider probing with probe_solution first to filter candidates cheaply. You have {} probes left.".format(probes_remaining)
    
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
