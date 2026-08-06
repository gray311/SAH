"""Per-run proposer session and candidate-isolated H2 filesystem.

Mirrors inner/session.py: the propose driver sets the active session in a
contextvar for the duration of one H1 agent run; the tool bindings and the
submit-reminder middleware resolve it via get_session(). Thread-safe: each
proposer thread runs in its own context.
"""
from __future__ import annotations

import contextvars
import shlex
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from outer import harness_spec as hs
from outer import h2_workspace as h2ws


@dataclass
class ProposeSession:
    base_spec: Dict[str, Any]
    draft_dir: Optional[Path] = None
    validations: int = 0
    submitted: bool = False
    raw_submission: str = ""
    partial_spec: Optional[Dict[str, Any]] = None
    effective: Optional[Dict[str, Any]] = None
    changed_fields: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    file_events: List[Dict[str, str]] = field(default_factory=list)
    agent_yaml_inspected: bool = False
    inspected_files: Set[str] = field(default_factory=set)
    workspace_revision: int = 0
    validated_revision: Optional[int] = None
    component_audit: List[Dict[str, Any]] = field(default_factory=list)
    _validated_check: Optional[h2ws.WorkspaceCheck] = field(default=None, repr=False)

    def _check(self, spec_yaml: str):
        v = hs.parse_and_validate(spec_yaml)
        if not v.valid:
            return None, None, [], v.errors
        eff = hs.merge_with_base(v.spec, self.base_spec)
        differs, changed = hs.differs_from_base(eff, self.base_spec)
        if not differs:
            return v.spec, eff, [], ["spec is identical to the current harness (no-op)"]
        prompt_errors = hs.component_prompt_issues(eff)
        if prompt_errors:
            return v.spec, eff, changed, prompt_errors
        return v.spec, eff, changed, []

    def validate(self, spec_yaml: str) -> str:
        self.validations += 1
        _, _, changed, errors = self._check(spec_yaml)
        if errors:
            return "INVALID:\n- " + "\n- ".join(errors)
        return ("VALID. This spec changes: " + ", ".join(changed) +
                ". You can refine further or submit_spec now.")

    def submit(self, spec_yaml: str) -> str:
        self.submitted = True
        self.raw_submission = spec_yaml
        spec, eff, changed, errors = self._check(spec_yaml)
        if errors:
            self.errors = errors
            return "SUBMITTED but INVALID (minimum reward):\n- " + "\n- ".join(errors)
        self.partial_spec, self.effective, self.changed_fields = spec, eff, changed
        return f"SUBMITTED. Candidate spec accepted; changes: {', '.join(changed)}."

    def _require_draft(self) -> Path:
        if self.draft_dir is None:
            raise RuntimeError("this proposer session has no H2 file workspace")
        return Path(self.draft_dir)

    def inspect_harness(self, command: str) -> str:
        try:
            argv = shlex.split(command)
        except ValueError:
            argv = []
        is_agent_cat = (
            len(argv) == 2
            and argv[0] == "cat"
            and Path(argv[1]).as_posix().lstrip("./") == "agent.yaml"
        )
        if not self.agent_yaml_inspected and not is_agent_cat:
            return (
                "ERROR: first inspect the actual mount graph with "
                '`harness_shell(command="cat agent.yaml")`.'
            )
        output = h2ws.inspect(self._require_draft(), command)
        if not output.startswith("ERROR:") and len(argv) == 2 and argv[0] == "cat":
            try:
                relative = h2ws.relative_path(
                    self._require_draft(), argv[1], must_exist=True
                )
                self.inspected_files.add(relative)
                if relative == "agent.yaml":
                    self.agent_yaml_inspected = True
            except ValueError:
                pass
        self.file_events.append({"operation": "inspect", "target": command})
        return output

    def _require_read_before_existing_edit(self, path: str) -> Optional[str]:
        if not self.agent_yaml_inspected:
            return (
                "ERROR: first inspect the actual mount graph with "
                '`harness_shell(command="cat agent.yaml")`.'
            )
        try:
            relative = h2ws.relative_path(
                self._require_draft(), path, must_exist=False
            )
            exists = (self._require_draft() / relative).exists()
        except ValueError as exc:
            return f"ERROR: {exc}"
        if exists and relative not in self.inspected_files:
            return (
                f"ERROR: read existing file first with "
                f'`harness_shell(command="cat {relative}")`.'
            )
        return None

    def _record_mutation(self, output: str) -> None:
        if not output.startswith("ERROR:"):
            self.workspace_revision += 1
            self.validated_revision = None
            self._validated_check = None
            self.component_audit = []

    def write_harness_file(self, path: str, content: str) -> str:
        blocked = self._require_read_before_existing_edit(path)
        if blocked:
            return blocked
        output = h2ws.write_file(self._require_draft(), path, content)
        self._record_mutation(output)
        self.file_events.append({"operation": "write", "target": path,
                                 "result": output})
        return output

    def edit_harness_file(self, path: str, old_text: str, new_text: str) -> str:
        blocked = self._require_read_before_existing_edit(path)
        if blocked:
            return blocked
        output = h2ws.edit_file(
            self._require_draft(), path, old_text, new_text
        )
        self._record_mutation(output)
        self.file_events.append({"operation": "edit", "target": path,
                                 "result": output})
        return output

    def delete_harness_file(self, path: str) -> str:
        blocked = self._require_read_before_existing_edit(path)
        if blocked:
            return blocked
        output = h2ws.delete_file(self._require_draft(), path)
        self._record_mutation(output)
        self.file_events.append({"operation": "delete", "target": path,
                                 "result": output})
        return output

    def _check_workspace(self) -> h2ws.WorkspaceCheck:
        return h2ws.validate_workspace(self._require_draft(), self.base_spec)

    def validate_harness(self) -> str:
        self.validations += 1
        if not self.agent_yaml_inspected:
            return (
                "INVALID H2 WORKSPACE:\n- agent.yaml was not inspected; start "
                'with harness_shell(command="cat agent.yaml")'
            )
        if "prompt.md" not in self.inspected_files:
            return (
                "INVALID H2 WORKSPACE:\n- prompt.md was not inspected; read the "
                "executor system prompt before validating H2"
            )
        check = self._check_workspace()
        self.component_audit = list(check.component_audit)
        if not check.valid:
            return "INVALID H2 WORKSPACE:\n- " + "\n- ".join(check.errors)
        self.validated_revision = self.workspace_revision
        self._validated_check = check
        return (
            "VALID H2 WORKSPACE. Changes: "
            + ", ".join(check.changed_fields)
            + ". You may refine files further or call submit_harness."
        )

    def submit_harness(self) -> str:
        self.submitted = True
        if self.validated_revision != self.workspace_revision:
            self.errors = [
                "submit_harness requires a successful validate_harness after "
                "the most recent file edit"
            ]
            return "SUBMITTED but INVALID (minimum reward):\n- " + self.errors[0]
        # Reuse the exact validated object: submit_harness is atomic and never
        # invokes a reviewer or rewrites component bytes after H1 stops.
        check = self._validated_check
        if check is None:
            self.errors = ["validated workspace result is missing"]
            return "SUBMITTED but INVALID (minimum reward):\n- " + self.errors[0]
        if not check.valid:
            self.errors = check.errors
            return "SUBMITTED but INVALID (minimum reward):\n- " + "\n- ".join(
                check.errors
            )
        self.partial_spec = check.partial
        self.effective = check.effective
        self.changed_fields = check.changed_fields
        self.component_audit = list(check.component_audit)
        self.raw_submission = yaml.safe_dump(
            check.partial, sort_keys=False, allow_unicode=True, width=100
        ).strip()
        return (
            "SUBMITTED. Candidate H2 accepted; changes: "
            + ", ".join(check.changed_fields)
            + "."
        )


_CURRENT: "contextvars.ContextVar[Optional[ProposeSession]]" = contextvars.ContextVar(
    "propose_session", default=None
)


def get_session() -> ProposeSession:
    s = _CURRENT.get()
    if s is None:
        raise RuntimeError("no active ProposeSession (tool called outside propose_scope)")
    return s


@contextmanager
def propose_scope(session: ProposeSession):
    token = _CURRENT.set(session)
    try:
        yield session
    finally:
        _CURRENT.reset(token)
