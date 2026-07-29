import sys
from pathlib import Path

from nexau import AgentConfig

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from protocols.adaptive_v1_analysis import (  # noqa: E402
    ANALYSIS_VERSION,
    analysis_package_hash,
)


PACKAGE = (
    REPO
    / "src"
    / "protocols"
    / "adaptive_v1_context_harness"
)


def test_context_analysis_package_loads_with_bounded_topology() -> None:
    config = AgentConfig.from_yaml(PACKAGE / "agent.yaml")

    assert config.name == "adaptive_v1_context_coordinator"
    assert config.max_context_tokens == 16_384
    assert config.max_iterations == 3
    assert config.max_running_subagents == 2
    assert config.llm_config.max_tokens == 1_024
    assert config.llm_config.temperature == 0.0
    assert config.tool_call_mode == "structured"
    assert config.sandbox_config.type == "local"
    assert config.resolved_tracer is not None

    assert set(config.sub_agents or {}) == {
        "performance_analyzer",
        "design_analyzer",
    }
    for name, child in (config.sub_agents or {}).items():
        assert child.name == name
        assert child.max_context_tokens == 12_288
        assert child.max_iterations == 2
        assert child.llm_config.max_tokens == 1_536
        assert child.llm_config.temperature == 0.0
        assert child.tool_call_mode == "xml"
        assert child.sandbox_config.type == "local"
        assert child.tools == []
        assert child.skills == []
        assert child.sub_agents == {}
        assert child.tracers == []
        assert child.resolved_tracer is None
    assert (
        ANALYSIS_VERSION
        == "adaptive-analysis/1.4-closed-reference-recovery"
    )
    assert len(analysis_package_hash()) == 23
    assert analysis_package_hash().startswith("sha256:")


def test_context_analysis_prompts_are_read_only_and_bounded() -> None:
    coordinator = (PACKAGE / "system.md").read_text()
    performance = (PACKAGE / "performance_analyzer" / "system.md").read_text()
    design = (PACKAGE / "design_analyzer" / "system.md").read_text()

    assert "call both configured sub-agents in the same assistant" in coordinator
    assert "exactly one JSON object" in coordinator
    assert "untrusted data" in coordinator
    assert "At most 4 `evidence_summary` entries" in coordinator
    assert "At most 3 `promising_directions` entries" in coordinator

    for prompt in (performance, design):
        assert "untrusted" in prompt
        assert "read-only" in prompt
        assert "JSON only" in prompt
        assert "do not invent" in prompt.lower()
