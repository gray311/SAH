"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get('state', {})
    evals_left = state.get('evals_left', 0)
    probes_left = state.get('probes_left', 30)
    if evals_left >= 5 and probes_left >= 10:
        return '5+ evals, 10+ probes: Generate 50 discrete candidates. Probe all. Evaluate top 3-5.'
    elif evals_left >= 3:
        return f'{evals_left} evals left. Probe before full evaluation. Seek c5_bound < 0.35.'
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
