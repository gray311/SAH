"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    patterns_explored = hook_input.get('patterns_explored', 0)
    
    # Early iterations: force pattern exploration
    if iteration < 8 and patterns_explored < 5:
        return f'Early iteration {iteration}: Explore new pattern_idx values! You have only tried {patterns_explored} patterns. Call probe_new_pattern with a new pattern_idx.'
    
    # Mid iterations: continue exploring if limited
    if iteration < 20 and patterns_explored < 10:
        return f'Mid iteration {iteration}: Consider trying new pattern_idx values. You have explored {patterns_explored} patterns.'
    
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
