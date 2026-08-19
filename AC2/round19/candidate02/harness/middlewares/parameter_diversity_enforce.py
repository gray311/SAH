"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    history = hook_input.get("parameter_history", [])
    current = hook_input.get("current_params", {})
    
    # If same 3 params for 5+ iterations, warn
    if len(history) >= 5:
        recent = history[-5:]
        params_frequent = []
        for param in ['num_intervals', 'learning_rate', 'num_steps', 
                     'reinit_fraction', 'reinit_std']:
            counts = sum(1 for h in recent if param in h)
            if counts >= 3:
                params_frequent.append(param)
        
        if len(params_frequent) >= 3:
            return f"Warning: Repeating {params_frequent} frequently. Try varying other hyperparameters."
    
    # Remind to analyze at regular intervals
    if iteration == 0 or iteration % 8 == 0:
        return "Reminder: Call analyze_optimizer_params to know current hyperparameters before editing."
    
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
