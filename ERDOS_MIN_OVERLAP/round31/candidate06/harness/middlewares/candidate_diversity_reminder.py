"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    # Check if generate_candidates has been called recently
    gen_candidates_count = sum(1 for t in history if "generate_candidates" in str(t.get("tools_used", [])))
    
    if gen_candidates_count == 0:
        return "First call: CALL generate_candidates to create diverse step function candidates before evaluating anything."
    
    if gen_candidates_count >= 1:
        return "You've called generate_candidates. Now CALL probe_solution to screen the candidates."
    
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
