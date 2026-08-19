"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    iteration = hook_input.get('iteration', 0)
    tool = hook_input.get('tool_name', '')
    evals_used = hook_input.get('evals_used', 0)
    best_combined = hook_input.get('best_combined_score', 1.042)

    if iteration > 5 and 'scan_pattern_variants' not in hook_input.get('tool_name', ''):
        return 'Reminder: Call scan_pattern_variants to explore seed''s 12 step patterns—this unlocks the hidden search space.'

    if iteration >= 10 and evals_used >= 15 and 'step' in tool.lower():
        return 'Warning: You''ve spent 15+ evals on step patterns without beating seed. Switch to Gaussian/Spline families now.'

    if evals_used >= 25 and best_combined <= 1.042:
        return 'Budget alert: Only 5 evals left. Submit best or try multi-family hybrids.'

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
