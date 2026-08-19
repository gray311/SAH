"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    text = hook_input.get("text", "")
    
    # Check if agent is trying smooth functions
    if any(word in text.lower() for word in ['gaussian', 'b-spline', 'spline', 'oscillatory', 'smooth', 'gauss']):
        return "STOP: Smooth functions UNDERPERFORM. Step functions create sharp convolution peaks and beat the record. Generate step patterns instead."
    
    # Remind about probe usage
    if iteration > 5 and "probe_solution" not in text:
        return "Reminder: Call probe_solution to rank multiple step patterns before full evaluation. Use all 30 probes efficiently."
    
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
