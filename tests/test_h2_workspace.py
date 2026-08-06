from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from outer import h2_workspace as ws  # noqa: E402
from outer import harness_spec as hs  # noqa: E402
from outer.materialize import INNER_HARNESS, materialize  # noqa: E402
from outer.propose_session import ProposeSession  # noqa: E402


class H2WorkspaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base = hs.read_base_spec(INNER_HARNESS)

    def _materialize(self, root: Path, spec: dict | None = None) -> Path:
        effective = spec or self.base
        package = root / "h2"
        materialize(effective, package, meta={"effective": effective})
        return package

    def _add_tool(self, package: Path, name: str = "alpha_probe") -> None:
        agent_path = package / "agent.yaml"
        agent = yaml.safe_load(agent_path.read_text())
        agent["tools"].append({
            "name": name,
            "yaml_path": f"./tools/{name}.tool.yaml",
            "binding": "inner.harness.tools.custom_runtime:custom_tool",
            "extra_kwargs": {"py_path": f"./custom_tools/{name}.py"},
        })
        self.assertTrue(
            ws.write_file(
                package, "agent.yaml",
                yaml.safe_dump(agent, sort_keys=False, allow_unicode=True),
            ).startswith("WROTE")
        )
        schema = {
            "type": "tool",
            "name": name,
            "description": "Return a compact structural probe before editing.",
            "input_schema": {"type": "object", "properties": {}},
        }
        ws.write_file(
            package, f"tools/{name}.tool.yaml",
            yaml.safe_dump(schema, sort_keys=False),
        )
        ws.write_file(
            package, f"custom_tools/{name}.py",
            "def run(ctx, args):\n    return {'best': ctx.best_score()}",
        )
        prompt = (package / "prompt.md").read_text().rstrip()
        ws.write_file(
            package, "prompt.md",
            prompt + f"\n- `{name}`: call once to inspect the current search state.",
        )

    def _add_skill_and_middleware(self, package: Path) -> None:
        agent = yaml.safe_load((package / "agent.yaml").read_text())
        agent["skills"].append("./skills/ac2-search")
        agent["middlewares"].insert(0, {
            "import": "middlewares.diversity_guard:GeneratedMiddleware",
            "params": {},
        })
        ws.write_file(
            package, "agent.yaml",
            yaml.safe_dump(agent, sort_keys=False, allow_unicode=True),
        )
        ws.write_file(
            package, "skills/ac2-search/SKILL.md",
            "---\nname: ac2-search\n"
            "description: Search AC2 structures.\n---\n\n"
            "# AC2\nUse multiple representations.",
        )
        ws.write_file(
            package, "middlewares/diversity_guard.py",
            "def before_model(hook_input):\n"
            "    state = hook_input.get('state', {})\n"
            "    if state.get('family_streak', 0) >= 4:\n"
            "        return 'Switch family.'\n"
            "    return None",
        )
        ws.write_file(
            package, "middlewares/diversity_guard.middleware.yaml",
            "name: diversity_guard\n"
            "hook: before_model\n"
            "description: Force a family switch after a stall.",
        )
        prompt = (package / "prompt.md").read_text().rstrip()
        ws.write_file(
            package, "prompt.md",
            prompt
            + "\n- `ac2-search`: load when AC2 structure search stalls."
            + "\n- `diversity_guard`: automatic middleware requesting a family switch.",
        )

    def test_shell_feedback_starts_from_agent_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            package = self._materialize(Path(td))
            output = ws.inspect(package, "cat agent.yaml")
            self.assertIn("system_prompt: ./prompt.md", output)
            self.assertIn("tools:", output)
            self.assertIn("probe_solution", ws.inspect(package, "ls tools/"))
            self.assertIn("ERROR", ws.inspect(package, "cat ../outside"))

    def test_added_tool_requires_file_mount_and_prompt_then_is_submitted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            package = self._materialize(Path(td))
            self._add_tool(package)
            check = ws.validate_workspace(package, self.base)
            self.assertTrue(check.valid, check.errors)
            self.assertEqual(
                hs.generated_component_inventory(check.effective or {})["new_tools"],
                ["alpha_probe"],
            )
            self.assertIn("new_tools.alpha_probe", check.changed_fields)
            self.assertIn("system_prompt", check.changed_fields)

            session = ProposeSession(base_spec=self.base, draft_dir=package)
            self.assertIn(
                "system_prompt: ./prompt.md",
                session.inspect_harness("cat agent.yaml"),
            )
            session.inspect_harness("cat prompt.md")
            self.assertIn("VALID H2 WORKSPACE", session.validate_harness())
            self.assertIn("SUBMITTED", session.submit_harness())
            self.assertTrue(session.submitted)
            self.assertIn("new_tools", session.partial_spec or {})

    def test_unadvertised_or_orphan_tool_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            package = self._materialize(Path(td))
            self._add_tool(package)
            prompt = (package / "prompt.md").read_text()
            ws.write_file(
                package, "prompt.md",
                prompt.replace(
                    "- `alpha_probe`: call once to inspect the current search state.\n",
                    "",
                ),
            )
            check = ws.validate_workspace(package, self.base)
            self.assertFalse(check.valid)
            self.assertTrue(any("does not name" in err for err in check.errors))

            # If the files exist but agent.yaml does not mount them, they are
            # not silently accepted as proposed components either.
            agent = yaml.safe_load((package / "agent.yaml").read_text())
            agent["tools"] = [row for row in agent["tools"]
                              if row.get("name") != "alpha_probe"]
            ws.write_file(
                package, "agent.yaml",
                yaml.safe_dump(agent, sort_keys=False, allow_unicode=True),
            )
            check = ws.validate_workspace(package, self.base)
            self.assertFalse(check.valid)
            self.assertTrue(any("custom_tools files" in err for err in check.errors))

    def test_file_level_delete_is_explicit_and_does_not_reinherit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            first = self._materialize(root)
            self._add_tool(first)
            added = ws.validate_workspace(first, self.base)
            self.assertTrue(added.valid, added.errors)
            inherited = added.effective or {}

            second = root / "second"
            materialize(inherited, second, meta={"effective": inherited})
            agent = yaml.safe_load((second / "agent.yaml").read_text())
            agent["tools"] = [row for row in agent["tools"]
                              if row.get("name") != "alpha_probe"]
            ws.write_file(
                second, "agent.yaml",
                yaml.safe_dump(agent, sort_keys=False, allow_unicode=True),
            )
            ws.delete_file(second, "tools/alpha_probe.tool.yaml")
            ws.delete_file(second, "custom_tools/alpha_probe.py")
            prompt = (second / "prompt.md").read_text()
            ws.write_file(
                second, "prompt.md",
                prompt.replace(
                    "- `alpha_probe`: call once to inspect the current search state.\n",
                    "",
                ),
            )

            removed = ws.validate_workspace(second, inherited)
            self.assertTrue(removed.valid, removed.errors)
            self.assertEqual(
                (removed.partial or {}).get("remove_generated"),
                {"tools": ["alpha_probe"]},
            )
            self.assertEqual(
                hs.generated_component_inventory(removed.effective or {})["new_tools"],
                [],
            )

    def test_inherited_tool_skill_and_middleware_are_editable_in_place(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            first = self._materialize(root)
            self._add_tool(first)
            self._add_skill_and_middleware(first)
            added = ws.validate_workspace(first, self.base)
            self.assertTrue(added.valid, added.errors)
            inherited = added.effective or {}

            second = root / "second"
            materialize(inherited, second, meta={"effective": inherited})
            self.assertIn(
                "EDITED",
                ws.edit_file(
                    second,
                    "custom_tools/alpha_probe.py",
                    "return {'best': ctx.best_score()}",
                    "return {'best_v2': ctx.best_score()}",
                ),
            )
            self.assertIn(
                "EDITED",
                ws.edit_file(
                    second,
                    "skills/ac2-search/SKILL.md",
                    "Use multiple representations.",
                    "Probe and compare multiple representations.",
                ),
            )
            self.assertIn(
                "EDITED",
                ws.edit_file(
                    second,
                    "middlewares/diversity_guard.py",
                    "return 'Switch family.'",
                    "return 'Switch representation family now.'",
                ),
            )

            updated = ws.validate_workspace(second, inherited)
            self.assertTrue(updated.valid, updated.errors)
            self.assertEqual(updated.changed_fields, [
                "new_tools.alpha_probe",
                "new_skills.ac2-search",
                "new_middlewares.diversity_guard",
            ])
            self.assertEqual(
                hs.generated_component_inventory(updated.effective or {}),
                hs.generated_component_inventory(inherited),
            )

    def test_session_enforces_inspect_edit_validate_submit_order(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            package = self._materialize(Path(td))
            session = ProposeSession(base_spec=self.base, draft_dir=package)
            self.assertIn("first inspect", session.inspect_harness("ls tools/"))
            self.assertIn(
                "first inspect",
                session.write_harness_file(
                    "custom_tools/too_early.py", "def run(ctx, args): return {}"
                ),
            )
            self.assertIn(
                "first inspect",
                session.edit_harness_file(
                    "prompt.md", "Be decisive", "Be systematic"
                ),
            )
            session.inspect_harness("cat agent.yaml")
            self.assertIn(
                "read existing file first",
                session.edit_harness_file(
                    "prompt.md", "Be decisive", "Be systematic"
                ),
            )
            session.inspect_harness("cat prompt.md")
            self.assertIn(
                "EDITED",
                session.edit_harness_file(
                    "prompt.md", "Be decisive", "Be systematic"
                ),
            )
            self.assertIn(
                "requires a successful validate_harness",
                session.submit_harness(),
            )

            # A fresh session shows the successful path because submit_harness
            # is a stop tool: calling it too early correctly invalidates the
            # previous session.
            session = ProposeSession(base_spec=self.base, draft_dir=package)
            session.inspect_harness("cat agent.yaml")
            session.inspect_harness("cat prompt.md")
            self.assertIn("VALID H2 WORKSPACE", session.validate_harness())
            self.assertIn("Candidate H2 accepted", session.submit_harness())

    def test_legacy_parent_is_copied_but_only_proposer_can_repair_prompt(self) -> None:
        legacy = dict(self.base)
        legacy["system_prompt"] = "Legacy executor instructions without a catalog."
        with tempfile.TemporaryDirectory() as td:
            package = Path(td) / "h2"
            with self.assertRaisesRegex(ValueError, "proposer-owned system_prompt"):
                materialize(legacy, package, meta={"effective": legacy})

            materialize(
                legacy,
                package,
                meta={"effective": legacy},
                validate_prompt=False,
            )
            invalid = ws.validate_workspace(package, legacy)
            self.assertFalse(invalid.valid)
            self.assertTrue(any("does not name" in err for err in invalid.errors))

            catalog = hs.h2_component_catalog(legacy)
            repaired_prompt = (
                "Executor workflow.\nTools: " + ", ".join(catalog["tools"])
                + "\nSkills: " + ", ".join(catalog["skills"])
                + "\nMiddleware: " + ", ".join(catalog["middlewares"])
            )
            ws.write_file(package, "prompt.md", repaired_prompt)
            repaired = ws.validate_workspace(package, legacy)
            self.assertTrue(repaired.valid, repaired.errors)
            self.assertEqual(repaired.changed_fields, ["system_prompt"])

    def test_middleware_wrapper_edits_outside_user_hook_are_not_silently_lost(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            first = self._materialize(root)
            self._add_skill_and_middleware(first)
            added = ws.validate_workspace(first, self.base)
            self.assertTrue(added.valid, added.errors)
            inherited = added.effective or {}

            second = root / "second"
            materialize(inherited, second, meta={"effective": inherited})
            ws.edit_file(
                second,
                "middlewares/diversity_guard.py",
                '"""Generated middleware (h2spec/1.0), lifecycle-audited."""',
                '"""A proposer edit outside the user-hook region."""',
            )
            prompt = (second / "prompt.md").read_text().rstrip()
            ws.write_file(second, "prompt.md", prompt + "\nUse explicit diagnostics.")
            check = ws.validate_workspace(second, inherited)
            self.assertFalse(check.valid)
            self.assertTrue(
                any("outside its USER-HOOK region" in err for err in check.errors),
                check.errors,
            )


if __name__ == "__main__":
    unittest.main()
