"""Submit-reminder middleware for H1.

From ``remind_from_iteration`` on, if the proposer has not yet submitted a
spec, append a bounded framework message urging it to validate + submit before
the iteration cap — an un-submitted run is an invalid candidate (minimum
reward). Fails open: any error resolves to no-changes.
"""
from __future__ import annotations

from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput,
    HookResult,
    Middleware,
)
from nexau.core.messages import Message, Role, TextBlock

from outer.harness.tools.runtime import get_session


class SubmitReminderMiddleware(Middleware):
    def __init__(self, *, remind_from_iteration: int = 6, max_iterations: int = 8) -> None:
        self.remind_from_iteration = int(remind_from_iteration)
        self.max_iterations = int(max_iterations)

    def before_model(self, hook_input: BeforeModelHookInput) -> HookResult:
        try:
            session = get_session()
            iteration = int(hook_input.current_iteration)
        except Exception:
            return HookResult.no_changes()
        if session.submitted or iteration < self.remind_from_iteration:
            return HookResult.no_changes()
        left = max(0, self.max_iterations - iteration)
        text = (f"Only ~{left} turn(s) left and no spec submitted yet. Finalize now: "
                "validate_spec your best draft, then submit_spec it. An un-submitted "
                "run scores the minimum reward.")
        return HookResult.with_modifications(messages=[
            *hook_input.messages,
            Message(role=Role.FRAMEWORK, content=[TextBlock(text=text)]),
        ])
