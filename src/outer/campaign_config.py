"""Single YAML control surface for a campaign run.

One config file drives an entire campaign: task, round budget, sampling width
vs depth, reward implementation, and the *optional* Adaptive-ported features
(sequential sampling, analysis sub-agents, anti-leak guards). Defaults reproduce
the current `sah` v3 behavior byte-for-byte — an empty/minimal config changes
nothing, so the running pushes are unaffected until a feature is explicitly
turned on.

The loader is the single source of truth: it validates against the schema
(unknown keys fail closed), fills defaults, and emits the env-var overrides the
existing shell/worker layer already consumes (`K`, `MAX_EVALS`, `EVAL_TIMEOUT`,
`SAH_ADV`, ...). Nothing downstream has to learn about YAML; the config just
computes the knobs the pipeline already reads.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping

# --- schema: every key, its default, and (implicitly) its type ------------- #
# Nested dicts define sections. A value here is the DEFAULT and also pins the
# accepted key set: a key not present at its level is rejected (fail-closed),
# which catches typos like `sampling.k` vs `sampling.K` before a 3-hour round.
DEFAULTS: Dict[str, Any] = {
    "protocol": "sah",                     # sah | adaptive_v1 (feature bundle)
    "task": None,                          # required: task_id string
    "rounds": 12,
    "round_base": None,                    # required: disjoint round range start
    "workspace": None,                     # optional explicit ws dir

    "phi": {
        "resume_export": None,             # RESUME_PHI  (continue a lineage)
        "resume_ckpt": None,               # RESUME_CKPT
    },

    "sampling": {
        "K": 8,
        "mode": "parallel",                # parallel | sequential
        "max_evals": 30,
        "eval_timeout": 180,
        "force_tool_frac": 0.25,
    },

    "reward": {
        "impl": "v3",                      # v2 | v3 | legacy
        "hist_lambda": 0.3,                # v3 historical-frontier rescue weight
        "sharpen_alpha": 0.3,              # v2/v3 max-weight sharpening
    },

    # optional pre-proposal analysis sub-agents (Adaptive port). enabled=false
    # -> zero behavior change; the proposer sees only the existing feedback.
    "analysis": {
        "enabled": False,
        "performance_analyzer": True,
        "design_analyzer": True,
        "brief_token_cap": 6000,
        "dossier_char_cap": 18000,
        "dossier_rows": 8,
    },

    # optional sequential-sampling policy (Adaptive port): later samples in a
    # task's K batch see prior VALID actions to avoid paraphrase collisions.
    "sequential": {
        "enabled": False,
        "share_valid_actions": True,       # feed prior valid specs into later msgs
        "max_shared": 6,                   # cap prior actions shown
    },

    # optional anti-leak guards (Adaptive port). The sah base already has the
    # reviewer leak-markers + capability-parity repairer; these add the
    # champion-isolation and claim-word neutralization from Adaptive.
    "leakage_guard": {
        "champion_isolation": True,        # promotion signal never enters context
        "neutralize_claim_words": True,    # scrub "successful/gain/improvement"
        "scrub_leak_markers": True,        # existing reviewer behavior (kept on)
    },

    "training": {
        "kl_coef": 0.05,
        "num_epoch": 3,
        "plateau_rounds": 1,               # 1 = train every round (sah default)
    },
}

_REQUIRED = ("task", "round_base")


@dataclass
class CampaignConfig:
    data: Dict[str, Any]

    # -- typed dotted access ------------------------------------------------ #
    def get(self, dotted: str, default: Any = None) -> Any:
        node: Any = self.data
        for part in dotted.split("."):
            if not isinstance(node, Mapping) or part not in node:
                return default
            node = node[part]
        return node

    # -- env overrides for the existing shell/worker layer ------------------ #
    def env_overrides(self) -> Dict[str, str]:
        """Translate the config into the env vars the pipeline already reads,
        so no downstream code needs to know YAML exists."""
        s, r, t, p = (self.data["sampling"], self.data["reward"],
                      self.data["training"], self.data["phi"])
        env = {
            "K": str(s["K"]),
            "MAX_EVALS": str(s["max_evals"]),
            "EVAL_TIMEOUT": str(s["eval_timeout"]),
            "FORCE_TOOL_FRAC": str(s["force_tool_frac"]),
            "SAH_ADV": str(r["impl"]),
            "SAH_HIST_LAMBDA": str(r["hist_lambda"]),
            "SAH_ALPHA": str(r["sharpen_alpha"]),
            "KL_COEF": str(t["kl_coef"]),
            "NUM_EPOCH": str(t["num_epoch"]),
            # optional-feature flags (worker/propose read these; default-off keys
            # keep the sah path byte-identical when features are disabled)
            "SAH_SAMPLING_MODE": str(s["mode"]),
            "SAH_SEQUENTIAL": "1" if self.data["sequential"]["enabled"] else "0",
            "SAH_SEQ_MAX_SHARED": str(self.data["sequential"]["max_shared"]),
            "SAH_ANALYSIS": "1" if self.data["analysis"]["enabled"] else "0",
            "SAH_LEAK_NEUTRALIZE": "1" if self.data["leakage_guard"]["neutralize_claim_words"] else "0",
            "SAH_CHAMPION_ISOLATION": "1" if self.data["leakage_guard"]["champion_isolation"] else "0",
            "SAH_PROTOCOL": str(self.data["protocol"]),
        }
        if p.get("resume_export"):
            env["RESUME_PHI"] = str(p["resume_export"])
        if p.get("resume_ckpt"):
            env["RESUME_CKPT"] = str(p["resume_ckpt"])
        return env


def _deep_merge(base: Mapping[str, Any], over: Mapping[str, Any], path: str = "") -> Dict[str, Any]:
    """Merge ``over`` onto ``base``; reject any key not present in ``base``
    (fail-closed on typos). Nested dicts recurse; scalars replace."""
    out: Dict[str, Any] = copy.deepcopy(dict(base))
    for k, v in over.items():
        where = f"{path}.{k}" if path else k
        if k not in base:
            raise KeyError(f"unknown config key: '{where}' "
                           f"(valid at this level: {sorted(base.keys())})")
        if isinstance(base[k], Mapping):
            if not isinstance(v, Mapping):
                raise TypeError(f"config key '{where}' expects a mapping, got {type(v).__name__}")
            out[k] = _deep_merge(base[k], v, where)
        else:
            out[k] = v
    return out


def load(path: str | Path) -> CampaignConfig:
    import yaml
    raw = yaml.safe_load(Path(path).read_text()) or {}
    if not isinstance(raw, Mapping):
        raise TypeError(f"config root must be a mapping, got {type(raw).__name__}")
    data = _deep_merge(DEFAULTS, raw)
    missing = [k for k in _REQUIRED if data.get(k) in (None, "")]
    if missing:
        raise ValueError(f"config missing required key(s): {missing}")
    if data["sampling"]["mode"] not in ("parallel", "sequential"):
        raise ValueError(f"sampling.mode must be parallel|sequential, got {data['sampling']['mode']!r}")
    if data["reward"]["impl"] not in ("v2", "v3", "legacy", "anchored"):
        raise ValueError(f"reward.impl must be v2|v3|legacy|anchored, got {data['reward']['impl']!r}")
    # sequential mode implies sequential sampling feature (convenience)
    if data["sampling"]["mode"] == "sequential":
        data["sequential"]["enabled"] = True
    return CampaignConfig(data)


if __name__ == "__main__":  # `python -m outer.campaign_config <file>` -> env
    import sys
    cfg = load(sys.argv[1])
    for key, val in cfg.env_overrides().items():
        print(f"{key}={val}")
