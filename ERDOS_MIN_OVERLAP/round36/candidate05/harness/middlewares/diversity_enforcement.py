"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    if len(history) == 0:
        return "First call: Generate 5-10 diverse initializations by varying SEED PATTERN PARAMETERS (thresholds, peak positions, spacings). Do NOT call analysis tools. Use num_intervals=100 for speed." 
    last_turn = history[-1]
    tools_used = last_turn.get("tools_used", [])
    if "evaluate_solution" in tools_used or "probe_solution" in tools_used:
        return "You evaluated without generating diverse candidates first! Generate 3-5 new pattern variations with different parameters before evaluating."
    if "probe_solution" in tools_used:
        return "You probed without checking integral constraint! For each candidate, verify integral(h) = 1 by computing sum(h) * dx where dx = 2.0/num_intervals. Adjust by scaling h if needed."
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
