"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    best_score = state.get("best_score", 1.029)
    used_step_config = state.get("used_step_config", False)
    used_pattern_mutation = state.get("used_pattern_mutation", False)
    
    # Phase 1: iterations 0-2, explore with step_config_generator
    if iteration <= 2:
        if used_pattern_mutation:
            return "WARNING: Don't use pattern_mutation_tool yet. Phase 1 (exploration) should use step_config_generator first."
    
    # Phase 2: iteration 3+ or score > 1.030, refine with pattern_mutation_tool
    if iteration >= 3 or best_score > 1.030:
        if not used_pattern_mutation:
            return "PROMPT: Phase 2 ready. Use pattern_mutation_tool to mutate seed patterns (0-13). They're near-optimal - we need to fine-tune them."
        if used_step_config:
            return "PROMPT: Consider switching to Phase 2. You've explored new configs. Try pattern_mutation_tool to fine-tune seed patterns (0-13)."
    
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
