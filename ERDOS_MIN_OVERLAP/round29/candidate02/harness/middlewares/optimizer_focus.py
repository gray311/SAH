"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    # Check if we've already run generate_optimizer_seeds
    has_generated_seeds = any(
        "generate_optimizer_seeds" in str(turn.get("tools_used", [])) 
        for turn in history
    )
    
    if not has_generated_seeds:
        return "First call: Call generate_optimizer_seeds to get 10 diverse latent-space initializations. Then run edit_solution+evaluate_solution on EACH (not just probe them)."
    
    # Check if we've started evaluating seeds
    num_evaluations = sum(
        1 for turn in history 
        if "evaluate_solution" in str(turn.get("tools_used", []))
    )
    
    if num_evaluations < 10:
        return f"You've only evaluated {num_evaluations}/10 seeds. Continue running the optimizer on remaining seeds - the 59000-step training is where improvement happens."
    
    # Check if we've finished seed evaluations
    if num_evaluations == 10:
        return "You've evaluated all 10 seeds. Pick the best combined_score. If all are <= 1.0, you may try hyperparameter tuning."
    
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
