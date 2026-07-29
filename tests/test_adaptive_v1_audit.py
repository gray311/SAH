from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO / "scripts" / "audit_adaptive_round.py"
SPEC = importlib.util.spec_from_file_location(
    "adaptive_round_audit_test_module", AUDIT_PATH
)
assert SPEC is not None and SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def test_analysis_audit_accepts_only_valid_team_or_grounded_fallback() -> None:
    assert audit._validate_analysis_mode(
        {
            "valid": True,
            "source": "nexau_subagent_team",
            "synthesis": "coordinator_json",
        }
    ) == ("nexau_subagent_team", "coordinator_json", False)
    assert audit._validate_analysis_mode(
        {
            "valid": False,
            "source": "deterministic_fallback",
            "synthesis": "deterministic_dossier_fallback",
            "errors": ["coordinator JSON truncated"],
        }
    ) == (
        "deterministic_fallback",
        "deterministic_dossier_fallback",
        True,
    )
    with pytest.raises(ValueError, match="source/synthesis"):
        audit._validate_analysis_mode(
            {
                "valid": False,
                "source": "deterministic_fallback",
                "synthesis": "deterministic_dossier_fallback",
                "errors": [],
            }
        )


def test_analysis_audit_requires_groundable_reference_closure() -> None:
    dossier = {
        "evidence": [
            {
                "evidence_id": "ev-recent",
                "learning_reward": 0.0,
            },
            {
                "evidence_id": "ev-confirmed",
                "learning_reward": 0.2,
            },
        ],
        "optimizer_memory": {
            "successful_actions": [{"evidence_id": "ev-confirmed"}],
            "invalid_signatures": [{"failure_reason": "invalid tool"}],
        },
        "analysis_contract": {
            "known_evidence_ids": ["ev-confirmed", "ev-recent"],
            "evidence_reference_closure": True,
        },
    }
    assert audit._validate_dossier_reference_closure(dossier) == {
        "ev-confirmed",
        "ev-recent",
    }

    dossier["optimizer_memory"]["invalid_signatures"][0][
        "evidence_id"
    ] = "ev-ungrounded"
    with pytest.raises(ValueError, match="ungroundable"):
        audit._validate_dossier_reference_closure(dossier)


def test_campaign_resume_requires_source_matched_round_audits(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    status_path = tmp_path / "campaign_status.json"
    out_dir = tmp_path / "outer"
    round_dir = out_dir / "round100"
    round_dir.mkdir(parents=True)
    status_path.write_text(json.dumps({"collected_rounds": [0]}))
    report = {
        "schema": "sah.adaptive-v1-round-audit/1",
        "ok": True,
        "protocol_round": 0,
        "artifact_round": 100,
        "max_evals": 20,
        "h1_package_hash": audit.adaptive_v1.h1_package_hash(),
        "analysis_package_hash": audit.analysis_package_hash(),
        "controller_package_hash": audit.controller_package_hash(),
        "runtime_package_hash": audit.runtime_package_hash(),
        "audit_source_hash": audit._audit_source_hash(),
    }
    report_path = round_dir / "artifact_audit_complete.json"
    report_path.write_text(json.dumps(report))
    monkeypatch.setattr(
        audit,
        "audit_round",
        lambda *_args, **_kwargs: {"ok": True},
    )

    verified = audit.verify_collected_audits(
        status_path,
        out_dir=out_dir,
        round_base=100,
    )

    assert verified["ok"]
    assert verified["verified_rounds"] == 1
    report["controller_package_hash"] = "sha256:stale"
    report_path.write_text(json.dumps(report))
    with pytest.raises(ValueError, match="controller_package_hash"):
        audit.verify_collected_audits(
            status_path,
            out_dir=out_dir,
            round_base=100,
        )


def test_failed_rerun_does_not_overwrite_successful_audit(
    tmp_path: Path,
) -> None:
    canonical = tmp_path / "artifact_audit_complete.json"
    previous = {
        "schema": "sah.adaptive-v1-subagent-round-audit/1",
        "phase": "complete",
    }
    canonical.write_text(json.dumps(previous))

    target = audit._write_failure_report(
        tmp_path,
        {"schema": "sah.adaptive-v1-round-audit/1", "ok": False},
    )

    assert target.name == "artifact_audit_failed_rerun.json"
    assert json.loads(canonical.read_text()) == previous
    assert json.loads(target.read_text())["ok"] is False
