"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    iteration = hook_input.get('iteration', 0)
    tool = hook_input.get('tool_name', '')
    last_pattern = hook_input.get('last_sampled_pattern', '')
    
    if tool == 'edit_solution' and last_pattern:
        # Warn if editing same pattern repeatedly
        if 'Mutation' not in hook_input.get('edit_description', ''):
            return 'Warning: Editing same pattern? Sample a new pattern from sample_step_patterns instead of tiny tweaks.'
    
    if iteration >= 10 and last_pattern:
        # After 10 iterations, encourage new pattern sampling
        return 'Iteration 10+: Consider sampling a fresh step pattern to avoid local optima.'
    
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
