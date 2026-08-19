"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    import re
    code = hook_input.get('code', '')
    # Check for multiple construction methods (budget killer)
    if re.search(r'(Paley|random|perturbed|Hadamard\(\s*28\s*\))', code, re.IGNORECASE):
        methods_found = len(re.findall(r'\b(Paley|random|perturbed|Hadamard)\b', code, re.IGNORECASE))
        if methods_found >= 2:
            return "WARNING: Too many construction methods detected. This will exceed 350s budget. Use ONLY Paley construction with simulated annealing refinement (50k iters, 3 seeds). Maximum: ONE method + refinement."
        if methods_found >= 3:
            return "CRITICAL ERROR: 3 or more methods will definitely timeout. Use SINGLE construction (Paley) + SA refinement only."
    # Check iteration count
    iters = re.findall(r'(\d{4,6})\s*(iter|it)?', code)
    if iters:
        total = sum(int(i[0]) for i in iters[:3])
        if total > 150000:
            return "WARNING: >150k iterations likely exceeds budget. Reduce to 50k iterations with 3 seeds (total 150k flips max)."
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
