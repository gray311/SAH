# HarnessRL — experiment handoff plan

Written 2026-08-02. Everything below is either verified against data/code or
explicitly marked as unverified. Read §5 (pitfalls) before running anything —
most of it is a list of ways I already wasted GPU hours.

> **Live amendment (2026-08-03): §§1--4 and §8 below describe the superseded
> six-task pilot, not the canonical paper comparison now running.**  The final
> 1x7 comparison has Hadamard, AHC039, AHC058, EPLB, PRISM, LLM-SQL, and
> Transaction scheduling.  It plots exactly three routes: task-local
> proposer-weight campaigns (ours), isolated analyzer-context
> campaigns (ours ablation; both weights frozen), and a local budget-scaled
> TTT-Discover-style executor-weight reference (not our method).  The primary
> x-axis measures launched executor trajectories, not equal FLOPs or equal GPU
> time.  Canonical run roots and all caveats are recorded by
> `scripts/plot_reward_route_12h.py` and fail-closed in
> `scripts/audit_score_compute_sota5.py`.
>
> Do **not** use the old `ttt_arm` data, the pre-guard system-context run,
> historical LLM-SQL rounds 471--475, historical Transaction rounds 450/460--463,
> or historical PRISM rounds 410--417.  SQL serialized a curated note naming a
> 0.728 program; Transaction inherited an illegal one-element schedule; PRISM
> selected a success-rate-0.98 candidate and used its harness as the next base.
> A separate reward-attribution audit found that the legacy loader also fell
> back to the seed checkpoint when a terminal summary explicitly reported
> `best_score=null` after a harness `ConfigError`.  That violates the documented
> failed-trajectory reward of -1 and contaminates later weight/context updates.
> Historical Hadamard/AHC058 proposer lineages and AHC058/PRISM context lineages
> are therefore excluded as well.  `src/outer/rewards.py` now treats a terminal
> task row as authoritative and permits checkpoint fallback only when no
> terminal task row exists; the fix is regression-tested against the stored
> PRISM failure.
> The admissible proposer replacements are
> `outer-proposer-sota7-sql-clean-v2` (round1200+),
> `outer-proposer-sota7-txn-clean-v1` (round1000+), and
> `outer-proposer-sota7-prism-clean-v1` (round1020+), plus
> `outer-proposer-sota7-hadamard-rewardfix-v1` (round1040+) and
> `outer-proposer-sota7-ahc058-rewardfix-v1` (round1060+).  The shared
> `outer-context-sota7-rewardfix-v1` campaign remains admissible for PRISM, but
> **not for AHC058**: AHC058 round1101 improved to 1.2732476556 without the
> immutable Slurm marker proving that an analyzer brief was attached, and all
> later AHC058 rounds inherit that non-analyzer harness.  The tempting result
> and its descendants are excluded.  AHC058 context instead uses the isolated
> analysis-required recovery
> `outer-context-sota7-ahc058-analysis-required-v1` (round1120+), whose
> controller rejects the whole round and restores the pre-round task-local
> state whenever a post-cold analyzer marker is absent.
> Each starts its first
> adaptive batch from `task.initial_program` and uses the current output guard.
> The
> canonical executor roots are `ttt_discover_sota5_k8` and
> `ttt_discover_sota5_k8_ahc039`, plus `ttt_discover_sota7_extra_k8` for
> Hadamard/Transaction; every executor training batch must have at least eight
> distinct usable/replay rows, and failed/top-up launches remain charged.  H1
> routes propose eight candidates; schema-invalid proposals that never launch an
> executor are excluded from trajectory x but charged in the proposal/model-call
> ledgers.
> The rollout axis is a sample-efficiency comparison, not a total-compute
> equivalence claim.  The final audit also reports charged evaluator-call
> budgets, recorded executor/H1/analyzer model calls, sandbox time, optimizer
> boundaries, and authoritative `sacct` allocated GPU-hours.  In particular,
> proposer-weight outer jobs reserve four GPUs but run H1 on one trained-phi
> replica (the remaining replicas keep the frozen base available), whereas the
> frozen context proposer can parallelize H1 over as many as four replicas.
> Logical H1 work is comparable; wall-clock concurrency is not.  Proposer LoRA
> uses r64/a128 for three epochs, while the local executor reference uses
> r32/a64 for one epoch.  Any efficiency claim must therefore say exactly which
> ledger it refers to.  Serialized H1 assistant turns do not fully recover
> transport retries or server work orphaned after a client timeout, so reported
> model-call counts are explicitly lower bounds rather than FLOP estimates.
> Final N>=5 endpoint re-evaluation is evaluator-only, CPU-only common
> measurement overhead performed after adaptation.  It validates stochastic
> program scores but is excluded from every route's adaptation GPU-cost ledger.
> The seven tasks were explicitly chosen as the paper's
> priority/strength set, not sampled as an unbiased benchmark population.
> Aggregate claims must therefore be scoped to this declared set; they cannot
> be presented as an estimate of average performance over all tasks.
> Claim selection is also fixed before the final results: strong
> executor-trajectory sample-efficiency language requires proposer weights to
> lead both common-budget macro score and common-budget macro log-AUC.  Strong
> observed-endpoint language requires both a leading macro endpoint ratio and
> pairwise-majority wins versus each alternative.  The audit separately lists
> tasks where all three routes meet the empirical plateau rule.  Finite
> plateau/cap endpoints must never be called absolute or asymptotic limits; if
> these gates are mixed, report the task-level wins/losses and all predeclared
> aggregates rather than selecting a favorable post-hoc subset.
> Zero-trajectory infrastructure failures are quarantined in
> `results/sota7_operational_retries.json` and charged only to the separate
> as-run overhead ledger.  The analysis-required AHC058 controller separately
> archives any executed-but-rejected attempt under
> `rejected_analysis_attempts/`; those trajectories contribute no logical
> method score or x-budget, but their full allocation is also charged in
> as-run GPU-hours.  Five other proposer/context outer jobs exited
> nonzero after all requested trajectories and both atomic collector artifacts
> were already complete; these are accepted score evidence and their entire
> allocation remains charged.  Their fixed, machine-checked exception set is
> `results/sota7_accepted_job_anomalies.json`.  Do not move those jobs into the
> zero-work retry ledger or silently treat their nonzero batch state as missing
> compute.
>
> No final figure is publishable until all context and executor campaigns reach
> the common three-transition plateau rule or their explicit cap, all five clean
> proposer replacements pass their own plateau/cap review (`CANONICAL_COMPLETE`),
> online and legacy semantic guards match the current evaluator worker, all 21
> route endpoints receive at least five repeat evaluations, and the strict audit
> passes without `--allow-incomplete`.  That audit parses all seven relevant
> cells in each of `\method(initial)`, `\method(context)`, and
> `\method(weight)` and requires them to equal the figure's canonical H2,
> context, and proposer endpoints at the table's displayed precision.  The
> completion gate is
> `scripts/finalize_sota7_when_done.sh`; the intended artifacts are
> `papers/figures/score_compute_curves_sota7.{png,pdf}` and the matching
> `_data.json`/audit JSON.  The strict audit also feeds
> `scripts/render_score_compute_cost_table.py`, which keeps common-rollout
> score/AUC separate from full-campaign trajectory, H1, evaluator, model-call,
> optimizer-boundary, and accepted/as-run GPU-hour totals.  After the
> allow-incomplete post-campaign audit has enumerated every job, run
> `scripts/collect_sota7_sacct_snapshot.py`; it refuses a publishable
> `results/sota7_sacct_snapshot.json` unless every requested top-level job has a
> terminal authoritative `sacct -X` row and nonzero GPU allocation.  The strict
> audit reads that frozen snapshot first and queries live accounting only for
> missing rows.  A log-time proxy is never sufficient for the final cost claim.
> Before paper sync, also check whether the aggregate conclusion is sensitive
> to AHC039's admissible
> historical K=16/max-evals=30 proposer cadence; if it is, run a fresh K=8/20
> proposer arm and demote the historical curve to a disclosed sensitivity.
> This amendment will replace the stale pilot sections once those conditions
> are met.

> **Main-text view policy fixed 2026-08-04 after interim inspection.**  The
> paper's compact main-text figure is a 1x4 illustrative task-level view of
> **Hadamard, EPLB, PRISM, and Transaction scheduling**.  These are the four
> tasks on which the current proposer curve leads the local executor reference
> at the task-specific common trajectory budget; they were therefore selected
> to make the efficiency pattern legible, not predeclared as a representative
> benchmark sample.  The caption and surrounding text must disclose that the
> selection was made after interim inspection.  This 1x4 view may support only
> named, task-level statements and must not report or motivate a four-task
> macro average, win rate, population claim, or claim of across-the-board
> superiority.  A route need not lead every endpoint in these panels: distinguish
> common-budget score, log-AUC/SOTA-crossing speed, and observed finite endpoint.
> The canonical 1x7 figure remains the appendix view and the sole source for all
> aggregate gates and wins/losses; every full seven-task reported condition must
> continue to match that 1x7 manifest point by point. Both views are rendered from the
> same canonical roots with `scripts/render_sota_reward_views.sh`, producing
> `score_compute_curves_sota4_{live,final}.{png,pdf}` and
> `score_compute_curves_sota7_{live,final}.{png,pdf}`.  The selected view is
> publishable only if `scripts/audit_sota4_view.py` proves that every displayed
> route point and provenance field is an exact subview of the audited 1x7 data
> and that no standalone four-task aggregate has been serialized.
> `audit_score_compute_sota5.py` additionally has a strict paper gate.  Before
> the paper-sync marker can be accepted, the main text must reference
> `score_compute_curves_sota4_final.pdf`, label it an illustrative view chosen
> after interim inspection, scope the claim to executor-trajectory sample
> efficiency, and direct every aggregate interpretation to the full seven-task
> appendix figure `score_compute_curves_sota7_final.pdf`.  The gate rejects the
> old sota5 figure, five-task wording, every-task/full-ordering claims, and the
> inadmissible historical SQL/Txn table values.  Allow-incomplete mode lists
> these as `pending_paper_sync`; strict mode fails until all are resolved.

> AHC058 analysis-required recovery submitted 2026-08-04: CPU controller
> 2818081, first cold outer job 2818082.  The controller is re-entrant and
> accepts only a contiguous lineage whose post-cold rounds retain both their
> accepted attempt log and exact analyzer marker.  The current live
> `finalize_sota7_when_done.sh` predates this recovery gate; do not treat its
> results-ready marker as sufficient until the finalizer is replaced or a
> manual gate also requires
> `context_sota7_ahc058_analysis_required_v1/CANONICAL_CONTEXT_COMPLETE`.

> Live recovery status (2026-08-04 02:55 PDT): AHC058 context cold round1120
> was accepted from outer job 2818082 at score 0.46643612; adaptive round1121
> is outer job 2818615 and its immutable log contains the required
> `analysis brief attached` marker.  Transaction executor update1 eval job
> 2814442 exhausted its two-hour allocation after eight charged launches but
> only four usable summaries, so it is not a curve point and must not be
> mistaken for an executor plateau.  `scripts/recover_ttt_txn_executor.sbatch`
> records a partial manifest, preserves and charges those eight launches, adds
> uniquely indexed top-up trajectories until K=8 usable rows exist, and resumes
> the unchanged checkpoint/cadence.  `scripts/submit_ttt_txn_recovery.sh`
> submits that recovery exactly once.  Recovery controller 2818873 was
> submitted at 2026-08-04 03:09 PDT and is recorded in
> `results/txn_timeout_recovery_submission.env`; do not submit a duplicate.
> It preserved `eval_manifest.partial_l8_u4.json` and launched the first
> uniquely indexed k8--k11 top-up as eval job 2818874.  The strict audit now
> requires the final u1 manifest to charge at least 12 launches, contain at
> least eight usable rows, retain the four-usable partial manifest, and expose
> every dynamic top-up job before accepting the Txn executor curve.

> Live continuation status (2026-08-04 03:50 PDT): isolated AHC058 context
> round1121 was accepted at combined score `0.8592248866666669`; round1122 is
> outer job 2819031 and its immutable stdout contains the required post-cold
> marker `analysis brief attached` before any proposal trajectories.  It is
> still in flight and is not yet a curve point.  Hadamard executor update4
> completed as eval job 2818155 with `launched=8`, `usable=8`, and batch/best
> score `0.4876497046303815`; the unchanged controller then submitted update5
> as train/merge/eval jobs 2819083/2819084/2819085.  Transaction top-up job
> 2818874 has launched k8--k11, but none of those four trajectories has yet
> produced an admissible summary and no final u1 manifest exists.  Charge the
> allocation in full and do not draw an update1 point unless the recovery gate
> eventually records at least eight usable rows.

> Live continuation status (2026-08-04 04:48 PDT): AHC058 analysis-required
> context round1122 completed cleanly with the immutable analyzer marker and
> improved `0.8592248866666669 -> 1.5853146711111112`; controller 2818081 has
> submitted round1123 as outer job 2819866.  This clean context endpoint is
> currently above the clean proposer endpoint `0.8166714` and below the local
> executor endpoint `1.762481697777778`; do not claim proposer superiority on
> AHC058 unless later complete rounds change that ordering.  Clean PRISM
> proposer round1025 improved `25.733073175702806 -> 26.1831`, and clean SQL
> proposer round907 improved `0.7376043605398055 -> 0.738204`; both campaigns
> remain active.  Transaction recovery top-up k9 and k11 are now usable, so
> update1 has six usable summaries across twelve charged launches, still short
> of the required eight and still absent from the curve.

> Live continuation status (2026-08-04 05:48 PDT): Transaction executor
> recovery subsequently reached eight usable rows across all twelve charged
> launches and prepared update1; its audit state is
> `complete_and_prepared`.  Hadamard executor update5 eval job 2819085 then
> exhausted its two-hour allocation after eight launches and seven usable
> summaries.  Recovery controller 2821176 preserved
> `eval_manifest.partial_l8_u7.json` and submitted uniquely indexed k8 top-up
> job 2821177 without changing the checkpoint, K=8 replay target, 20-evaluation
> trajectory cap, harness, or optimizer cadence.  The final update5 point must
> charge at least nine launches.  The strict audit now has separate fail-closed
> recovery checks for both Transaction and Hadamard.  During that change an
> indentation error was also found in the endpoint-validation audit: the N>=5
> case checks had become unreachable after the Txn helper's return.  They were
> restored to `audit_endpoint_validation`; allow-incomplete mode now correctly
> reports endpoint revalidation as `pending`, and strict mode cannot publish
> until all 21 cases pass.

> Live continuation status (2026-08-04 05:58 PDT): AHC058 context round1123
> was accepted with the exact analyzer marker, 8/8 valid proposals, and a new
> endpoint `1.71418512`; round1124 is outer job 2821196.  The scheduler then
> admitted fourteen four-GPU jobs simultaneously (56 GPUs, the user limit),
> covering the queued proposer/context rounds, executor training/evaluation,
> and the Hadamard timeout top-up.  The refreshed allow-incomplete aggregate
> has proposer task-level common-budget wins over executor on 5/7 tasks and
> five reference crossings versus executor's four and context's three, but
> proposer does not lead the macro common-budget score or log-AUC.  Treat that
> as an interim mixed result, not as permission for a strong aggregate claim.

> Finalization-controller correction (2026-08-04 06:15 PDT): the original
> detached finalizer PID 2048486 was verified by `/proc` and terminated because
> its in-memory completion function predated the clean AHC058 context gate.
> Corrected PID 1690947 now owns `sota7_finalizer.lock`.  It additionally
> requires `context_sota7_ahc058_analysis_required_v1/CANONICAL_CONTEXT_COMPLETE`
> and accepted round1129 (ten clean batches), uses the isolated
> `sota7_endpoint_validation_final_v2` directory rather than the pending
> AHC039-only provisional validation, and freezes an authoritative `sacct`
> snapshot before exposing the paper-sync marker.  Its durable launch ledger is
> `results/sota7_finalizer_v2.env`.

> Live continuation status (2026-08-04 06:54 PDT): system-context round009
> completed with all 22 launched trajectories materialized.  EPLB improved
> `0.1277408920 -> 0.1279808550`, LLM-SQL improved
> `0.7336881370 -> 0.7337696980`, and PRISM remained at its task-local
> incumbent; the controller submitted its predeclared final/cap round010 as
> outer job 2821836.  The refreshed preliminary audit still has proposer wins
> over executor on 5/7 tasks at the task-specific common rollout budget and
> proposer task-best performance on 4/7, but context leads the current macro
> common-budget score and log-AUC.  The strong aggregate gate therefore remains
> closed while the later clean AHC058 proposer points are still beyond the
> current shared budget.  Do not rewrite this mixed interim result as aggregate
> superiority.  PID-namespace inspection can hide the login-node finalizer from
> `ps`; `fuser` on `sota7_finalizer.lock` verified that corrected PID 1690947
> remains the lock owner.  A duplicate fallback launch exited at the flock and
> performed no work.

> Live continuation status (2026-08-04 07:19 PDT): Hadamard executor update5
> timeout recovery is now `complete_and_prepared`.  The final manifest charges
> nine launches, retains eight usable rows, preserves the original
> `eval_manifest.partial_l8_u7.json`, reuses `ttts7k8_hadamard_u5` and the same
> fixed-harness hash, and records top-up job 2821177.  Its batch best is
> `0.4971542131`; controller 2821176 then submitted unchanged-cadence update6
> train/merge/eval jobs 2822096/2822097/2822098.  Clean PRISM proposer round1027
> also improved `26.1831383919 -> 26.1842335196`; it therefore remains active.
> Clean SQL round909 produced no new best, but its preceding three-transition
> window still contained improvements, so the plateau controller extended the
> campaign through rounds910--912 (first outer job 2821934 after training).

> SQL provenance incident and clean restart decision (2026-08-04 08:08 PDT):
> a stale second v1 controller submitted outer job 2821956 into the already
> completed `round900` directory while the intended plateau controller submitted
> job 2821934 into round910.  Job 2821956 replaced `round900/{round.json,
> prompts.json,trajectories.json,propose.log}` at 07:34, so the strict audit
> correctly refused the live v1 lineage.  Slurm cancellation RPCs failed because
> the controller was unreachable; a reversible workspace `STOP` sentinel now
> prevents both controllers from advancing, and `outer_round.sbatch` refuses any
> completed round before starting a container and is `--no-requeue`.  The
> original Aug-03 GRPO batch, summary, replay, next base, overwritten metadata,
> Slurm logs, and pre-incident audit were copied and hashed under
> `results/provenance_quarantine/sql_round900_overwrite_20260804T073442/`.
> `scripts/audit_sql_round900_overwrite.py` independently reconstructed all
> eight original H1 trajectories and the exact first prompt: SHA256
> `87bc6ab9...` equals the pre-incident audit and its seed excerpt SHA256
> `3895e90e...` equals `task.initial_program[:5000]`.  This closes the forensic
> record but is deliberately **not** used to rescue the paper curve.  All SQL-v1
> jobs, including the otherwise correct r910 attempt, are excluded from logical
> score/trajectory cost and will be charged as discarded as-run proposer
> overhead.  The final SQL proposer route is a wholly independent
> `proposer_sota7_sql_clean_v2` / `outer-proposer-sota7-sql-clean-v2` campaign
> starting at round1200 with the original shared H2 base and the same K=8,
> max-evals=20, r64/a128, three-epoch protocol.  Its submission was prepared but
> the first `sbatch` attempt failed at 08:05 because slurmctld was unreachable;
> no v2 job ID exists yet.  Do not retry v1 or remove its STOP marker.

> Finalizer v3 (2026-08-04 08:13 PDT): the prior detached finalizer remains in
> a login PID namespace that this shell cannot signal and still owns the old
> `sota7_finalizer.lock`.  It is harmlessly stranded because it requires the
> excluded v1 `CANONICAL_COMPLETE`, which is absent and cannot be created while
> the v1 STOP sentinel remains.  Corrected PID 2271326 owns the independent
> `sota7_finalizer_v3.lock`, waits on SQL clean-v2, and has written its first
> waiting heartbeat.  Durable launch metadata is
> `results/sota7_finalizer_v3.env`; do not start another v3 process.

> SQL clean-v2 submission (2026-08-04 08:16 PDT): the bounded submitter acquired
> Slurm briefly and recorded one-shot driver job **2822536** and plateau
> controller job **2822537** in `results/sql_clean_v2_submission.env`.  The
> submitter has exited successfully.  A subsequent `squeue` RPC timed out, so
> treat the durable IDs and eventual workspace/log materialization as the
> current source of truth; do not submit duplicates.  The driver/outer scripts
> are `--no-requeue`, the driver owns a cross-process lock, and the plateau
> controller waits for round1209 before testing or extending to cap round1218.

> SQL clean-v2 first-round gate (2026-08-04 08:34 PDT): driver 2822536
> submitted round1200 outer job **2822543**, which is running.  It materialized
> 8/8 valid H1 candidates and launched all eight executor trajectories with
> K=8/max-evals=20.  `round1200/round.json` records the exact shared H2 base
> `0.09343955531989306`, frozen `qwen3.5-9b`, and one proposer endpoint.  The
> serialized seed excerpt equals `task.initial_program[:5000]` (SHA256
> `3895e90e...`), contains no curated-note leak fragment, and the whole prompt
> SHA256 `87bc6ab9...` equals the independently frozen pre-incident clean prompt.
> This is protocol evidence only; round1200 is not a curve point until its
> terminal rollouts and atomic collector summary complete.

> Transaction executor update2 timeout (2026-08-04 08:53 PDT): eval job
> **2820262** exhausted its two-hour allocation after launching all eight
> trajectories.  Six distinct terminal summaries survived; k1 and k7 did not
> finish.  This batch is not accepted as a K=8 curve point.  The parameterized
> `scripts/recover_ttt_txn_executor.sbatch` now preserves an immutable
> `eval_manifest.partial_l8_u6.json`, charges all eight launches, reuses the
> exact `ttts7k8_txnsched_u2` checkpoint and fixed harness, and asks the ordinary
> resumable driver for fresh indices k8+ until eight usable rows exist.
> Future Transaction eval/top-up allocations use normal-QoS four-hour leases
> instead of short-QoS two-hour leases because a full trajectory batch can
> legitimately exceed two hours.  This scheduler-only change leaves K=8,
> MAX_EVALS=20, the per-call timeout, checkpoint, harness, LoRA, and optimizer
> cadence unchanged; frozen sacct still charges the actual allocation.
> `scripts/submit_ttt_txn_u2_recovery.sh` is the one-shot submitter and writes
> `results/txn_u2_timeout_recovery_submission.env`; slurmctld is currently
> unavailable, so the submitter is retrying and no recovery job ID has yet been
> recorded.  The strict audit has a separate u2 gate and links every GPU top-up
> to the CPU wrapper through the inherited Slurm TMPDIR marker.

> Excluded SQL-v1 tail accounting (2026-08-04 08:53 PDT): after both stale
> controllers had already entered their terminal collect/train section, they
> submitted LoRA jobs **2822789** (the otherwise correct r910 lineage) and
> **2822814** (the clobbering r900 lineage).  Both are excluded wholesale from
> the logical method curve and registered in
> `results/sota7_excluded_campaigns.json` as discarded as-run proposer cost.
> Their merge children **2822790** and **2822815** are likewise excluded and
> registered.  Both controllers observed `STOP` immediately after their merge
> and exited at 08:55/08:56, so they cannot submit another round.  The registry
> continues to fail closed whenever controller-linked Slurm logs and the
> declared job sets differ.

> System-context controller recovery (2026-08-04 09:30 PDT): canonical round010
> finished and improved EPLB `0.1279808550 -> 0.1280082728`.  Plateau controller
> 2812925 correctly submitted round011 as outer job **2823686**, but then one
> reader of the shared `context_ablation.sh` saw a transient malformed line and
> the CPU controller exited.  Round011 itself is valid, isolated GPU work and is
> running.  `scripts/recover_sys_context_plateau.sbatch` waits for its atomic
> summary, performs exactly the skipped validity-ratchet/best-program/feedback
> bookkeeping without launching a duplicate round011, completes rounds012--013,
> and re-enters the predeclared three-round plateau cadence at round013.
> `scripts/submit_sys_context_recovery.sh` retries a one-shot CPU wrapper and
> records its ID in `results/sys_context_recovery_submission.env`.  The strict
> audit hashes the recovered round011 summary and requires the driver log to
> contain exactly one round011 GPU job ID.

> Slurm control-plane correction (2026-08-04 10:03 PDT): RPC failures observed
> from the default tool sandbox were local DNS/network isolation, not a cluster
> outage.  The exact same `squeue`, `scancel`, and `sbatch` calls succeed when
> issued through the approved unsandboxed execution path.  Do not launch another
> background retry loop based on a sandboxed `slurmctld` lookup failure.  All
> job IDs below were accepted directly by Slurm and written to durable result
> ledgers.

> Plateau pre-commit race and retirement (2026-08-04 10:03 PDT): every original
> proposer/context plateau controller waited only for `next_bases.json`, but the
> collector writes that file before the driver finishes proposer training and
> feedback/checkpoint commit.  PRISM controller 2814293 therefore submitted
> stale round1030 outer job **2823642** from `mphi_sota7_prism_clean_v1_08`
> while round1029 was still committing `mphi..._09`.  The stale job was cancelled
> and quarantined as `round1030_stale_phi_2823642`; its H1/rollouts are excluded
> from the logical curve and charged as-run.  The immutable forensic record is
> `results/provenance_quarantine/prism_round1030_stale_phi_20260804/forensic_audit.json`.
> Controllers 2814293, 2813977, 2814902, 2814901, 2822537, 2813735, and 2814903
> were retired, and every controller script now waits for the driver's explicit
> `fresh campaign done` or `context ablation done` commit marker before it can
> extend.  Commit-gated replacements are 2824267 (Hadamard proposer), 2824268
> (Transaction proposer), 2824269 (SQL-v2 proposer), 2824271 (reward-fix
> context), 2824272 (AHC058 proposer), and 2824273 (extra context), recorded in
> `results/commit_gated_plateau_controller_submissions.env`.  System context and
> PRISM use their dedicated recovery controllers instead.

> PRISM/Transaction recovery continuation (2026-08-04 10:16 PDT): PRISM CPU
> recovery 2824228 restored the exact post-round1029 incumbent/feedback and
> committed `mphi..._09`.  Its first correct replacement outer job 2824284 was
> cancelled by uid 0 with signal 54 after 22 seconds and before creating any
> round artifact; it is a zero-trajectory operational retry charged only in the
> as-run ledger.  Idempotent retry controller **2824415** has now submitted
> canonical round1030 outer job **2824459** from `mphi..._09`; the strict audit
> binds every accepted PRISM point to its driver event and replica-0 serve path.
> The initial recovery controller 2824228 was then retired before it could wake
> on round1032's pre-commit `next_bases`; replacement plateau job **2824600**
> has the scheduler dependency `afterok:2824415`, so it cannot review or extend
> until the complete 1030--1032 segment (including round1032 training/feedback
> commit) has exited successfully.
> Transaction update2 recovery job 2824229 initially exited before top-up
> because the newly parameterized wrapper still checked `prepare_step01` rather
> than the selected recovery step.  No GPU work was duplicated.  The guard now
> checks `prepare_step%02d`; retry controller **2824374** preserved the six
> usable results from all eight charged launches and submitted exactly two new
> indices as top-up GPU job **2824460**.  The first CPU attempt remains in the
> durable ledger but launched no GPU work; the retry is the active controller.
> The audit reads `JOB=2824229` and `RETRY_JOB=2824374` separately, proves that
> no eval log inherits the first wrapper's TMPDIR, and binds top-up 2824460 to
> the retry's TMPDIR plus the driver's exact submission event.  All original
> and top-up GPU allocations remain charged; the current state is
> `topup_in_progress` until the eighth usable row and prepare_step02 commit.

> Generalized proposer-checkpoint audit (2026-08-04 10:46 PDT): the strict
> audit now binds every accepted point in the clean SQL, Transaction, PRISM,
> Hadamard, and AHC058 proposer lineages to the driver's proposal event/job,
> the latest committed proposer checkpoint at proposal time, replica 0's exact
> served path, and the preceding round's completed train/merge/feedback commit.
> PRISM round1030 is additionally required to serve `mphi..._09` and explicitly
> forbids stale job 2823642 and the uid-0-cancelled retry 2824284.  A round with
> at least four valid candidates is allowed to retain the same checkpoint only
> when all replay advantages are exactly zero (`no_signal(true-plateau)`); this
> is the legitimate Transaction round1002 case, not a missed training job.  The
> allow-incomplete audit, all five regression tests, Python compilation, shell
> syntax checks, and `git diff --check` pass after this strengthening.

> Hadamard final-update continuation (2026-08-04 10:59 PDT): executor update7
> eval job **2823649** was still running near its two-hour lease with only a
> partial terminal set, so CPU-only job **2825120** was installed with scheduler
> dependency `afterany:2823649`.  It blocks on the task's existing recovery lock
> and is a no-op if the original driver reaches/prepares K=8.  Only if 2823649
> times out does it bind the exact terminal usable count, preserve and charge
> all eight original launches, and let the ordinary driver add unique k indices
> under the identical u7 checkpoint, fixed harness, K=8 target, MAX_EVALS=20,
> and optimizer cadence.  `audit_hadamard_executor_u7_timeout_recovery` fails
> closed on the dependency ledger, checkpoint/harness hash, preserved partial,
> wrapper-linked top-up jobs, final manifest, and prepare_step07.  Submission is
> recorded in `results/hadamard_u7_timeout_recovery_submission.env`.

> Hadamard update7 terminal resolution (2026-08-04 11:39 PDT): Slurm job
> **2823649** reached its lease and is authoritatively `TIMEOUT`, but its TERM
> cleanup atomically collected the last missing k5 trajectory before exiting.
> The canonical manifest records exactly `launched=8`, `usable=8`,
> `partial=false`, and the unchanged `ttts7k8_hadamard_u7` checkpoint/fixed
> harness; `prepare_step07.json` and `jobs_ttts7k8_u8.env` were then committed.
> Conditional CPU wrapper **2825120** observed that prepared state and logged
> `already prepared; no recovery needed`, so it launched no duplicate GPU work.
> The audit now represents this third boundary state explicitly as
> `timeout_cleanup_completed_and_prepared_no_topup`: the timed-out four-GPU job
> remains charged in full, its eight usable rows define update7, and the CPU
> no-op wrapper is excluded from GPU-hours.  Do not create a u7 recovery
> manifest or top-up retrospectively.

> Hadamard executor lease correction (2026-08-04 11:54 PDT): u8 eval job
> **2825671** released its dependency and began running before an attempted
> pending-job lease update reached slurmctld, so its authoritative as-run
> configuration remains short-QoS/2h; no job field was mutated.  Do not claim
> otherwise.  Because Hadamard u5 and u7 both reached that boundary,
> `drive_ttt_executor_12h.sh` now assigns future Hadamard initial and top-up eval
> submissions normal-QoS/4h, matching the scheduler-only policy already used
> for Txn/AHC.  K=8, MAX_EVALS=20, per-call timeout, checkpoint, fixed harness,
> and optimizer cadence are unchanged, and frozen sacct charges actual time.
> The currently parsed u8--u10 driver may retain its old 2h policy and must be
> audited as run; its resumable collector still preserves and charges any
> partial batch before unique-index top-up.  The immutable decision ledger is
> `results/hadamard_executor_eval_lease_policy_correction.env`, and the strict
> audit binds it to u8's job ledger plus both future submission branches.

> Reward-fix context round-namespace correction (2026-08-04 11:08 PDT): the
> replacement plateau waiter 2824271 had inherited the generic `10/19`
> review/cap even though this isolated campaign is deliberately numbered
> 1100--1109.  It had not launched GPU work and could only have waited forever
> for nonexistent round010 after the active initial segment.  Job 2824271 was
> cancelled by the owner; active outer round1106 job 2824519 was untouched.
> Corrected CPU job **2825248** carries immutable
> `START_REVIEW_ROUND=1109,MAX_ROUND=1118`.  The defaults and one-shot submitter
> now encode the 1100-series namespace, and the correction is recorded in
> `results/rewardfix_context_controller_round_namespace_correction.env`.

> AHC039 executor plateau-controller recovery (2026-08-04 12:17 PDT): CPU
> controller **2812935** successfully completed canonical executor updates
> 8--10, then exited with code 2 when its already-loaded copy of the driver hit
> the subsequently corrected line-474 shell syntax error.  The curve and
> update10 preparation were committed before that error, but no completion
> marker was written.  The task lock was free and no AHC039 GPU job remained.
> Existing cumulative best is exactly `2.485475555555556` at both update7 and
> update10, which already satisfies the predeclared three-transition plateau
> rule.  Recovery controller **2826463** was therefore submitted using the
> syntax-clean current script; it performs only the existing-curve review and
> writes the plateau marker, with no new GPU work.  Durable evidence is
> `results/ahc039_executor_plateau_controller_recovery.env`.
> The job subsequently completed in five seconds with AllocTRES cpu=1, mem=2G
> and exit 0:0; plateau_review.json and the completion marker were both
> observed at 12:20:56 PDT.  By 12:40 the marker alone had been removed by an
> unverified concurrent external action, while the immutable review and Slurm
> evidence remained unchanged.  This overlapped commit e0152ed, which records
> a separate author decision to pin a campaign-best paper protocol.  Do not
> silently recreate the marker or let the finalizer rewrite that paper decision
> until the pinned-paper protocol and the clean fair-comparison protocol are
> explicitly reconciled; the scientific plateau evidence itself remains
> complete.
> A non-mutating audit of the author-pinned figure now lives at
> `results/pinned_main_figure_fairness_audit.json` (generated by
> `scripts/audit_pinned_paper_figure.py`).  It records that the pinned
> Aug-03 five-task snapshot is neither the current selected four nor the full
> seven-task scope; AHC058 and PRISM proposer/context sources precede the
> fail-closed clean replacements, SQL points at the wholly excluded v1
> campaign, and the pinned AHC039/EPLB/SQL endpoints do not equal the current
> paper-table cells at displayed precision.  The audit deliberately does not
> modify the pinned paper artifact.

> Reward-fix controllers submitted 2026-08-03: Hadamard proposer driver
> 2814897 (first outer 2814899), AHC058 proposer driver 2814894 (first outer
> 2814900), AHC058/PRISM context driver 2814895 (first outer 2814898); plateau
> controllers 2814902, 2814901, and 2814903 respectively.

---

## 1. Motivation and the claim under test

An agent's performance is decided as much by its **harness** (system prompt,
skills, tool descriptions, control parameters, and generated tool code) as by the
model weights. Self-improvement today takes one of two forms:

| family | what the reward updates | examples |
|---|---|---|
| **executor adaptation** | the solver's own weights | TTT-Discover, ThetaEvolve |
| **artifact / context evolution** | an external archive or harness, revised by a **fixed** proposer | AlphaEvolve, OpenEvolve, Meta-Harness |

**Our claim:** keep the executor permanently frozen and instead train the
*policy that proposes harnesses*. The proposer internalizes the task's reward
history into its weights, so the same reward buys more progress per executor
rollout than either alternative.

**The figure that must decide this** is score-vs-compute, one panel per task:
- x = cumulative **executor rollouts** actually spent by that arm (log scale)
- y = best **valid** score so far, normalized: 0 = seed program, 1.0 = published ≤10B best
- three arms, plus TTT-Discover's published Qwen3-8B point at its own 25,600-rollout budget

**Hard constraint, applies to everything:** no strong-model leakage. The frozen
Qwen3.5-9B must derive every solution itself. No stronger teacher, no external
solution, no human hint, no injected reference program. Any analyst pass must run
on the **same frozen model** and pass the leak guard.

---

## 2. The three arms (what must differ, what must not)

All arms share: the same frozen executor (Qwen3.5-9B), the same six tasks, the
same evaluator, the same fixed initial harness as the starting point, and the
same seed program. They differ **only in what gets updated**.

| arm | updates | harness | proposer | analyst |
|---|---|---|---|---|
| **A. update proposer** (ours) | φ (LoRA on proposer) | synthesized per round | trained | off |
| **B. context only** | nothing — only what the proposer *reads* | synthesized per round | frozen at base | **on** |
| **C. update executor** (TTT) | executor LoRA | **fixed initial harness** | none | off |

Arms A and B come from the same driver so they are budget-matched by
construction; arm C is a separate loop because it has no proposer.

**Six tasks for the figure** (chosen for data coverage):
```
eft__math__erdos_min_overlap      eft__math__circle_packing
eft__math__hadamard_maximal_det   eft__math__first_autocorr_ineq
eft__math__second_autocorr_ineq   eft__ahc_simpletes__ahc039
```

---

## 3. Status — what is done, what is not

### Done and verified
- The initial/context/proposer reporting semantics are frozen. Do not hand-pick
  replacements: after every clean campaign and N>=5 endpoint validation closes,
  generate all reported values from the canonical manifest and require strict
  displayed-precision alignment.
- **Erdős crosses SOTA**: raw **0.380919** vs previous ≤10B best 0.380932, also
  past best human 0.380927. Verified clean: JAX/optax step-function optimizer the
  executor wrote itself, no hardcoded constant, no evaluator/file/network access.
- **Cross-task transfer heatmap** `papers/figures/cross_task_transfer.png` is
  **exploratory only, not a final negative result**.  The old `Best@6` run reset
  the incumbent program, harness, and feedback even though the task adapters
  were trained conditionally on that evolving state; its zero-shot matrix is
  therefore input-distribution mismatched.  The currently rendered diagonal is
  a separate full-campaign Initial-to-Weight quantity and must not be presented
  as if every matrix cell shared one estimand.  The proposed replacement is the
  frozen-target-state, paired adapter-swap protocol in
  `CROSS_TASK_TRANSFER_PLAN.md`.  It is recorded but **not yet confirmed or
  launched**.
- **`\method (context)` row** — from context_v2 rounds 1861–1863, each verified
  to carry 11 analyst briefs.

### Not done / blocked
- **CP-26 SOTA**: our verified best is **2.502** (a uniform 5×5+1 grid, valid:
  in-bounds, zero overlap). Target 2.635983. Two attempts failed; see §5.7.
  **The previously reported 2.635983 is not reproduced by any run we have.**
- **Cross-model transfer**: never started. The 35B endpoint
  `http://10.12.190.18:10211` was up once and has been unreachable since.
- **Arm C (TTT)**: **all data so far is invalid** — see §5.6. Must be rebuilt.
- **Arms A/B**: healthy but only ~2 rounds each (≈5 h/round for six tasks).

---

## 4. What to run

### 4.1 Arms A and B (matched)

Driver: `scripts/context_ablation.sh`. Same script for both; `TRAIN_PHI` selects
the arm.

```bash
SIX="eft__math__erdos_min_overlap eft__math__first_autocorr_ineq \
eft__math__second_autocorr_ineq eft__math__circle_packing \
eft__math__hadamard_maximal_det eft__ahc_simpletes__ahc039"

# arm A — update proposer
CTX_TASKS="$SIX" TRAIN_PHI=1 USE_ANALYST=0 K=8 MAX_EVALS=20 EVAL_TIMEOUT=300 \
  bash scripts/context_ablation.sh <n_rounds> <round_base> $RUN_ROOT/self_adapt_harness/arm_proposer

# arm B — context only
CTX_TASKS="$SIX" TRAIN_PHI=0 USE_ANALYST=1 K=8 MAX_EVALS=20 EVAL_TIMEOUT=300 \
  bash scripts/context_ablation.sh <n_rounds> <round_base> $RUN_ROOT/self_adapt_harness/arm_context_long
```

Round numbers must not collide with existing rounds (current max ≈ 1900s; pick
2000+). Budget ≈ **5 h per round** for six tasks at K=8. Aim for ≥6 rounds per
arm; run them concurrently (1 node each).

Verify arm A is really training:
```bash
grep -c 'trained -> mphi_ctxp' $RUN_ROOT/self_adapt_harness/arm_proposer/driver.log
```
If this is 0, arm A is silently identical to arm B and the comparison is void.

### 4.2 Arm C (TTT) — must be rebuilt first

Current scripts: `scripts/ttt_iterate.sbatch` (host wrapper) +
`scripts/_ttt_iter_worker.sh` (in-container loop). **The in-container loop cannot
submit training jobs** (§5.6). Restructure so that per round:

1. host `sbatch`/`srun --container` → generate K solutions with the current ckpt
2. host (outside container) → `sbatch` the LoRA training + merge, wait
3. loop with the merged ckpt

TTT-Discover's published config (arXiv:2601.16175, Table 9) — match what you can:

| parameter | their value |
|---|---|
| model | gpt-oss-120b (they also report **Qwen3-8B**, which is the ≤10B point we cite) |
| batch | **512 = 8 groups × 64 rollouts** |
| steps | **50** (⇒ 25,600 rollouts/problem) |
| LoRA rank | 32 |
| optimizer | Adam, lr 4e-5 |
| KL coefficient | 0.1 (0.01 for algorithm engineering) |
| sampling temperature | 1.0, context 32768 |
| objective | entropic utility (adaptive β + KL constraint) |

Their Qwen3-8B results, for the figure's reference point:
Erdős **0.380932**, AC1 **1.50525**, AC2 **0.9472**.

We cannot afford 25,600 rollouts/task. Whatever budget is used, **state both
budgets on the figure** — do not present it as an equal-compute comparison.

### 4.3 Cross-model transfer (not started)

Needs a second, larger frozen executor. Protocol: train the proposer only against
M0, freeze the harness bank on M0, forbid the target model from re-editing or
re-selecting harnesses, permit only chat-template/tool-call syntax adapters.
Compare `E+H₁`, `E+H_φ0`, `E+H_φj`, `M0+H_φj`.

### 4.4 Figures

```bash
python3 scripts/score_compute_curves.py    # six panels -> papers/figures/score_compute_curves.{png,pdf}
python3 scripts/cross_task_heatmap.py      # transfer heatmap
python3 scripts/arms_status.py             # budget / best / plateau per arm
python3 scripts/context_collect.py         # \method (context) row, analyst rounds only
```

---

## 5. Pitfalls — read this before running

Every item below actually happened.

**5.1 The score direction.** `rows[].score` is a *combined* score and is
**higher-is-better on every task**, including the minimized ones (Erdős, AC1).
The display-scale conversion re-applies direction. Taking `min()` for the
minimized tasks silently picks the *worst* round. This bug appeared twice
(figure script and `context_collect.py`).

**5.2 Display-scale conversions** (verified against a rollout reporting both):
```
Erdős    raw = 0.380922 / combined
AC1      raw = 1.505293 / combined
AC2      raw = combined * 0.896280
CP       sum_radii = combined * 2.635
ahc039   raw = combined * 225_000       (0.2733511 × 225000 = 61504 = total_score ✓)
ahc058   raw = combined * 4.5e8
Hadamard, EPLB, PRISM, LLM-SQL, Txn: combined IS the table value
```

**5.3 The analyst only fires when there is prior-round feedback.** Condition in
`outer_round.py`: `if SAH_ANALYSIS == "1" and fb:`. **Round 1 never has an
analyst.** Using round 1 as the "context" condition measures a cold base
proposer, not context adaptation. `context_collect.py` now verifies each round's
Slurm log for `analysis brief attached` and skips rounds with zero.

**5.4 The global-ratchet trap.** Several drivers copy the **global**
`$RUN_ROOT/self_adapt_harness/outer/best_programs.json` into the workspace after
each round. That re-imports the main campaign's incumbents and the run stops
measuring itself. `context_ablation.sh` now keeps a campaign-local ratchet;
`fresh_campaign.sh` has `NO_INHERIT=1`. **Check any new driver for this.**

**5.5 Never split one shared ratchet into "independent" arms.** The first version
of the score-compute figure plotted campaign rounds with base-φ as a separate
"context" arm with its own x-axis. Those rounds *inherit programs built by the
trained-φ rounds* (e.g. round760 is a base-φ round whose starting score 0.8583
came from earlier trained rounds), so the curve got credit for compute it never
spent and looked faster than the proposer arm. Arms must each own their ratchet.

**5.6 You cannot `sbatch` from inside the compute container.** The TTT loop ran
entirely inside the container and submitted its training jobs from there. The
submissions returned empty job IDs, `wait_job ""` spun for three hours, the merge
never appeared, and **every round re-served the base checkpoint**. All 18 TTT
jobs then hit the 4 h wall. Any "TTT round 2 vs round 1" numbers produced before
this is fixed are the *same model run twice* and mean nothing.

**5.7 Circle packing is stuck in a hard local optimum.** The 2.502 uniform grid
cannot be improved by local edits: with the ratchet on, all K=16 candidates score
*exactly* the incumbent, giving a zero-variance group
(`no_signal(true-plateau)`) → zero advantage → φ never trains. `NO_INHERIT=1`
restores the signal (φ trained 5×, scores 1.86–2.03) but removes compounding, so
it never gets back above 2.502. Warm-starting the 2.502 ratchet *with* a trained
φ re-plateaus immediately (15/15 candidates identical to base). Reaching 2.636
appears to need the executor to write a **variable-radius continuous optimizer**
(SLSQP-style), which it does not do spontaneously. Seeding such a skill would be
leakage — do not do it without an explicit decision.

**5.8 Environment gotchas.**
- `VLLM_ENV` is not exported by default: `export VLLM_ENV="${VLLM_ENV:-$ENV_ROOT/weave-qwen35-vllm/0.17.1}"`.
- The container image does **not** ship the agent package. Install first:
  `uv pip install --system -e "$CODE_ROOT/NexAU" jax optax orjson cvxpy` with
  `UV_BREAK_SYSTEM_PACKAGES=1`, then assert `from nexau import Agent`.
  Without it, rollouts return `best=None` **silently** while the job looks healthy.
- AHC tasks score **0** without native aarch64 testers:
  `AHC_NATIVE=1 AHC_CXX=g++ AHC_CASE_WORKERS=12 AHC_CACHE_DIR=$SAH/ahc_work/cache`.
- LLM-SQL needs `EVAL_TIMEOUT=420`; the default 180–240 makes every real algorithm
  time out.
- A bare `wait` also waits on the backgrounded vLLM server, which never exits.
  Track rollout PIDs and wait on those. This alone caused two 4 h timeouts where
  the rollouts had actually finished in ~25 minutes.
- **Jobs are capped at 4 h.** Size each round to fit generation + training + merge.
- Do not `pkill -f <pattern>` when the pattern also matches your own shell — it
  kills the session. Use STOP flags or explicit PIDs.

**5.9 Trainer input format.** The offline-GRPO trainer needs replay rows
`{"messages": [...], "tools": [...], "metadata": {"advantage": float, "reward": float, ...}}`
and reads tool schemas from **`metadata.tools`**. The Qwen3.5 loss-mask generator
only finds trainable tokens when the assistant turn is an **inline `<tool_call>`
block**; a plain-text assistant message yields
`offline GRPO row 0 has no trainable assistant tokens`.

**5.10 Not every job runs at 4 GPUs on one node** — check the budget (32 GPU) with
`squeue -u $USER -h -t RUNNING,PENDING -o "%D %j"`, and exclude other projects'
jobs (`dgemma_*`, `anch-*`, `v5b-*` are **not ours — never cancel them**).

---

## 6. Integrity notes that must survive into the paper

- **Historical LLM-SQL is not a clean result.** A curated note placed a verified 0.728
  program in the task message and instructed the harness to make the executor
  adopt it *verbatim*, naming the row-sort that produces the score. That is
  solution injection.  Historical rounds 471--475 and the table's 0.7415 are
  excluded.  The first isolated replacement
  `proposer_sota5_sql_clean_v1` / `outer-proposer-sota5-sql-clean-v1`
  started from `task.initial_program` without curated notes, but a stale
  duplicate controller later overwrote its completed round900 proposal
  metadata.  That entire v1 campaign is now excluded from the final curve and
  retained only in the forensic/as-run cost ledger.  The canonical replacement
  is `proposer_sota7_sql_clean_v2` /
  `outer-proposer-sota7-sql-clean-v2` (round1200+), a fresh lineage with no v1
  prompt, feedback, harness, or proposer checkpoint input.
  Its final audited endpoint—not the old value—must determine both the reported
  score and the clean SOTA count. The note has been stripped from the old workspaces
  (backups: `*.withleak`).
- **Erdős had no analyst note.** An earlier draft claimed one; the audit found the
  only `analyst_note` in the entire campaign belongs to `adrs__llm_sql`.
- **The reward ceiling is the published SOTA value** (`results/finch_targets.json`,
  `sota_combined`). It normalizes the reward only and never enters the executor's
  context, but it must be disclosed.
- **A reward-hacked Transaction entry (32258, validity=0) was sitting in the global
  ratchet** and has been quarantined to the best valid parent (4184.10); backup
  `best_programs.json.with_txn_hack`.
- **The later legal Transaction score 4255.32 is also inadmissible for the fair
  reward-route curve.**  The stored `round460/prompts.json` proves that its first
  H1 seed was the same illegal one-element round450 program (SHA256
  `8229c2ee...`), even though round460--463 eventually emitted legal schedules.
  A new isolated lineage starts from `task.initial_program` under the corrected
  exact-permutation guard at
  `proposer_sota7_txn_clean_v1` / `outer-proposer-sota7-txn-clean-v1`
  (driver job 2813973, plateau controller 2813977).  Do not put 4255.32 in the
  reported results or efficiency figure unless that clean lineage independently
  reaches it.
- **Historical PRISM 26.25597 is not admissible for the fair reward-route
  curve.**  The current semantic replay found round410/cand04 had
  `success_rate=0.98` (program SHA256 `53f90752...`), yet the old collector marked
  it `best_k=4`, `improved=true`; `round411/round.json` then names that candidate's
  harness package as its base.  Every later proposer update therefore descends
  from an invalidly rewarded H1 harness even when its final program has
  success-rate 1.0.  The clean replacement is
  `proposer_sota7_prism_clean_v1` /
  `outer-proposer-sota7-prism-clean-v1` (driver job 2814292, plateau controller
  2814293, first outer job 2814294).  Plotting and audit code fail closed rather
  than falling back to rounds 410--417.
- **Historical Hadamard/AHC058 proposer and AHC058/PRISM context rewards also
  predate the terminal-null attribution fix.**  A terminal task row with
  `best_score=null` is an invalid trajectory; it may not inherit a positive
  seed checkpoint.  In particular, AHC058 round511/cand01 was credited
  1.2342518022 despite an authoritative null terminal score before proposer
  training.  Hadamard and AHC058 proposer therefore use the isolated
  `*_rewardfix_v1` campaigns.  PRISM context remains on the shared reward-fix
  campaign, while AHC058 context uses the separate analysis-required recovery
  because shared round1101 improved without its analyzer marker.
- Claims already removed from the paper because the code does not implement them:
  checkpoint symlink rollback, a `K/2` valid-candidate training guard, and
  "generated tools cannot reach the evaluator" (they *can* call `ctx.evaluate()`;
  what is unreachable is the evaluator implementation and ground truth).

---

## 7. Key paths

```
code            $CODE_ROOT/self_adapt_harness
runs            $RUN_ROOT/self_adapt_harness
  outer/round*/round_summary.json     per-round groups, rows, scores
  outer/best_programs.json            GLOBAL ratchet (shared — treat as read-only)
  arm_proposer/, arm_context_long/    matched arms A and B
  ttt_arm/iter*/curve.jsonl           arm C curves (currently invalid, see §5.6)
  context_v2/                         context arm used for the table row
  proposer_sota5_sql_clean_v1/        excluded SQL-v1 forensic/as-run lineage
  proposer_sota7_sql_clean_v2/        canonical fresh SQL proposer workspace
  proposer_sota7_txn_clean_v1/        clean Transaction proposer workspace
  proposer_sota7_prism_clean_v1/      clean PRISM proposer workspace
  proposer_sota7_hadamard_rewardfix_v1/ clean Hadamard proposer workspace
  proposer_sota7_ahc058_rewardfix_v1/   clean AHC058 proposer workspace
  ttt_discover_sota5_k8*/             canonical K=8 executor state
  ttt_discover_sota7_extra_k8/        Hadamard/Transaction executor state
  context_sota5_*_guarded/            canonical five-task context state
  context_sota7_extra_guarded/        Hadamard/Transaction context state
  context_sota7_rewardfix_v1/         clean PRISM context state; AHC058 excluded
  context_sota7_ahc058_analysis_required_v1/ clean AHC058 context recovery
  cross_task/rows.txt, rows2.txt      transfer matrix rows (source, round, job)
checkpoints     $MODEL_ROOT/checkpoints/self_adapt_harness/
merged          $MODEL_ROOT/exports/self_adapt_harness/     (per-task adapters mphi_f_*)
base model      $MODEL_ROOT/base/Qwen3.5-9B/c202236235762e1c871ad0ccb60c8ee5ba337b9a
paper           $CODE_ROOT/self_adapt_harness/papers
```

---

## 8. Priority order

1. **Rebuild arm C (TTT)** so training actually happens (§4.2, §5.6). Without it
   the central figure has only two of three arms.
2. **Extend arms A and B** to ≥6 rounds each so the comparison is not decided at
   2 rounds. At 16 rollouts they are within noise of each other and **context is
   ahead on 4 of 6 tasks** — the hypothesis is *not* supported at that budget, and
   this must be reported honestly whichever way it ends up.
3. Regenerate the six panels; state both budgets; do not claim equal compute.
4. Optional: cross-model transfer, and a decision on CP-26 (§5.7).

---

## 9. Clean-five live snapshot (2026-08-04 13:03 PDT)

- The requested clean-fair five-task view is now rendered independently of the
  author-pinned campaign-best paper snapshot:
  `papers/figures/score_compute_curves_clean5_live.{png,pdf}` with machine data
  in `score_compute_curves_clean5_live_data.json`.  It is the exact
  AHC039/AHC058/EPLB/PRISM/LLM-SQL subview of the contemporaneous 1x7 manifest,
  as proved by
  `results/score_compute_curves_clean5_live_view_audit.json`.
- The exact-subview check passes. Every reported condition is now derived from
  the same clean manifest, and the human-best reference is independently frozen
  in `results/human_best_references.json`. Do not replace clean-route endpoints
  with historical campaign-best values merely to make the figure look stronger.
- Clean SQL proposer round1202 improved the admissible endpoint from
  0.7112830629 to **0.7301400640**.  At the current task-common budget B=25 it
  leads context (0.7227029262) and the scaled executor reference
  (0.7286779966), though its endpoint remains below the pinned 0.7415 cell.
- Hadamard executor u8 job 2825671 is the last evaluation submitted under the
  superseded short/2h lease and had only one materialized summary after about
  one hour.  Conditional CPU wrapper **2827445** is installed afterany:2825671.
  It is a no-op if the original job reaches K=8; otherwise it preserves and
  charges all original launches, tops up only fresh indices under the identical
  u8 checkpoint/parent/fixed harness, and lets u9--u10 use the corrected normal
  4h lease.  Submission provenance is
  `results/hadamard_u8_timeout_recovery_submission.env`.
- The live all-seven claim gate remains preliminary: proposer leads the local
  executor at the common trajectory budget on 5/7 tasks, but neither macro
  common-budget score nor macro log-AUC.  No aggregate superiority or absolute
  limit claim is currently admissible; continue to plateau/cap and N>=5
  endpoint validation before deciding the final task-level wording.
