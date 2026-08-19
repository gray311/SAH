"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get("tool_name", "")
    iteration = hook_input.get("iteration", 0)
    pattern_sources = hook_input.get("pattern_sources", [])
    probes_used = hook_input.get("probes_used", 0)
    
    if tool in ["edit_solution", "generate_candidates"]:
        unique_sources = set(pattern_sources)
        num_variants = hook_input.get("num_variants", 0)
        if num_variants >= 4 and len(unique_sources) < 2:
            return "DIVERSITY WARNING: Generate variants from at least 2 different pattern sources"
    
    if probes_used >= 15 and tool != "evaluate_solution":
        return "Budget pressure: You've used 15+ probes. Evaluate a promising variant soon."
    
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def before_tool(self, hook_input):
        try:
            note = before_tool(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
