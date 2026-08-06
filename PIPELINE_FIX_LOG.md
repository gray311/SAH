# Evolve pipeline fix log

Updated: 2026-08-05

## 0. Scope and current status

This change set repairs the pipeline defects exposed by the eight AC2
case-study nodes. It changes future H1/H2 evolution, rollout attribution,
training eligibility, and experiment provenance. It does **not** rewrite old
artifacts or retroactively turn legacy scores into clean evidence.

The canonical comparison remains:

| Route | Per-batch generated trajectories | Updated state |
|---|---:|---|
| Update proposer weights | 8 H1 + 8 H2 | proposer LoRA |
| Analyzer/context only | 8 H1 + 8 H2 | task-local analyzer context |
| Update executor weights | 16 H2 | executor LoRA |

All routes use `x = 1, 17, ..., 305`: one shared display anchor, 19 batches,
16 generated agent trajectories per batch, and 18 evaluated update
opportunities. The final batch is measurement-only, so no unmeasured trailing
adapter is trained.

No `sbatch`, `scancel`, or GPU execution was issued while implementing these
fixes. Existing dependency-gated controllers were not modified. A canonical
run must create its runtime snapshot after these fixes; otherwise it is not a
clean rerun of this pipeline.

## 1. What the eight AC2 nodes actually established

The historical nodes were useful for diagnosis, but they mix genuine mechanism
evidence with several pipeline artifacts:

1. Node 01: prompt/skill guidance caused the executor to replace one start with
   six deterministic starts. Multi-start was not a custom tool; it was enacted
   through ordinary code edits.
2. Node 02: context requested broad search, but the executor used zero probes
   and spent all full evaluations repairing one weak candidate. Text context
   did not preserve a strong executable search state.
3. Node 03: the apparent jump was an inherited program already present at
   executor step 0. That round did not earn discovery credit.
4. Node 04: the context route recovered from its preceding drop, but the winner
   called the new probe only once. The trace does not justify attributing the
   jump to the tool.
5. Node 05: representation switching was relevant, but the executor made two
   probes and then produced invalid code before any full evaluation. The
   proposed diversification middleware was mounted but did not execute under
   the old wrapper contract.
6. Node 06: another context instruction requested topology switching and
   probe-first behavior; the frozen policy ignored it, used zero probes, and
   returned to local/no-op edits.
7. Node 07: an executable screen-then-verify harness worked: a generator tool,
   structured skill, and middleware changed both candidate generation and
   allocation of cheap versus expensive feedback.
8. Node 08: executor updating produced a real local optimizer improvement, but
   remained inside the fixed interface and did not create the representation or
   screening machinery seen in node 07.

This audit led to the fixes below.

## 2. MW-001 — middleware was present on disk but did not participate

### Root cause

- Generated hooks treated the framework hook input as a dictionary.
- The old wrapper swallowed hook exceptions.
- State such as `family_streak` had no supported runtime producer.
- A candidate could still publish a score after its proposed middleware never
  ran.

### Fix

- Generated middleware now receives a stable read-only state mapping produced
  from the active inner session.
- Supported state includes iteration, remaining budgets, latest error/result,
  stalled evaluations, probes since evaluation, structural-family streak, and
  explored families.
- Every generated middleware records `mounts`, `invocations`, `fires`,
  `errors`, last iteration, and last error.
- A middleware may fire zero times; that means its condition was ineffective,
  which is a valid experimental outcome.
- It may not have zero mounts, zero invocations, or an execution error. Any of
  those makes the rollout `score_eligible=false`.
- Static validation currently permits only the adapted `before_model` hook.
  Unsupported framework hooks fail before rollout.
- Generated wrapper code is compiled and validated atomically; a bad
  middleware invalidates the complete candidate instead of being silently
  dropped.

Primary files:

- `src/inner/harness/middleware/generated_context.py`
- `src/inner/session.py`
- `src/inner/harness_runner.py`
- `src/outer/materialize.py`
- `src/outer/static_gates.py`

Regression coverage: `tests/test_generated_middleware_runtime.py`.

## 3. INHERIT-001 — tool, skill, and middleware inheritance was replacing state

### Root cause

The old merge treated `new_tools`, `new_skills`, and `new_middlewares` as
whole-list replacements. A child that proposed one component silently dropped
all omitted parent components. This is why the eight-node artifact sequence did
not form a cumulative harness lineage.

### Fix

- Generated components merge by stable component name.
- A new name appends; the same name updates in place; an omitted name is
  inherited.
- Deletion is explicit. The proposer must remove the file, remove the
  `agent.yaml` mount, and remove the prompt advertisement.
- `agent.yaml` is the mount authority. Mounted-but-missing,
  unmounted-but-present, stale provenance, and orphan schema/code files all
  fail closed.
- Each accepted package stores a component manifest and parent-relative
  `inherited`, `added`, `updated`, and `removed` lineage.
- The executor decides whether to call optional tools and load optional skills.
  Middleware is different: it is automatically mounted and must enter its hook.

Primary files:

- `src/outer/harness_spec.py`
- `src/outer/materialize.py`
- `src/outer/h2_workspace.py`
- `src/inner/harness_runner.py`

Regression coverage:

- `tests/test_generated_component_inheritance.py`
- `tests/test_h2_workspace.py`

## 4. H2OWN-001 — H1 did not truly own the executor harness

### Root cause

H1 previously received a flattened description and submitted a detached spec.
It could not traverse the actual mount graph, inspect an inherited
implementation before editing it, or consistently update the executor system
prompt. Runtime post-processing could also alter what H1 submitted.

### Fix

Every H1 candidate now receives a private file-native copy of its parent H2.
The required interaction is:

```text
cat agent.yaml
  -> inspect relevant mounted directories/files
  -> edit/create/delete H2 files
  -> validate_harness
  -> submit_harness
```

- Read feedback is appended to the H1 conversation exactly like ordinary tool
  feedback.
- H1 may edit `agent.yaml`, `prompt.md`, generated tool schemas/code, skill
  files, middleware descriptors/code, sampling parameters, and supported
  middleware parameters.
- H1 cannot edit evaluator code, session state, runtime adapters, result files,
  or provenance.
- `prompt.md` is the executor system prompt and therefore part of H2. Runtime
  no longer appends component text or repairs it after submission.
- `agent.yaml`, mounted files, and prompt component inventory must agree.
- Candidate workspaces are isolated from the parent and from parallel H1
  candidates.
- The accepted bytes are exactly the bytes H1 validated and submitted. There
  is no post-submit model reviewer or automatic repair call.

Primary files:

- `src/outer/h2_workspace.py`
- `src/outer/propose_session.py`
- `src/outer/propose.py`
- `src/outer/harness/system.md`
- `src/outer/harness/agent.yaml`
- `src/outer/harness/tools/*.tool.yaml`

## 5. CREDIT-001 — inherited program and step-0 gain received false credit

### Root cause

The old rollout read a mutable cross-round program registry. A strong inherited
program could appear at the next plotted node even when every executor started
and ended with the same bytes. Harness base, program base, and observed seed
were not first-class linked provenance.

### Fix

- `outer_round propose` snapshots the program registry into the immutable
  round-local `seed_programs_in.json` before any H1 or H2 call.
- Every H2 slot consumes that snapshot, never the mutable workspace registry.
- The worker verifies the snapshot hash against `round.json` before launching.
- Every rollout records the exact seed program hash, registry path/hash,
  claimed source score/round/k, and observed seed score.
- Every rollout also records the exact H2 package path and canonical H2 hash.
- Canonical `strict_single` maintains one task-local program incumbent. QD
  elites and crossover parents are disabled in the comparison.
- A candidate program is promoted only if all of the following hold:
  1. result score equals the group-reported score;
  2. seed-registry hash equals the frozen round snapshot;
  3. inherited seed hash equals the previous program incumbent, or the cold
     batch explicitly uses `task_initial`;
  4. candidate H2 bytes equal the H2 hash recorded by the rollout;
  5. output program differs from the seed program;
  6. output score beats the observed rollout seed;
  7. output beats both the incoming H2 score and program incumbent.
- A raw score increase that fails attribution cannot advance either H2 or the
  program incumbent.
- Its complete task-level proposer advantages are zeroed, so the same false
  gain cannot update proposer weights indirectly.
- `program_ratchet_audit.json`, `seed_programs_in.json`, and accepted/rejected
  reasons are retained per round.

Primary files:

- `src/outer/program_ratchet.py`
- `src/outer/outer_round.py`
- `scripts/_outer_round_worker.sh`
- `src/inner/run_baseline.py`
- `src/inner/package_hash.py`

Regression coverage: `tests/test_program_ratchet.py`.

## 6. TRAJ-001 — failed or missing executor conversations could publish a seed

### Root cause

The inner session deliberately preserved its seed checkpoint after an agent
exception. That diagnostic fallback could be mistaken for a completed executor
trajectory. A required-but-missing conversation also marked an error without
always making the score ineligible.

### Fix

- `harness_error` is never score eligible.
- Under `--require-trajectory`, a missing assistant turn sets
  `score_eligible=false`.
- Full diagnostic score/program/error data remains in the per-task result, but
  published `best_score` and `delta` are `null`.
- The outer worker audits all required conversations before collection.
- Already launched failures remain charged on the trajectory axis and in cost
  accounting; they are not replaced with top-up trajectories.

Regression coverage:

- `tests/test_trajectory_retention.py`
- `tests/test_outer_rewards.py`

## 7. TOOLSEC-001 — generated tools needed a candidate-local capability boundary

### Fix

- Generated code receives `ToolContext`, not the live session object.
- Program/evaluator paths are canonicalized and restricted to task-local files.
- Prefix tricks, sibling paths, absolute generated-tool paths, evaluator state,
  reflection, process/network access, and unsafe imports fail validation.
- Tool scratch storage is per rollout and per candidate.
- Tool source resolution is relative to the active H2 package; there are no
  stale absolute paths copied from a parent package.
- Tool invocation/completion/error events are persisted. Optional tool use is
  still the executor's decision.

Primary files:

- `src/inner/harness_sdk.py`
- `src/inner/harness/tools/custom_runtime.py`
- `src/inner/session.py`
- `src/outer/static_gates.py`

Regression coverage: `tests/test_tool_security_contract.py`.

## 8. FAIR-001 — matched axis, update cadence, seeds, and training settings

### Frozen trajectory protocol

- Proposer: 8 H1 + 8 H2 launched trajectories per batch.
- Context: 8 H1 + 8 H2 launched trajectories per batch.
- Executor: 16 H2 launched trajectories per batch.
- Invalid H1 proposals still consume their paired H2 slot using an explicitly
  labelled incumbent fallback; that fallback cannot become positive reward for
  the invalid H1 row.
- No route tops up failed trajectories.
- Logical H2 seed block is `200000 + 16 * batch_index + k`; the first eight
  executor-route seeds pair with the eight H2 seeds in both H1 routes.
- H1 seed is deterministic by logical round and candidate.

### Matched weight-update settings

Both weight-update routes use LoRA rank/alpha 64/128, three epochs, learning
rate `3e-5`, KL coefficient `0.05`, micro batch 1, and adapter continuation.
Both take one optimizer boundary per epoch. The proposer requires at least four
of eight trainable H1 rows; the executor requires at least eight of sixteen
usable H2 rows. Thus both thresholds are 50% of the launched route-specific
training candidates.

For proposer batches with 4--7 trainable rows, zero-advantage copies fill the
fixed GBS=8 geometry. A new `replay_manifest.json` distinguishes:

- genuine generated trainable rows;
- archive-mixed rows (fixed to zero in the canonical comparison);
- zero-advantage geometry padding;
- total optimizer rows.

The executor route uses only distinct usable H2 rows and sets GBS to that safe
subset. These settings match update capacity/cadence; they do **not** imply
equal training tokens or equal FLOPs.

Primary files:

- `scripts/reward_route_inference16_config.sh`
- `src/outer/trajectory_budget.py`
- `scripts/train_mphi_step.sh`
- `scripts/submit_ttt_executor_update.sh`
- `scripts/ttt_discover_prepare.py`
- `scripts/ttt_executor_eval.sbatch`
- `scripts/drive_ttt_executor_12h.sh`

## 9. PROV-002 — source, H2, checkpoint, and endpoint binding

### Runtime source

- Each route atomically copies and hashes all execution-relevant `src` files,
  H1/H2 prompt/skill files, runtime scripts, and frozen reference registries.
- Every later batch verifies both live repository bytes and the immutable copy.
- Plotting, case-study, and prose files are excluded because editing a figure
  cannot change execution and must not invalidate a long run.

### H2 and TTT manifests

- One canonical location-independent H2 hashing function is shared by the
  inner rollout, command-line hash tool, TTT collector, and eval worker.
- Manual completion, timeout, and straggler collection paths now record and
  verify the same H2 hash, batch index, decode seed base/list, checkpoint, job
  ID, evaluator calls, and observed executor model calls.
- Executor archive nodes store exact source summary, originating step/k, and
  executor checkpoint.

### Endpoints

- Each run captures its x=1 program into its own namespace. Resuming is
  idempotent, but changing its program or score is rejected.
- Endpoint collection reads only that captured copy, not the mutable global
  index.
- A proposer/context endpoint resolves to the exact promoting round, candidate
  H2, result file, proposer checkpoint, and executor checkpoint.
- An executor endpoint resolves to the exact archive node, source rollout,
  originating eval batch, and checkpoint.
- Before re-evaluation, every program hash and H2 package hash is checked.
- Endpoint programs are evaluated at least five times; only the resulting mean
  may enter the authoritative main-result registry.

Primary files:

- `scripts/runtime_provenance.py`
- `scripts/capture_shared_anchor.py`
- `scripts/hash_h2_package.py`
- `scripts/collect_ttt_eval_manifest.py`
- `scripts/collect_reward_route_inference16_endpoint_programs.py`
- `scripts/revalidate_reward_route_endpoints.py`
- `scripts/bind_reward_route_inference16_main_results.py`

Regression coverage:

- `tests/test_runtime_provenance.py`
- `tests/test_h2_hash_contract.py`
- `tests/test_anchor_capture.py`
- `tests/test_inference16_effects.py`

## 10. COST-001 — trajectory equality is not compute equality

`scripts/collect_reward_route_inference16_costs.py` now reports, per route:

- launched H1/H2 trajectories and terminal summaries;
- observed evaluator calls;
- observed H1, analyzer, and executor model calls;
- generated trainable rows versus optimizer rows/padding;
- eligible/applied update counts;
- every associated Slurm job ID and allocated GPU-hours from `sacct`.

The paper-safe statement is **matched launched generated-agent trajectories**.
It is not an equal-token, equal-evaluator-call, equal-FLOP, or equal-GPU-hour
experiment. Call totals are observed lower bounds when a failed launched
trajectory exits before writing a terminal summary; the failure is still
present in the exact launched-trajectory count and Slurm accounting.

## 11. Known boundaries that remain explicit

1. The eight AC2 node bundles are immutable legacy evidence. They demonstrate
   why the bugs matter, but cannot validate the repaired cumulative pipeline.
2. Node 05's old text says seven no-ops and one invalid candidate, while its
   structured round summary says five no-ops and three invalid candidates. The
   structured summary is authoritative; figure cleanup is intentionally
   deferred to the later visualization pass.
3. Some legacy result files have no full executor conversation. New canonical
   runs fail closed when the conversation is absent.
4. The shared historical x=1 source records exact program bytes and score, but
   not the exact historical H2 hash or executor checkpoint that originally
   generated it. Each route therefore labels its current H2 hash as
   `route_initial_h2_for_legacy_anchor`, not as fabricated origin provenance.
   The anchor is display-only and is not inherited. A claim requiring exact
   origin-H2 provenance needs a newly generated x=1 measurement.
5. Checkpoint paths, LoRA lineage, Slurm jobs, and configuration are recorded,
   but full tensor files are not re-hashed every round. Model directories must
   remain immutable; tensor-level cryptographic binding would require a
   separate storage/checksum pass.
6. The fixes establish protocol correctness. They do not establish that the
   proposer route wins; that requires the four-task clean rerun and endpoint
   revalidation.

## 12. MWGATE-001 — advisory-only middleware could be ignored by the executor

### Root cause

A generated `before_model` hook could only inject advisory text.  The AC2
nodes showed the executor ignoring injected imperatives (zero probes despite a
probe-first gate), which is an executor/hook-capability fact shared by every
route -- the hook had no mechanical authority.

### Fix

- A hook may now return `{"note": str?, "require_tools": [tool, ...]?}` in
  addition to the plain advisory string.  The hook stays a pure function; the
  trusted wrapper applies effects.
- `require_tools` arms a session-level gate: the executor's next tool call
  must come from the named subset (`probe_solution`, `edit_solution`,
  `evaluate_solution`).  A disallowed call is refused with a structured
  message and consumes no budget.  `finish` is never gated; two refusals
  auto-lift the gate, so it steers without hard-locking.
- Enforcements, satisfactions, refusals, and auto-lifts are audited per
  middleware inside `middleware_audit[...]["gate"]`.  Malformed dict shapes
  are hook errors (score-ineligibility rules unchanged).
- The hook state mapping gains read-only `active_tool_gate`; the static gate
  whitelists it, and the H1 contract documents the dict return.

Primary files: `src/inner/session.py`, `src/inner/harness/tools/discovery.py`,
`src/outer/materialize.py`, `src/inner/harness/middleware/generated_context.py`,
`src/outer/static_gates.py`, `src/outer/harness/system.md`.

Regression coverage: `tests/test_tool_gate.py`,
`tests/test_generated_middleware_runtime.py` (gate cases).

## 13. NOTEGUARD-001 — curated-note channel had no anti-code defense

### Root cause

`leak_guard.sanitize` drops marker words (evaluator/target-score), but the
historical solution-injection note carried a *program* and the word
"verbatim" -- no marker word at all.  A note channel that can carry code can
carry solutions.

### Fix

- `leak_guard.code_signals` / `sanitize_note`: any code fence, line-start
  statement keyword (`def`/`import`/`from`/`class`/`return`/`lambda`/`@`),
  the token "verbatim", or an over-length note (>1500 chars) drops the whole
  note fail-closed; mid-sentence English is unaffected.  Wired into the
  analyst-note path with the dropped signals printed.
- Task-text pinning: `scripts/build_task_text_registry.py` pins sha256 of
  every task's spec and initial program from the frozen dataset into
  `provenance/task_text_registry.json` (25 tasks).  Every round verifies the
  texts it serves and writes `task_text_provenance.json`; mismatches are
  fatal under `SAH_TASK_TEXT_ENFORCE=1` (exported by the canonical driver).

Primary files: `src/outer/leak_guard.py`, `src/outer/outer_round.py`,
`src/outer/task_text_registry.py`, `scripts/build_task_text_registry.py`,
`scripts/drive_reward_route_inference16_h1.sh`.

Regression coverage: `tests/test_note_injection_guard.py`,
`tests/test_task_text_registry.py`.

## 14. RATCHETMODE-001 — legacy_qd was the silent default

### Fix

- `program_ratchet_audit.json` now records the mode and whether it came from
  the environment or the default.
- `SAH_REQUIRE_STRICT_RATCHET=1` (exported by the canonical driver) makes any
  mode other than `strict_single` a hard error before the round runs.

Primary files: `src/outer/outer_round.py`,
`scripts/drive_reward_route_inference16_h1.sh`.

## 15. Verification performed

- Python compilation completed for all modified runtime/finalization modules.
- Shell syntax checks completed for the H1 worker/trainer and executor driver.
- `PYTHONPATH=.:src python3 -m unittest discover -s tests -v`: **60/60 passed**
  at the section 2--11 change set; **73/73 passed** after sections 12--14.
- Static inference-16 audit passed and returned the frozen four tasks, 19
  batches, 18 updates, and common endpoint `x=305`.
- No GPU job was launched as part of this repair/verification pass.

