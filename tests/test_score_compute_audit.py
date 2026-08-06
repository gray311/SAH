import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_score_compute_sota5 import (
    HUMAN_BEST_REFERENCE,
    TASKS,
    audit_endpoint_validation,
    audit_human_best_reference,
)
from scripts.audit_clean5_publishable import (
    ROUTES as CLEAN5_ROUTES,
    SERIES as CLEAN5_SERIES,
    TASKS as CLEAN5_TASKS,
    audit_endpoint_validation as audit_clean5_endpoint_validation,
    audit_route_update_isolation,
)
from scripts.collect_sota7_sacct_snapshot import requested_jobs
from scripts.collect_clean5_sacct_snapshot import is_zero_allocation_submission


class EndpointValidationAuditTest(unittest.TestCase):
    def test_clean5_route_update_isolation_fails_on_missing_context_brief(self):
        tasks = {}
        audit_tasks = {}
        for task in CLEAN5_TASKS:
            tasks[task] = {
                "series": {
                    "proposer_full": {"points": [
                        {"round": 1, "analyzer_model_calls": 0}
                    ]},
                    "context": {"points": [
                        {
                            "round": 1,
                            "analyst_briefs": 0,
                            "analyzer_model_calls": 0,
                            "analyzer_specialists": [],
                        },
                        {
                            "round": 2,
                            "analyst_briefs": 1,
                            "analyzer_model_calls": 2,
                            "analyzer_specialists": [
                                "performance", "design"
                            ],
                        },
                    ]},
                    "executor": {"points": [
                        {"step": 0}
                    ]},
                }
            }
            audit_tasks[task] = {"costs": {
                "proposer": {"analyzer_calls": 0},
                "context": {
                    "weight_updates": 0,
                    "planned_optimizer_boundaries": 0,
                    "analyzer_briefs": 1,
                    "analyzer_calls": 2,
                },
                "executor": {
                    "harness_proposals": 0,
                    "analyzer_calls": 0,
                },
            }}
        view = {"tasks": tasks}
        full_audit = {"tasks": audit_tasks}
        result = audit_route_update_isolation(view, full_audit)
        self.assertEqual(
            result["status"],
            "all_five_routes_match_declared_update_targets",
        )

        first = CLEAN5_TASKS[0]
        tasks[first]["series"]["context"]["points"][1].update({
            "analyst_briefs": 0,
            "analyzer_model_calls": 0,
            "analyzer_specialists": [],
        })
        with self.assertRaisesRegex(AssertionError, "analyzer briefs"):
            audit_route_update_isolation(view, full_audit)

    def test_cancelled_before_allocation_is_retained_as_zero_cost(self):
        row = {
            "state": "CANCELLED by 158198",
            "start": "None",
            "elapsed_seconds_sacct": 0,
            "allocated_gpus_sacct": 0,
            "allocated_gpu_hours_sacct": 0.0,
        }
        self.assertTrue(is_zero_allocation_submission(row))
        self.assertFalse(is_zero_allocation_submission({
            **row, "elapsed_seconds_sacct": 1
        }))
        self.assertFalse(is_zero_allocation_submission({
            **row, "state": "COMPLETED"
        }))

    def test_clean5_validation_binds_final_endpoint_and_program(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            view_path = root / "view.json"
            cases_path = root / "cases.json"
            result_path = root / "results.json"
            cases = []
            results = {}
            tasks = {}
            for task_index, task in enumerate(CLEAN5_TASKS, start=1):
                tasks[task] = {
                    "series": {},
                    "endpoint_revalidation": {},
                }
                for route_index, route in enumerate(CLEAN5_ROUTES, start=1):
                    score = float(task_index * 10 + route_index)
                    program_sha = hashlib.sha256(
                        f"{task}::{route}".encode()
                    ).hexdigest()
                    case_id = f"{task}::{route}"
                    case = {
                        "case_id": case_id,
                        "task": task,
                        "method": route,
                        "reported_curve_endpoint_score": score,
                        "program_sha256": program_sha,
                    }
                    result = {
                        **case,
                        "reported_endpoint_inside_revalidation_range": True,
                    }
                    cases.append(case)
                    results[case_id] = result
                    tasks[task]["series"][CLEAN5_SERIES[route]] = {
                        "points": [{"x": 1, "score": score}]
                    }
                    tasks[task]["endpoint_revalidation"][route] = result
            view_path.write_text(json.dumps({"tasks": tasks}))
            cases_path.write_text(json.dumps({
                "source_plot_data": str(view_path),
                "source_plot_data_sha256_at_collection": hashlib.sha256(
                    view_path.read_bytes()
                ).hexdigest(),
                "cases": cases,
            }))
            result_path.write_text(json.dumps({
                "status": "complete",
                "all_runs_valid": True,
                "requested_runs": 5,
                "source_cases": str(cases_path),
                "source_cases_sha256": hashlib.sha256(
                    cases_path.read_bytes()
                ).hexdigest(),
                "case_results": results,
            }))
            (root / "CANONICAL_COMPLETE").touch()

            audited = audit_clean5_endpoint_validation(result_path, view_path)
            self.assertTrue(
                audited[
                    "all_final_view_endpoints_and_programs_bound_to_validation"
                ]
            )

            view = json.loads(view_path.read_text())
            first_task = CLEAN5_TASKS[0]
            view["tasks"][first_task]["series"]["proposer_full"]["points"][-1][
                "score"
            ] += 0.1
            view_path.write_text(json.dumps(view))
            with self.assertRaisesRegex(
                AssertionError, "final plotted endpoint changed"
            ):
                audit_clean5_endpoint_validation(result_path, view_path)

    def test_human_reference_is_standalone_and_tamper_evident(self):
        frozen = json.loads(HUMAN_BEST_REFERENCE.read_text())
        payload = {
            "anchors": {
                task: [0.0, frozen["tasks"][task][
                    "human_best_combined_score"
                ]]
                for task in TASKS
            }
        }
        audited = audit_human_best_reference(payload)
        self.assertEqual(
            audited["status"],
            "all_y_equals_one_values_match_frozen_human_references",
        )
        self.assertEqual(set(audited["tasks"]), set(TASKS))

        payload["anchors"][TASKS[0]][1] += 1e-4
        with self.assertRaisesRegex(
            AssertionError, "plotted y=1 reference is not the frozen"
        ):
            audit_human_best_reference(payload)

    def test_incomplete_endpoint_validation_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plot = root / "plot_data.json"
            plot.write_text("{}")
            cases = root / "cases.json"
            cases.write_text(json.dumps({"source_plot_data": str(plot)}))
            result = root / "results.json"
            result.write_text(json.dumps({
                "status": "partial",
                "all_runs_valid": True,
                "requested_runs": 5,
                "source_cases": str(cases),
                "source_cases_sha256": hashlib.sha256(cases.read_bytes()).hexdigest(),
                "case_results": {},
            }))

            partial = audit_endpoint_validation(
                result, plot, require_complete=False
            )
            self.assertEqual(partial["status"], "partial")
            self.assertEqual(partial["cases_present"], 0)
            self.assertEqual(partial["cases_expected"], 21)
            with self.assertRaisesRegex(
                AssertionError, "endpoint validation is not complete"
            ):
                audit_endpoint_validation(result, plot, require_complete=True)

    def test_sacct_snapshot_includes_whole_excluded_campaigns(self):
        audit = {
            "compute_timing_proxy": {
                route: {"jobs": ([{"job": "10", "role": "outer"}]
                                  if route == "proposer" else [])}
                for route in ("proposer", "context", "executor")
            },
            "operational_retry_costs": {
                "timing": {
                    route: {"jobs": ([{"job": "11", "role": "outer"}]
                                      if route == "proposer" else [])}
                    for route in ("proposer", "context", "executor")
                }
            },
            "analysis_required_rejection_costs": {"timing": {"jobs": []}},
            "excluded_campaign_costs": {
                "timing": {
                    "proposer": {"jobs": [
                        {"job": "12", "role": "outer"},
                        {"job": "13", "role": "train"},
                    ]},
                    "context": {"jobs": []},
                    "executor": {"jobs": []},
                }
            },
        }
        roles = requested_jobs(audit)
        self.assertEqual(set(roles), {"10", "11", "12", "13"})
        self.assertEqual(
            roles["13"], ["excluded_campaign:proposer:train"]
        )


if __name__ == "__main__":
    unittest.main()
