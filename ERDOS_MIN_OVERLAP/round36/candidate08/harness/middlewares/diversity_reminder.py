"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    templates_used = []
    for turn in history:
        tools = turn.get("tools_used", [])
        for t in tools:
            if t == "generate_step_function_template":
                templates_used.append(t)
    
    if len(templates_used) < 5:
        return f"Remember: You've only called generate_step_function_template {len(templates_used)} times. Generate more diverse templates (try: bipartite, multimodal_3peaks, golomb_ruler, sinusoidal_threshold, piecewise_constant) with different num_intervals (400, 800, 1600, 3200). Do not tune hyperparameters yet!"
    
    has_hyper_tuning = any("hyperparameter" in str(turn.get("tools_used", [])) for turn in history[-5:])
    if has_hyper_tuning and len(templates_used) < 7:
        return "You're tuning hyperparameters but haven't exhausted diverse templates. Finish generating 7 diverse templates with different num_intervals first!"
    
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
