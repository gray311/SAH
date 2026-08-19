"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get('code', '')
    import re
    # Check for large seed range
    seed_ranges = re.findall(r'range\(\d+, (\d+)\)', code)
    if seed_ranges:
        seed_count = int(seed_ranges[-1]) - int(seed_ranges[0])
        if seed_count > 100:
            return f"\U0001F6A8 WARNING: {seed_count} seeds is TOO MANY! Each eval will timeout.\n\
            MUST use 3-5 seeds max. With 20 evals total, you need fast evaluations.\n\
            Implement 4 construction strategies (Paley, Random, Perturbed, Alt) in parallel instead."
    # Check for 500 seeds
    if '500' in code or 'range(4000, 4500)' in code:
        return "\U0001F6A8 ERROR: 500 seeds violates the new strategy! Use 3-5 seeds.\n\
            Implement parallel construction testing instead of massive seed sweep.\n\
            Each eval must complete in < 20 seconds."
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
