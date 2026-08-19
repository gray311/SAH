"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    remaining = hook_input.get("budget_left", {}).get("evals", 0)
    best_score = hook_input.get("best_score", 0.999641)
    
    if remaining > 5:
        return (f"💡 STRATEGY REMINDER: You have {remaining} evaluations left.\n"
                f"Best score so far: {best_score:.6f} (need > 1.0 for record).\n\n"
                f"**Do NOT rely on gradient descent alone.** Use `construct_candidate`\n"
                f"to generate 3-5 diverse step functions:\n"
                f"- construct_candidate(100, \"uniform\")\n"
                f"- construct_candidate(100, \"concentrated\")\n"
                f"- construct_candidate(200, \"symmetric\")\n"
                f"- construct_candidate(50, \"multi_step\", 4)\n\n"
                f"Evaluate each, pick best, then optionally refine. "
                f"Stop when combined_score > 1.0.")
    else:
        return (f"⏰ BUDGET ALERT: Only {remaining} evaluations left!\n\n"
                f"Focus on the BEST 2-3 candidates from your constructions.\n"
                f"Submit immediately if combined_score > 1.0.")
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
