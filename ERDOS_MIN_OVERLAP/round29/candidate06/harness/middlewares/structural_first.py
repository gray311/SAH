"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get('history', [])
    
    # Count how many times we've tried structural mutation vs hyperparameter tuning
    structural_count = 0
    hp_count = 0
    
    for turn in history:
        tools_used = turn.get('tools_used', [])
        if 'mutate_h_structure' in str(tools_used):
            structural_count += 1
        if 'edit_solution' in str(tools_used):
            hp_count += 1
    
    # If we've done hyperparameter tuning but not structural mutation, remind
    if hp_count > structural_count:
        return 'WARNING: You have tuned hyperparameters but haven\'t tried structural mutations yet. Structural changes are more likely to escape local optima. Call mutate_h_structure first.'
    
    # If we've done 2 structural searches but no evaluation, remind
    if structural_count >= 2:
        eval_count = sum(1 for turn in history if 'evaluate_solution' in str(turn.get('tools_used', [])))
        if eval_count == 0:
            return 'You have called mutate_h_structure twice but haven\'t evaluated any candidates. Call evaluate_solution on the best candidates from mutate_h_structure results.'
    
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
