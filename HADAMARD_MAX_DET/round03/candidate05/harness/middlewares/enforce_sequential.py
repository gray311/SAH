"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    evals_left = hook_input.get('evals_left', 20)
    evals_used = hook_input.get('evals_used', 0)
    current_best_score = hook_input.get('current_best_score', 0)
    
    reminder = None
    
    # Remind to seed from previous best
    if evals_used < 20:
        reminder = f"⚠️ REMINDER: Evaluation {evals_used + 1} of {20}. MUST seed from previous best result. Do NOT start fresh. Use ONE method (Paley or Random) to convergence. If no previous best available, use Paley construction." 
    
    # Remind about probe before evaluate
    if evals_left > 0:
        reminder += f"\n🔍 REMINDER: Call probe_solution on 2-3 parameter variants BEFORE calling evaluate_solution. Use probe budget wisely (30 total)." 
    
    # Plateau warning
    if evals_used >= 6:
        reminder += f"\n📊 Progress check: {evals_used} evaluations done. If last 3 had <1% improvement, analyze_plateau tool to consider method switch." 
    
    return reminder
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
