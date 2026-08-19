"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    has_template = any(
        "generate_step_function_template" in str(turn.get("tools_used", []))
        for turn in history
    )
    
    if not has_template:
        return "IMPORTANT: Call generate_step_function_template first to create concrete step functions (three_peak, bipartite, golomb, broad_plateau) before hyperparameter tuning. These satisfy integral(h)=1 exactly."
    
    template_count = sum(
        1 for turn in history
        if "generate_step_function_template" in str(turn.get("tools_used", []))
    )
    
    if template_count >= 3:
        return "Generated 3+ templates. Now probe and evaluate. Keep c5_bound < 0.382."
    
    if template_count == 2:
        return "Generated 2 templates. Generate one more, then probe all."
    
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
