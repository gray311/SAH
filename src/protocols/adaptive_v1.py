"""Public Adaptive v1 protocol surface.

Implementation is split by responsibility:

* :mod:`adaptive_v1_proposal` owns the frozen prompt, bounded context, typed
  semantic actions, deterministic compilation, and sequential K sampling.
* :mod:`adaptive_v1_controller` owns rollout assessment, anchored credit,
  working/champion frontiers, plateau state, and explicit update commit.
"""
from protocols.adaptive_v1_controller import (
    RolloutSamples,
    campaign_status,
    cmd_collect,
    commit_update,
    load_best_program,
    load_rollout_samples,
    main,
)
from protocols.adaptive_v1_proposal import (
    ADAPTIVE_H1_PACKAGE,
    ALIASES,
    H1_VERSION,
    MUTABLE_POINTERS,
    OBJECTIVE,
    PROTOCOL,
    PROPOSER_SYSTEM_PROMPT,
    CandidateRecord,
    EditAtom,
    HarnessAction,
    _digest,
    build_user_context,
    cmd_propose,
    compile_action,
    default_state,
    h1_package_hash,
    load_state,
    make_nexau_generator,
    propose_group,
    read_adaptive_base,
    resolve_state_path,
)

__all__ = [
    "ADAPTIVE_H1_PACKAGE",
    "ALIASES",
    "H1_VERSION",
    "MUTABLE_POINTERS",
    "OBJECTIVE",
    "PROTOCOL",
    "PROPOSER_SYSTEM_PROMPT",
    "CandidateRecord",
    "EditAtom",
    "HarnessAction",
    "RolloutSamples",
    "build_user_context",
    "campaign_status",
    "cmd_collect",
    "cmd_propose",
    "commit_update",
    "compile_action",
    "default_state",
    "h1_package_hash",
    "load_best_program",
    "load_rollout_samples",
    "load_state",
    "make_nexau_generator",
    "propose_group",
    "read_adaptive_base",
    "resolve_state_path",
]


if __name__ == "__main__":
    main()
