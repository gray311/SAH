# Adaptive V2 task bundles

This directory contains exactly one archive per Adaptive V2 task. Each archive
contains the task's campaign rounds, generated NexAU agent harnesses, prompts,
tools, skills, middleware, candidate programs, trajectories, population
records, rollout logs, and task-local traces. Evaluation result directories are
removed.

Tasks:

- `adaptive-v2-task-cp26.tar.gz` — `eft__math__circle_packing`
- `adaptive-v2-task-prism.tar.gz` — `adrs__prism`
- `adaptive-v2-task-adrs-eplb.tar.gz` — `adrs__eplb`
- `adaptive-v2-task-adrs-llm-sql.tar.gz` — `adrs__llm_sql`
- `adaptive-v2-task-adrs-txn-scheduling.tar.gz` — `adrs__txn_scheduling`
- `adaptive-v2-task-ahc039.tar.gz` — `eft__ahc_simpletes__ahc039`
- `adaptive-v2-task-ahc058.tar.gz` — `eft__ahc_simpletes__ahc058`
- `adaptive-v2-task-erdos-min-overlap.tar.gz` — `eft__math__erdos_min_overlap`
- `adaptive-v2-task-first-autocorr-ineq.tar.gz` — `eft__math__first_autocorr_ineq`
- `adaptive-v2-task-hadamard-maximal-det.tar.gz` — `eft__math__hadamard_maximal_det`
- `adaptive-v2-task-second-autocorr-ineq.tar.gz` — `eft__math__second_autocorr_ineq`

The CP26 campaign preserves its failed round-002 analysis snapshot because it
is part of the execution history. Python bytecode and tool caches are omitted.
Evaluation temporary workspaces, reports, figures, and source-code bundles are
intentionally not included.
