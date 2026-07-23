"""Container preflight: a materialized candidate package loads as a NexAU Agent.

Mirrors exactly what inner.harness_runner does for --harness-dir candidates:
AgentConfig.from_yaml + sys.path insert (middlewares import) + endpoint override
with preserved candidate sampling. Run inside the aarch64 container with nexau
installed, cwd = repo/src.
"""
import sys
from pathlib import Path

sys.path.insert(0, ".")
from outer import harness_spec as hs  # noqa: E402
from outer.materialize import materialize, INNER_HARNESS  # noqa: E402

RAW = """```yaml
schema: h2spec/0.1
sampling: {temperature: 1.1, top_k: 40}
agent: {max_iterations: 24}
middleware: {budget_reminder_from_left: 5}
```"""

base = hs.read_base_spec(INNER_HARNESS)
v = hs.parse_and_validate(RAW)
assert v.valid, v.errors
eff = hs.merge_with_base(v.spec, base)
ok, changed = hs.differs_from_base(eff, base)
assert ok, "must differ"
cdir = Path("/tmp/sah_cand_container_test")
materialize(eff, cdir, meta={"effective": eff})

sys.path.insert(0, str(cdir))  # same as harness_runner for candidates
from nexau import Agent, AgentConfig  # noqa: E402
from inner.harness_runner import LLMEndpoint, _override_llm  # noqa: E402

cfg = AgentConfig.from_yaml(cdir / "agent.yaml")
_override_llm(cfg, LLMEndpoint(base_url="http://127.0.0.1:1/v1"),
              preserve_sampling=True, top_k_override=40)
agent = Agent(config=cfg)
assert cfg.llm_config.temperature == 1.1, "candidate sampling must be preserved"
assert cfg.max_iterations == 24
names = [getattr(t, "name", t) for t in cfg.tools]
print("CANDIDATE AGENT BUILT OK | tools:", names,
      "| temp:", cfg.llm_config.temperature, "| iters:", cfg.max_iterations,
      "| changed:", changed)

# --- H1 (proposer harness package) also builds as a NexAU agent --- #
from outer.h1 import H1_PACKAGE  # noqa: E402

h1_cfg = AgentConfig.from_yaml(H1_PACKAGE / "agent.yaml")
h1_agent = Agent(config=h1_cfg)
h1_tools = [getattr(t, "name", t) for t in h1_cfg.tools]
assert h1_cfg.llm_config.temperature == 1.0 and h1_cfg.max_iterations == 8
print("H1 AGENT BUILT OK | tools:", h1_tools, "| stop:", h1_cfg.stop_tools)
