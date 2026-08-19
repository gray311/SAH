"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    edit = hook_input.get("last_edit", "")
    
    if "num_intervals" in edit:
        old_val = hook_input.get("last_edit_details", "")
        if "800" in old_val or "500" in old_val:
            return "Found fine grid (500-800 intervals). Change to COARSE grid (20-40 intervals) for step functions!"
    
    if "sigmoid" in edit.lower() or "sigmoid" in hook_input.get("last_state", ""):
        return "You're using sigmoid (smooth curves). Switch to HARD step functions (0, 0.5, 1.0) for true step functions."
    
    if hook_input.get("evals_left", 10) > 5:
        return "You have 5+ evals left. Try generate_step_functions with grid_size=30 to find step functions quickly."
    
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
