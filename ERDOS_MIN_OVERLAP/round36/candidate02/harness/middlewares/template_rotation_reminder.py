"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    distinct_templates = set()
    for turn in history:
        code = turn.get("code_changed", "")
        if "bipartite" in code.lower():
            distinct_templates.add("bipartite")
        if "dual_peaks" in code.lower() or "two" in code.lower():
            distinct_templates.add("dual_peaks")
        if "tri_modal" in code.lower() or "three" in code.lower():
            distinct_templates.add("tri_modal")

    if len(distinct_templates) < 3:
        templates_tried = list(distinct_templates)
        remaining = ["bipartite", "dual_peaks", "tri_modal", "boundary_peak", "golomb_ruler"]
        not_tried = [t for t in remaining if t not in templates_tried]
        if not_tried:
            return f"You've only tried {len(templates_tried)} template types: {templates_tried}. Try a different structure: {not_tried[0]}."
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
