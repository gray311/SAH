"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get('code', '')
    strategies = []
    if 'paley' in code.lower() or 'quadratic' in code.lower() or 'residues' in code.lower():
        strategies.append('paley-based')
    if 'random' in code.lower() and 'random.choice' in code.lower():
        strategies.append('random-init')
    
    if len(strategies) < 2:
        return "🚨 CRITICAL: You MUST test at least 2 different base constructions per evaluation! Current approaches (Paley-only) have failed to improve the score. Include: Paley+perturbation AND random initialization, or other variants."
    
    import re
    seeds = re.findall(r'perturbation_seed[\s=:]+\d+', code)
    if not seeds:
        return "⚠️ WARNING: Ensure perturbation_seed varies between evaluations. Use values like 0, 100, 200, 300, 400 for different runs."
    
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
