# Adaptive V2 / NexAU artifact bundle

This directory is prepared for the `adaptive-v2-artifacts-20260804` branch of
`https://github.com/gray311/SAH`.

The bundle contains the two Adaptive V2 campaigns, generated NexAU agent
harnesses, round-by-round proposals and decisions, agent/tool trajectories,
candidate/evaluation outputs, lifecycle and health records, vLLM/worker logs,
GPU monitoring snapshots, and the reporting figures.

## Archives

- `adaptive-v2-cp26-prism-20260731T123059.tar.gz`: CP26 and Prism campaign,
  including round artifacts, harnesses, trajectories, and logs.
- `adaptive-v2-remaining9-run-root.tar.gz`: remaining-9 campaign root-level
  scripts, lifecycle, monitoring, recovery, and model-service logs.
- `adaptive-v2-remaining9-<task>.tar.gz`: one archive per remaining task,
  containing all task rounds, generated harnesses, trajectories, rollout logs,
  population dossiers, evaluations, and task-local traces.
- `adaptive-v2-eval-temp-20260804.tar.gz`: temporary candidate/request/result
  evaluation artifacts from `.tmp_adaptive_v2`.
- `adaptive-v2-reporting-20260804.tar.gz`: reports, figures, deliverables, and
  Adaptive V2 research notes.
- `adaptive-v2-source-nexau-20260804.tar.gz`: the relevant Adaptive V2,
  NexAU, EvoGate, and packaging source/configuration snapshot from the working
  tree.

The archives intentionally omit Python bytecode and tool caches. Unix sockets
in `.tmp_adaptive_v2` are runtime IPC objects and cannot be meaningfully
archived; all regular files in that directory are included. No model weights,
API keys, or private credentials are included.

`SHA256SUMS` records the checksum of every archive in this directory.
