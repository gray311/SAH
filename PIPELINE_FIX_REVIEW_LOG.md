# Pipeline fix review log

Reviewed: 2026-08-05. Scope: the uncommitted working-tree change set
(~2,600 lines across 37 files) that implements PIPELINE_FIX_LOG.md §2–11 plus
the file-native H1, on top of the committed §12–14 addendum
(PIPELINE_FIX_SUMMARY.md). Review method: full diff read of every src/ file,
targeted reads of the enforcement code paths, compile/syntax checks, and the
combined test suite.

## Verdict

The implementation matches the documented design, the safety invariants hold
in code (not just in prose), and it composes cleanly with the committed
§12–14 fixes. **73/73 tests pass on the combined tree.** Main action item:
the change set (including ~12 of its test files) is still uncommitted — see
Risks.

## What was verified, area by area

### 1. File-native H1 (H2OWN-001) — implemented as documented

- `src/outer/harness/agent.yaml`: the two-tool spec loop is replaced by six
  tools (`harness_shell`, `write/edit/delete_harness_file`,
  `validate_harness`, `submit_harness`); `max_iterations` 12→24; the
  harness-design skill is removed (H1 works from real files instead);
  `submit_reminder` window moved to 18/24 consistently.
- `src/outer/propose_session.py`: enforces an inspect-before-edit discipline —
  `cat agent.yaml` must come first, an existing file must be `cat`-read before
  it can be edited, and `validate_harness` refuses until `prompt.md` was read.
  Every mutation bumps `workspace_revision` and invalidates the previous
  validation; `submit_harness` requires a successful validation of the exact
  current revision and reuses the exact validated check object.
  **Accepted bytes = validated bytes; no post-submit reviewer call exists.**
- `src/outer/h2_workspace.py::inspect`: a real allowlist interpreter
  (`pwd/ls/cat/find/tree`) with root-confined path resolution — no shell
  execution, no traversal.
- `src/outer/proposer_io.py`: `H1_VERSION` bumped to `h1/2.0-file-native`;
  the base-spec YAML dump is dropped from the user message (H1 reads files).
- `src/training/grpo_to_replay.py`: H1 tool schemas are now read from
  `agent.yaml` (the single mount authority) with validation, so training rows
  match the served tool surface.

### 2. Repair-loop removal — coherent end to end

`propose.py` no longer builds a repair function; the reviewer docstring no
longer promises repair; gates + sandboxed self-tests still run at
`validate_harness` time via `review_tool_code(repair_fn=None, max_rounds=0)`.
H1 repairs its own code through validate feedback — capability parity is now
trivially exact (the "repairer" is the proposer itself).

### 3. CREDIT/TRAJ/PROV enforcement — present in code

- `program_ratchet.update_strict_single`: all seven promotion conditions with
  named rejection reasons and a per-round audit (verified line by line).
- `harness_runner`: `harness_error` never score-eligible; middleware
  participation issues (missing mount/invocation, any error) fail the rollout.
- `scripts/_outer_round_worker.sh`: verifies the runtime-source manifest and
  the immutable seed-program snapshot hash before launching.

### 4. Task-specific validity guards — mechanical, in the eval worker

`src/inner/_eval_worker.py` adds `_eplb_topology_error`,
`_prism_success_error`, and `_evaluate_txn_guarded` — the EPLB topology,
PRISM success-rate, and transaction-legality rules from the protocol are now
enforced where scores are produced, not just claimed in prose.

### 5. rewards.py checkpoint-fallback fix — a real false-credit bug closed

The wall-safe seed checkpoint could previously be mistaken for a completed
run when a harness ConfigError left a terminal row with a null score; the
fallback now applies only when no terminal task row exists. This closes a
path where a broken harness inherited the incumbent's score and leaked it
into analyzer feedback.

### 6. Executor-facing legibility

`src/inner/harness/system.md` now documents probe semantics (rank cheaply,
confirm finalists), the skill catalog, and the mounted component catalog —
the executor is told the game it is playing.

### 7. Composition with the committed §12–14 addendum

None of the §12–14 files (`session.py`, `discovery.py`, `materialize.py`,
`leak_guard.py`, `outer_round.py`, `task_text_registry.py`,
`static_gates.py`) is touched by this change set; the combined tree passes
73/73, including the tool-gate, note-guard, and registry tests.

## Checks run

- `python3 -m py_compile` over every changed `src/**/*.py`: clean.
- `bash -n` over every changed `scripts/*.sh|*.sbatch`: clean.
- `PYTHONPATH=.:src python3 -m unittest discover -s tests`: **73/73**.

## Risks / follow-ups

1. **Everything is uncommitted.** The §2–11 implementation and ~12 of its
   test files exist only in the working tree (`git status` lists 286 paths;
   only the §12–14 test files are tracked). A stray checkout or reset loses
   it. Recommend committing the change set as one unit (or a small series)
   before any further work.
2. Inspect-tracking counts only exact `cat <file>` reads; `head`/`find`
   output does not mark a file as read. This is a deliberate discipline, but
   worth stating in the H1 contract if proposers plateau on it.
3. `draw_radar_method_ablation.py` / `score_compute_curves.py` changes are
   docstring-only (no figure behavior change) — confirmed harmless.
4. The four-task clean rerun remains the standing requirement for
   route-comparison claims (PIPELINE_FIX_LOG §11.6); nothing in this set
   claims otherwise.
5. Legacy paper text still describes the removed repair chain (method §3.3)
   and old routing arm parameters — paper updates are deferred by request.
