"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    # Check if we've already done bipartite search
    has_bipartite = any("bipartite_searcher" in str(turn.get("tools_used", [])) for turn in history)
    
    if not has_bipartite:
        return "REMINDER: Start with bipartite_searcher to generate bipartite step function candidates. This is your best chance at beating the current record!"
    
    # Check if we've probed all bipartite candidates
    has_probed = any("probe_solution" in str(turn.get("tools_used", [])) for turn in history)
    if has_bipartite and not has_probed:
        return "REMINDER: You've generated bipartite candidates. CALL probe_solution on all of them before full evaluation!"
    
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
