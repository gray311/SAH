#!/usr/bin/env python3
"""Fail-closed audit for one completed Adaptive V1 round."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from outer import harness_spec as hs  # noqa: E402
from protocols import adaptive_v1  # noqa: E402
from protocols.adaptive_v1_analysis import (  # noqa: E402
    analysis_package_hash,
    validate_analysis_brief,
)
from protocols.adaptive_v1_controller import (  # noqa: E402
    controller_package_hash,
)
from protocols.adaptive_v1_provenance import (  # noqa: E402
    runtime_package_hash,
)

AUDIT_VERSION = "adaptive-round-audit/1.5-bounded-evaluator"


def _audit_source_hash() -> str:
    return "sha256:" + hashlib.sha256(
        Path(__file__).resolve().read_bytes()
    ).hexdigest()[:16]


def _require(condition: Any, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _load(path: Path) -> Any:
    return json.loads(path.read_text())


def _write_failure_report(root: Path, report: Mapping[str, Any]) -> Path:
    """Never destroy a prior successful audit during a diagnostic rerun."""
    canonical = root / "artifact_audit_complete.json"
    target = canonical
    if canonical.exists():
        try:
            previous = _load(canonical)
        except (OSError, json.JSONDecodeError):
            previous = {}
        if previous.get("ok") is True or (
            previous.get("phase") == "complete" and not previous.get("error")
        ):
            target = root / "artifact_audit_failed_rerun.json"
    target.write_text(
        json.dumps({**dict(report), "report_path": str(target)}, indent=2)
    )
    return target


def _walk(nodes: Iterable[Mapping[str, Any]]):
    for node in nodes:
        yield node
        yield from _walk(node.get("children") or [])


def _assistant_calls(trajectory: Iterable[Mapping[str, Any]]) -> int:
    return sum(
        str(message.get("role", "")).lower().endswith("assistant")
        for message in trajectory
    )


def _custom_tool_calls(result: Mapping[str, Any]) -> Counter[str]:
    builtins = {
        "LoadSkill",
        "edit_solution",
        "evaluate_solution",
        "probe_solution",
        "finish",
    }
    calls: Counter[str] = Counter()
    for message in result.get("trajectory") or []:
        if not isinstance(message, Mapping):
            continue
        for block in message.get("content") or []:
            if not isinstance(block, Mapping) or block.get("type") != "tool_use":
                continue
            name = str(block.get("name") or "")
            if name and name not in builtins:
                calls[name] += 1
    return calls


def _training_spec_yaml(response: Any) -> str:
    match = re.search(
        r"<parameter=spec_yaml>\s*(.*?)\s*</parameter>",
        str(response or ""),
        flags=re.DOTALL,
    )
    _require(match is not None, "training response has no spec_yaml parameter")
    return match.group(1)


def _same_floats(left: Iterable[Any], right: Iterable[Any]) -> bool:
    left_values = [float(item) for item in left]
    right_values = [float(item) for item in right]
    return len(left_values) == len(right_values) and all(
        math.isclose(a, b, rel_tol=0.0, abs_tol=1e-12)
        for a, b in zip(left_values, right_values)
    )


def _validate_analysis_mode(
    analysis_meta: Mapping[str, Any],
) -> tuple[str, str, bool]:
    source = str(analysis_meta.get("source", ""))
    synthesis = str(analysis_meta.get("synthesis", ""))
    team_analysis = (
        analysis_meta.get("valid") is True
        and source == "nexau_subagent_team"
        and synthesis in {"coordinator_json", "deterministic_subagent_merge"}
    )
    grounded_fallback = (
        analysis_meta.get("valid") is False
        and source == "deterministic_fallback"
        and synthesis == "deterministic_dossier_fallback"
        and bool(analysis_meta.get("errors"))
    )
    _require(
        team_analysis or grounded_fallback,
        "invalid analysis source/synthesis contract",
    )
    return source, synthesis, grounded_fallback


def _dossier_evidence_references(value: Any) -> set[str]:
    references: set[str] = set()
    if isinstance(value, Mapping):
        if value.get("evidence_id"):
            references.add(str(value["evidence_id"]))
        for child in value.values():
            references.update(_dossier_evidence_references(child))
    elif isinstance(value, list):
        for child in value:
            references.update(_dossier_evidence_references(child))
    return references


def _validate_dossier_reference_closure(
    dossier: Mapping[str, Any],
) -> set[str]:
    contract = dossier.get("analysis_contract")
    contract = contract if isinstance(contract, Mapping) else {}
    _require(
        contract.get("evidence_reference_closure") is True,
        "analysis dossier does not declare evidence-reference closure",
    )
    raw_known = contract.get("known_evidence_ids")
    _require(
        isinstance(raw_known, list),
        "analysis dossier known_evidence_ids must be a list",
    )
    known = {str(item) for item in raw_known}
    _require(
        len(known) == len(raw_known),
        "analysis dossier contains duplicate known evidence IDs",
    )
    raw_evidence = dossier.get("evidence")
    _require(
        isinstance(raw_evidence, list),
        "analysis dossier evidence must be a list",
    )
    evidence_ids = {
        str(item["evidence_id"])
        for item in raw_evidence
        if isinstance(item, Mapping) and item.get("evidence_id")
    }
    _require(
        len(evidence_ids) == len(raw_evidence),
        "analysis dossier evidence rows need unique nonempty IDs",
    )
    _require(
        evidence_ids == known,
        "analysis dossier known IDs do not match groundable evidence rows",
    )
    referenced = _dossier_evidence_references(dossier)
    _require(
        referenced <= known,
        "analysis dossier contains ungroundable evidence references: "
        f"{sorted(referenced - known)}",
    )
    return known


def _validate_package(path: Path) -> dict[str, int]:
    from nexau import AgentConfig

    candidate = (path / "spec.yaml").exists()
    required = [path / "agent.yaml"]
    if candidate:
        required.extend(
            path / name
            for name in (
                "prompt.md",
                "spec.yaml",
                "tools",
                "skills",
                "middlewares",
                "meta.json",
            )
        )
    missing = [str(item) for item in required if not item.exists()]
    _require(not missing, f"incomplete NexAU package {path}: {missing}")
    if candidate:
        parsed = hs.parse_and_validate((path / "spec.yaml").read_text())
        _require(parsed.valid, f"invalid h2spec in {path}: {parsed.errors}")
    for module_name in list(sys.modules):
        if module_name == "middlewares" or module_name.startswith(
            "middlewares."
        ):
            sys.modules.pop(module_name, None)
    sys.path.insert(0, str(path))
    try:
        AgentConfig.from_yaml(path / "agent.yaml")
    finally:
        sys.path.pop(0)
        for module_name in list(sys.modules):
            if module_name == "middlewares" or module_name.startswith(
                "middlewares."
            ):
                sys.modules.pop(module_name, None)
    if not candidate:
        return {"tools": 0, "skills": 0, "middlewares": 0}
    effective = _load(path / "meta.json").get("effective") or {}
    return {
        "tools": len(effective.get("new_tools") or []),
        "skills": len(effective.get("new_skills") or []),
        "middlewares": len(effective.get("new_middlewares") or []),
    }


def verify_collected_audits(
    status_path: Path,
    *,
    out_dir: Path,
    round_base: int,
) -> dict[str, Any]:
    """Gate resume/training on source-matched audits for collected rounds."""
    status = _load(Path(status_path))
    expected = {
        "h1_package_hash": adaptive_v1.h1_package_hash(),
        "analysis_package_hash": analysis_package_hash(),
        "controller_package_hash": controller_package_hash(),
        "runtime_package_hash": runtime_package_hash(),
        "audit_source_hash": _audit_source_hash(),
    }
    verified = []
    for protocol_round in status.get("collected_rounds") or []:
        protocol_round = int(protocol_round)
        artifact_round = int(round_base) + protocol_round
        path = (
            Path(out_dir)
            / f"round{artifact_round:03d}"
            / "artifact_audit_complete.json"
        )
        _require(
            path.exists(),
            f"collected Adaptive round lacks successful audit: {path}",
        )
        report = _load(path)
        _require(
            report.get("schema") == "sah.adaptive-v1-round-audit/1"
            and report.get("ok") is True
            and int(report.get("protocol_round", -1)) == protocol_round
            and int(report.get("artifact_round", -1)) == artifact_round
            and int(report.get("max_evals", -1)) == 20,
            f"invalid/stale Adaptive round audit: {path}",
        )
        for field, value in expected.items():
            _require(
                report.get(field) == value,
                f"Adaptive audit/source mismatch {field}: {path}",
            )
        live = audit_round(
            path.parent,
            expected_max_evals=20,
            verify_current_hash=True,
        )
        _require(
            live.get("ok") is True,
            f"live Adaptive round re-audit failed: {path.parent}",
        )
        verified.append(str(path))
    return {
        "schema": "sah.adaptive-v1-campaign-audit-gate/1",
        "ok": True,
        "verified_rounds": len(verified),
        "audit_paths": verified,
        **expected,
    }


def audit_round(
    round_dir: Path,
    *,
    expected_max_evals: int | None = None,
    verify_current_hash: bool = False,
) -> dict[str, Any]:
    round_dir = Path(round_dir).resolve()
    required = (
        "round.json",
        "prompts.json",
        "trajectories.json",
        "adaptive_rollout_plan.json",
        "grpo_batch.jsonl",
        "round_summary.json",
        "next_bases.json",
    )
    missing = [name for name in required if not (round_dir / name).exists()]
    _require(not missing, f"missing Adaptive round artifacts: {missing}")

    meta = _load(round_dir / "round.json")
    _require(meta.get("protocol") == "adaptive_v1", "not an Adaptive V1 round")
    max_evals = int(meta.get("max_evals", 0))
    if expected_max_evals is not None:
        _require(
            max_evals == expected_max_evals,
            f"max_evals mismatch: {max_evals}!={expected_max_evals}",
        )
    _require(
        meta.get("action_surface") == "native_sah_h2spec/1.0_full",
        "round does not expose the native full h2spec action surface",
    )
    package_hash = str(meta.get("h1_package_hash", ""))
    _require(
        package_hash.startswith("sha256:") and len(package_hash) == 23,
        "invalid Adaptive H1 package hash",
    )
    analyzer_hash = str(meta.get("analysis_package_hash", ""))
    _require(
        analyzer_hash.startswith("sha256:") and len(analyzer_hash) == 23,
        "invalid Adaptive analyzer package hash",
    )
    controller_hash = str(meta.get("controller_package_hash", ""))
    _require(
        controller_hash.startswith("sha256:") and len(controller_hash) == 23,
        "invalid Adaptive controller package hash",
    )
    runtime_hash = str(meta.get("runtime_package_hash", ""))
    _require(
        runtime_hash.startswith("sha256:") and len(runtime_hash) == 23,
        "invalid Adaptive integration runtime hash",
    )
    if verify_current_hash:
        _require(
            package_hash == adaptive_v1.h1_package_hash(),
            "round H1 package hash differs from current source",
        )
        _require(
            meta.get("analysis_package_hash") == analysis_package_hash(),
            "round analyzer package hash differs from current source",
        )
        _require(
            controller_hash == controller_package_hash(),
            "round controller package hash differs from current source",
        )
        _require(
            runtime_hash == runtime_package_hash(),
            "round integration runtime hash differs from current source",
        )

    prompts = _load(round_dir / "prompts.json")
    trajectories = _load(round_dir / "trajectories.json")
    by_trace = {
        (str(item["task_id"]), int(item["k"])): item for item in trajectories
    }
    generated = {"tools": 0, "skills": 0, "middlewares": 0}
    valid_packages = 0
    analysis_sources: dict[str, str] = {}
    analysis_synthesis: dict[str, str] = {}
    analysis_fallback_errors: dict[str, list[str]] = {}
    nested_subagents: dict[str, list[str]] = {}
    assistant_counts: dict[str, list[int]] = {}

    for task_id in meta.get("tasks_order") or []:
        _require(task_id in prompts, f"missing proposer prompt for {task_id}")
        task = meta["per_task"][task_id]
        analysis_root = round_dir / "analysis" / task_id
        analysis_files = (
            "dossier.json",
            "brief.json",
            "coordinator_trajectory.json",
            "nested_traces.json",
            "meta.json",
        )
        _require(
            all((analysis_root / name).exists() for name in analysis_files),
            f"incomplete analysis artifacts for {task_id}",
        )
        analysis_meta = _load(analysis_root / "meta.json")
        _require(
            analysis_meta.get("version") == meta.get("analysis_version")
            and analysis_meta.get("package_hash") == analyzer_hash,
            f"analysis provenance mismatch for {task_id}",
        )
        try:
            source, synthesis, grounded_fallback = _validate_analysis_mode(
                analysis_meta
            )
        except Exception as exc:
            raise ValueError(f"{exc} for {task_id}") from exc
        dossier = _load(analysis_root / "dossier.json")
        brief = _load(analysis_root / "brief.json")
        known_evidence_ids = _validate_dossier_reference_closure(dossier)
        try:
            validated_brief = validate_analysis_brief(
                brief,
                known_evidence_ids,
            )
        except Exception as exc:
            raise ValueError(
                f"invalid grounded analysis brief for {task_id}: {exc}"
            ) from exc
        _require(
            validated_brief == brief,
            f"analysis brief normalization mismatch for {task_id}",
        )
        analysis_sources[task_id] = source
        analysis_synthesis[task_id] = synthesis
        if grounded_fallback:
            analysis_fallback_errors[task_id] = [
                str(item) for item in analysis_meta.get("errors") or []
            ]
        trace_nodes = list(_walk(_load(analysis_root / "nested_traces.json")))
        names = sorted(
            str(node.get("name"))
            for node in trace_nodes
            if node.get("type") == "SUB_AGENT"
        )
        nested_subagents[task_id] = names
        if source == "nexau_subagent_team":
            _require(
                names
                == [
                    "Agent: design_analyzer",
                    "Agent: performance_analyzer",
                ],
                f"missing analyzer subagent traces for {task_id}: {names}",
            )

        counts: list[int] = []
        base_spec = hs.read_base_spec(Path(task["base_package"]))
        for candidate in task.get("candidates") or []:
            key = (task_id, int(candidate["k"]))
            _require(key in by_trace, f"missing outer trajectory {key}")
            trace = by_trace[key]
            _require(
                trace.get("training_tools"),
                f"missing H1 tool schemas in trajectory {key}",
            )
            calls = _assistant_calls(trace.get("trajectory") or [])
            counts.append(calls)
            if candidate.get("valid"):
                _require(
                    all(
                        item.get("ok")
                        for item in candidate.get("review_log") or []
                    ),
                    f"valid candidate retained a failed generated-capability "
                    f"review: {key}",
                )
                _require(calls > 0, f"empty valid H1 trajectory {key}")
                if any(
                    int(item.get("rounds", 0) or 0) > 0
                    for item in candidate.get("review_log") or []
                ):
                    _require(
                        trace.get("training_response_reviewed") is True,
                        f"reviewed code was not propagated to training target: "
                        f"{key}",
                    )
                training_spec = hs.parse_and_validate(
                    _training_spec_yaml(trace.get("training_response"))
                )
                _require(
                    training_spec.valid and training_spec.spec is not None,
                    f"invalid reviewed training spec {key}: "
                    f"{training_spec.errors}",
                )
                training_effective = hs.merge_with_base(
                    training_spec.spec, base_spec
                )
                _require(
                    hs.spec_hash(training_effective)
                    == candidate.get("spec_hash"),
                    f"training target differs from rolled harness: {key}",
                )
                package = Path(candidate["dir"])
                capability_counts = _validate_package(package)
                for name, count in capability_counts.items():
                    generated[name] += count
                valid_packages += 1
            else:
                _require(
                    not candidate.get("dir"),
                    f"invalid candidate was materialized: {key}",
                )
        assistant_counts[task_id] = counts

    plan = _load(round_dir / "adaptive_rollout_plan.json")
    _require(
        plan.get("schema") == "sah.adaptive-v1-rollout-plan/1",
        "invalid Adaptive rollout plan schema",
    )
    runs = plan.get("runs") or []
    _require(runs, "Adaptive rollout plan is empty")
    outcome_repeats = int(plan.get("outcome_repeats", 0))
    promotion_repeats = int(plan.get("promotion_repeats", 0))
    _require(
        outcome_repeats > 0 and promotion_repeats > 0,
        "Adaptive rollout plan has non-positive repeat count",
    )
    _require(
        plan.get("eval_timeout_seconds") == 120,
        "Adaptive rollout plan must record eval_timeout_seconds=120",
    )
    expected_channels: Counter[tuple[str, str, int | None]] = Counter()
    expected_packages: dict[tuple[str, str, int | None], str] = {}
    for task_id in meta.get("tasks_order") or []:
        task_meta = meta["per_task"][task_id]
        expected_channels[(task_id, "outcome_base", None)] = outcome_repeats
        expected_channels[
            (task_id, "promotion_champion", None)
        ] = promotion_repeats
        expected_packages[(task_id, "outcome_base", None)] = str(
            task_meta["base_package"]
        )
        expected_packages[(task_id, "promotion_champion", None)] = str(
            task_meta["champion_package"]
        )
        for candidate in task_meta.get("candidates") or []:
            if not candidate.get("valid"):
                continue
            k = int(candidate["k"])
            expected_channels[(task_id, "outcome_candidate", k)] = (
                outcome_repeats
            )
            expected_channels[(task_id, "promotion_candidate", k)] = (
                promotion_repeats
            )
            expected_packages[(task_id, "outcome_candidate", k)] = str(
                candidate["dir"]
            )
            expected_packages[(task_id, "promotion_candidate", k)] = str(
                candidate["dir"]
            )
    observed_channels: Counter[tuple[str, str, int | None]] = Counter()
    output_dirs: list[str] = []
    for item in runs:
        candidate = item.get("candidate")
        channel = str(item.get("channel") or "")
        key = (
            str(item.get("task_id") or ""),
            channel,
            int(candidate) if candidate is not None else None,
        )
        observed_channels[key] += 1
        _require(
            key in expected_packages
            and Path(str(item.get("package"))).resolve()
            == Path(expected_packages[key]).resolve(),
            f"rollout plan uses wrong harness package: {key}",
        )
        repeat = int(item["repeat"])
        task_root = round_dir / "rollouts" / key[0]
        if channel == "outcome_base":
            expected_output = (
                task_root / "base" / "outcome" / f"repeat{repeat:02d}"
            )
        elif channel == "promotion_champion":
            expected_output = (
                task_root
                / "champion"
                / "promotion"
                / f"repeat{repeat:02d}"
            )
        elif channel == "outcome_candidate":
            expected_output = (
                task_root
                / f"cand{int(candidate):02d}"
                / "outcome"
                / f"repeat{repeat:02d}"
            )
        else:
            expected_output = (
                task_root
                / f"cand{int(candidate):02d}"
                / "promotion"
                / f"repeat{repeat:02d}"
            )
        actual_output = Path(item["output_dir"]).resolve()
        _require(
            actual_output == expected_output.resolve(),
            f"rollout plan output path differs from round layout: {key}",
        )
        output_dirs.append(str(actual_output))
    _require(
        observed_channels == expected_channels,
        "Adaptive rollout plan channel cardinality differs from round metadata",
    )
    _require(
        len(output_dirs) == len(set(output_dirs)),
        "Adaptive rollout plan reuses an output directory",
    )
    reference_seeds = {
        (
            str(item["task_id"]),
            "outcome" if item["channel"] == "outcome_base" else "promotion",
            int(item["repeat"]),
        ): int(item["request_seed"])
        for item in runs
        if item["channel"] in {"outcome_base", "promotion_champion"}
    }
    for task_id in meta.get("tasks_order") or []:
        for family, count in (
            ("outcome", outcome_repeats),
            ("promotion", promotion_repeats),
        ):
            family_seeds = [
                reference_seeds[(task_id, family, repeat)]
                for repeat in range(count)
            ]
            _require(
                len(family_seeds) == len(set(family_seeds)),
                f"reference repeats reuse request seeds: {task_id}/{family}",
            )
    for item in runs:
        channel = str(item["channel"])
        if channel not in {"outcome_candidate", "promotion_candidate"}:
            continue
        family = "outcome" if channel == "outcome_candidate" else "promotion"
        seed_key = (str(item["task_id"]), family, int(item["repeat"]))
        _require(
            int(item["request_seed"]) == reference_seeds.get(seed_key),
            f"candidate/reference request seed mismatch: {seed_key}",
        )
    scores: list[float] = []
    run_scores: dict[
        tuple[str, str, int | None], list[tuple[int, float]]
    ] = {}
    custom_calls_by_channel: dict[str, Counter[str]] = {}
    for item in runs:
        output_dir = Path(item["output_dir"])
        summaries = sorted(output_dir.glob("*/summary.json"))
        provenances = sorted(output_dir.glob("*/provenance.json"))
        results = sorted(
            output_dir.glob(f"*/results/{item['task_id']}.json")
        )
        _require(
            len(summaries) == 1
            and len(provenances) == 1
            and len(results) == 1,
            f"rollout output cardinality mismatch: {output_dir}",
        )
        provenance = _load(provenances[0])
        _require(
            int(provenance.get("request_seed", -1))
            == int(item["request_seed"])
            and int(provenance.get("max_evals", -1)) == max_evals,
            f"rollout provenance differs from plan: {provenances[0]}",
        )
        summary_rows = _load(summaries[0])
        matching_rows = [
            row
            for row in summary_rows
            if isinstance(row, Mapping)
            and row.get("task_id") == item["task_id"]
        ]
        _require(
            len(matching_rows) == 1,
            f"rollout summary task cardinality mismatch: {summaries[0]}",
        )
        result = _load(results[0])
        _require(
            result.get("stop_reason") == "completed" and not result.get("error"),
            f"incomplete rollout result: {results[0]}",
        )
        _require(result.get("trajectory"), f"empty inner trace: {results[0]}")
        score_value = result.get("best_score")
        _require(
            isinstance(score_value, (int, float))
            and not isinstance(score_value, bool)
            and math.isfinite(float(score_value)),
            f"missing/non-finite best score: {results[0]}",
        )
        _require(
            isinstance(result.get("best_program"), str)
            and bool(result["best_program"].strip()),
            f"missing best program: {results[0]}",
        )
        summary_score = matching_rows[0].get("best_score")
        _require(
            isinstance(summary_score, (int, float))
            and math.isclose(
                float(summary_score),
                float(score_value),
                rel_tol=0.0,
                abs_tol=1e-12,
            ),
            f"summary/result score mismatch: {results[0]}",
        )
        _require(
            matching_rows[0].get("stop_reason") == "completed"
            and not matching_rows[0].get("error"),
            f"incomplete rollout summary: {summaries[0]}",
        )
        channel = str(item.get("channel") or "unknown")
        custom_calls_by_channel.setdefault(channel, Counter()).update(
            _custom_tool_calls(result)
        )
        ledger = result.get("ledger") or {}
        maximum_calls = ledger.get("max_evaluator_calls")
        evaluator_calls = ledger.get("evaluator_calls")
        _require(
            isinstance(maximum_calls, int)
            and not isinstance(maximum_calls, bool)
            and maximum_calls == max_evals,
            f"ledger budget mismatch: {results[0]}",
        )
        _require(
            isinstance(evaluator_calls, int)
            and not isinstance(evaluator_calls, bool)
            and 0 <= evaluator_calls <= max_evals,
            f"invalid evaluator-call ledger: {results[0]}",
        )
        scores.append(float(score_value))
        candidate = item.get("candidate")
        score_key = (
            str(item["task_id"]),
            str(item["channel"]),
            int(candidate) if candidate is not None else None,
        )
        run_scores.setdefault(score_key, []).append(
            (int(item["repeat"]), float(score_value))
        )

    summary = _load(round_dir / "round_summary.json")
    _require(summary.get("protocol") == "adaptive_v1", "invalid round summary")
    next_bases = _load(round_dir / "next_bases.json")
    for task_id in meta.get("tasks_order") or []:
        group = summary["groups"][task_id]

        def channel_scores(
            channel: str,
            candidate: int | None = None,
            task_key: str = task_id,
        ) -> list[float]:
            return [
                score
                for _, score in sorted(
                    run_scores[(task_key, channel, candidate)]
                )
            ]

        base_samples = channel_scores("outcome_base")
        _require(
            _same_floats(
                group.get("base_score_samples") or [], base_samples
            )
            and math.isclose(
                float(group["base_score"]),
                sum(base_samples) / len(base_samples),
                rel_tol=0.0,
                abs_tol=1e-12,
            ),
            f"round summary base samples differ from results: {task_id}",
        )
        rows_by_k = {
            int(row["k"]): row for row in group.get("rows") or []
        }
        for candidate in meta["per_task"][task_id].get("candidates") or []:
            k = int(candidate["k"])
            _require(k in rows_by_k, f"round summary missing candidate row: {task_id}/{k}")
            row = rows_by_k[k]
            if candidate.get("valid"):
                outcome_samples = channel_scores("outcome_candidate", k)
                promotion_samples = channel_scores(
                    "promotion_candidate", k
                )
                _require(
                    _same_floats(
                        row.get("score_samples") or [],
                        outcome_samples,
                    )
                    and _same_floats(
                        row.get("promotion_samples") or [],
                        promotion_samples,
                    ),
                    f"round summary candidate samples differ from results: "
                    f"{task_id}/{k}",
                )
                _require(
                    math.isclose(
                        float(row["score"]),
                        sum(outcome_samples) / len(outcome_samples),
                        rel_tol=0.0,
                        abs_tol=1e-12,
                    )
                    and math.isclose(
                        float(row["promotion_score"]),
                        sum(promotion_samples) / len(promotion_samples),
                        rel_tol=0.0,
                        abs_tol=1e-12,
                    ),
                    f"round summary candidate mean differs from samples: "
                    f"{task_id}/{k}",
                )
            else:
                _require(
                    not row.get("valid") and row.get("score") is None,
                    f"invalid candidate acquired a rollout score: {task_id}/{k}",
                )
        working_k = group.get("working_k")
        if working_k is None:
            expected_package = meta["per_task"][task_id]["base_package"]
            expected_score = float(group["base_score"])
        else:
            expected_package = next(
                item["dir"]
                for item in meta["per_task"][task_id]["candidates"]
                if int(item["k"]) == int(working_k)
            )
            expected_score = rows_by_k[int(working_k)]["score"]
        _require(
            Path(next_bases[task_id]["package"]).resolve()
            == Path(expected_package).resolve()
            and math.isclose(
                float(next_bases[task_id]["score"]),
                float(expected_score),
                rel_tol=0.0,
                abs_tol=1e-12,
            ),
            f"next_bases differs from working-frontier decision: {task_id}",
        )
        _require(
            math.isclose(
                float(group["base_score_prior"]),
                float(meta["per_task"][task_id]["base_score"]),
                rel_tol=0.0,
                abs_tol=1e-12,
            )
            and math.isclose(
                float(group["working_score"]),
                float(expected_score),
                rel_tol=0.0,
                abs_tol=1e-12,
            )
            and bool(group.get("working_advanced")) == (working_k is not None),
            f"working-frontier score provenance mismatch: {task_id}",
        )
        champion_samples = channel_scores("promotion_champion")
        _require(
            _same_floats(
                group.get("champion_reference_samples") or [],
                champion_samples,
            )
            and math.isclose(
                float(group["champion_reference_score"]),
                sum(champion_samples) / len(champion_samples),
                rel_tol=0.0,
                abs_tol=1e-12,
            ),
            f"champion reference differs from results: {task_id}",
        )
        champion_k = group.get("champion_k")
        expected_champion_score = (
            rows_by_k[int(champion_k)]["promotion_score"]
            if champion_k is not None
            else group["champion_reference_score"]
        )
        _require(
            math.isclose(
                float(group["champion_score"]),
                float(expected_champion_score),
                rel_tol=0.0,
                abs_tol=1e-12,
            )
            and bool(group.get("champion_advanced"))
            == (champion_k is not None),
            f"champion-frontier score provenance mismatch: {task_id}",
        )
        _require(
            math.isclose(
                float(next_bases[task_id]["seed_score"]),
                float(meta["per_task"][task_id]["seed_score"]),
                rel_tol=0.0,
                abs_tol=1e-12,
            ),
            f"next_bases changed the protected seed score: {task_id}",
        )
        _validate_package(Path(next_bases[task_id]["package"]))

    rows = [
        json.loads(line)
        for line in (round_dir / "grpo_batch.jsonl").read_text().splitlines()
        if line.strip()
    ]
    _require(
        all(
            row.get("response_format") == "qwen3_xml_tool_call"
            and row.get("tools")
            and row.get("system")
            and row.get("user")
            and row.get("response")
            for row in rows
        ),
        "Adaptive training rows are not native tool-call rows",
    )
    rows_by_proposal = {
        str(row.get("proposal_id")): row for row in rows
    }
    for task_id in meta.get("tasks_order") or []:
        summary_rows = {
            int(row["k"]): row
            for row in summary["groups"][task_id].get("rows") or []
        }
        for candidate in meta["per_task"][task_id].get("candidates") or []:
            if not candidate.get("valid"):
                continue
            proposal_id = str(candidate["proposal_id"])
            _require(
                proposal_id in rows_by_proposal,
                f"valid candidate lacks training row: {proposal_id}",
            )
            row = rows_by_proposal[proposal_id]
            trace = by_trace[(task_id, int(candidate["k"]))]
            _require(
                row.get("task_id") == task_id
                and int(row.get("round", -1)) == int(meta["protocol_round"])
                and row.get("spec_hash") == candidate.get("spec_hash")
                and row.get("response") == trace.get("training_response")
                and math.isclose(
                    float(row["score"]),
                    float(summary_rows[int(candidate["k"])]["score"]),
                    rel_tol=0.0,
                    abs_tol=1e-12,
                ),
                f"training row differs from valid transition: {proposal_id}",
            )
    _require(
        len(rows) >= valid_packages,
        "Adaptive round is missing training rows for valid candidates",
    )
    return {
        "schema": "sah.adaptive-v1-round-audit/1",
        "audit_version": AUDIT_VERSION,
        "audit_source_hash": _audit_source_hash(),
        "ok": True,
        "protocol_round": meta.get("protocol_round"),
        "artifact_round": meta.get("round"),
        "max_evals": max_evals,
        "h1_version": meta.get("h1_version"),
        "h1_package_hash": package_hash,
        "analysis_version": meta.get("analysis_version"),
        "analysis_package_hash": analyzer_hash,
        "controller_version": meta.get("controller_version"),
        "controller_package_hash": controller_hash,
        "runtime_version": meta.get("runtime_version"),
        "runtime_package_hash": runtime_hash,
        "analysis_sources": analysis_sources,
        "analysis_synthesis": analysis_synthesis,
        "analysis_fallback_errors": analysis_fallback_errors,
        "nested_subagents": nested_subagents,
        "outer_assistant_calls": assistant_counts,
        "valid_native_packages": valid_packages,
        "generated_capabilities": generated,
        "planned_rollouts": len(runs),
        "complete_inner_traces": len(runs),
        "custom_tool_calls_by_channel": {
            channel: dict(counts)
            for channel, counts in sorted(custom_calls_by_channel.items())
        },
        "training_rows": len(rows),
        "best_observed_score": max(scores) if scores else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("round_dir", nargs="?")
    parser.add_argument("--expected-max-evals", type=int, default=None)
    parser.add_argument("--verify-current-hash", action="store_true")
    parser.add_argument("--verify-campaign-status")
    parser.add_argument("--out-dir")
    parser.add_argument("--round-base", type=int)
    args = parser.parse_args()
    if args.verify_campaign_status:
        if args.round_dir or not args.out_dir or args.round_base is None:
            parser.error(
                "--verify-campaign-status requires --out-dir and "
                "--round-base, without round_dir"
            )
        report = verify_collected_audits(
            Path(args.verify_campaign_status),
            out_dir=Path(args.out_dir),
            round_base=args.round_base,
        )
        print(json.dumps(report, indent=2))
        return
    if not args.round_dir:
        parser.error("round_dir is required for a round audit")
    root = Path(args.round_dir)
    try:
        report = audit_round(
            root,
            expected_max_evals=args.expected_max_evals,
            verify_current_hash=args.verify_current_hash,
        )
    except Exception as exc:
        report = {
            "schema": "sah.adaptive-v1-round-audit/1",
            "audit_version": AUDIT_VERSION,
            "audit_source_hash": _audit_source_hash(),
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
        report["report_path"] = str(_write_failure_report(root, report))
        print(json.dumps(report, indent=2))
        raise
    (root / "artifact_audit_complete.json").write_text(
        json.dumps(report, indent=2)
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
