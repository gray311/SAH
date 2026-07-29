"""Public Adaptive v1 protocol surface.

Implementation is split by responsibility:

* :mod:`adaptive_v1_proposal` runs a separate Adaptive NexAU H1 with bounded
  evidence memory and sequential sampling over SAH's full ``h2spec/1.0``
  action surface.
* :mod:`adaptive_v1_controller` owns rollout assessment, anchored credit,
  working/champion frontiers, plateau state, and explicit update commit.
"""
from protocols.adaptive_v1_controller import (
    CONTROLLER_VERSION,
    RolloutSamples,
    campaign_status,
    build_rollout_plan,
    cmd_collect,
    commit_update,
    controller_package_hash,
    load_best_program,
    load_rollout_samples,
    main,
    rollout_plan_shell_rows,
    write_rollout_plan,
)
from protocols.adaptive_v1_proposal import (
    ADAPTIVE_CONTEXT_MAX_CHARS,
    ADAPTIVE_CONTEXT_MAX_ESTIMATED_TOKENS,
    ADAPTIVE_CONTEXT_SCHEMA,
    ADAPTIVE_H1_PACKAGE,
    H1_VERSION,
    H1_TRAINING_TOOLS,
    MUTABLE_POINTERS,
    OBJECTIVE,
    PROTOCOL,
    PROPOSER_SYSTEM_PROMPT,
    CandidateRecord,
    build_user_context,
    cmd_propose,
    default_state,
    h1_package_hash,
    load_state,
    propose_group,
    resolve_state_path,
)
from protocols.adaptive_v1_provenance import (
    RUNTIME_VERSION,
    runtime_package_hash,
)

__all__ = [
    "ADAPTIVE_CONTEXT_MAX_CHARS",
    "ADAPTIVE_CONTEXT_MAX_ESTIMATED_TOKENS",
    "ADAPTIVE_CONTEXT_SCHEMA",
    "ADAPTIVE_H1_PACKAGE",
    "H1_VERSION",
    "H1_TRAINING_TOOLS",
    "MUTABLE_POINTERS",
    "OBJECTIVE",
    "PROTOCOL",
    "PROPOSER_SYSTEM_PROMPT",
    "RUNTIME_VERSION",
    "CandidateRecord",
    "CONTROLLER_VERSION",
    "RolloutSamples",
    "build_user_context",
    "build_rollout_plan",
    "campaign_status",
    "cmd_collect",
    "cmd_propose",
    "commit_update",
    "controller_package_hash",
    "default_state",
    "h1_package_hash",
    "load_best_program",
    "load_rollout_samples",
    "load_state",
    "propose_group",
    "resolve_state_path",
    "rollout_plan_shell_rows",
    "runtime_package_hash",
    "write_rollout_plan",
]


if __name__ == "__main__":
    main()
