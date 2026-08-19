"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    last_action = hook_input.get('last_action', '')
    
    if last_action == 'evaluate_solution' or 'evaluate_solution' in last_action:
        return "✅ Good! You evaluated. Next step: BEFORE next evaluate, you MUST probe 2-3 variants with probe_solution to rank them cheaply."
    elif last_action == 'edit_solution' and 'block_mutation' not in last_action and 'mutation' not in last_action:
        return "💡 Tip: Consider adding block_mutation_scramble to escape potential local optima, especially if score < 0.50."
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
