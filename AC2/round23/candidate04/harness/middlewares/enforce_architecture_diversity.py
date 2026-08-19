"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    edit_history = hook_input.get('edit_history', [])
    
    # Track last edit architecture
    if tool == 'edit_solution' and iteration > 5 and len(edit_history) >= 1:
        # Check if last edit was parameter tweak
        last_edit = edit_history[-1] if edit_history else ''
        if 'pattern_idx' in last_edit or 'height' in last_edit or 'start' in last_edit:
            return 'Warning: Last edit was parameter tweak. Generate a NEW architecture (polynomial/spline) with edit_solution!'
    
    if iteration >= 15 and len(edit_history) < 2:
        return 'Stalled alert: Iteration 15+ with only one edit type. Call edit_solution for a NEW function family (polynomial/spline)!'
    
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
