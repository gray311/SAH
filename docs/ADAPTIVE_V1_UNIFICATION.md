# Adaptive v1 × SAH unification

This branch keeps current SAH as the substrate and adds Adaptive v1 as an
optional outer-loop protocol. The default `sah` protocol continues through the
existing H1 YAML proposer, reward, and every-round training path.

Port provenance:

- SAH merge base: `907e32a7298dde99337f0088e8c545fa28815cd0`
  (`origin/main` when the merge-ready branch was prepared);
- Adaptive v1 source implementation
  (`harnessopt.py`, `strategies.py`, `evogate_policy_optimizer.py`):
  `dcbc45a2fed3cd7d6700c87a583d85952cfc695c`.

## Agent topology

Adaptive v1 has one bounded read-only analysis stage before candidate
generation. It is isolated from the default SAH protocol:

| role | Adaptive v1 implementation |
|---|---|
| analysis coordinator | Adaptive-only NexAU Agent; invokes both specialists in one turn and emits a schema-checked JSON brief |
| performance analyzer | read-only NexAU subagent for measured outcomes, uncertainty, regressions, and no-ops |
| design analyzer | read-only NexAU subagent for tested fields, invalid patterns, preserved capabilities, and unexplored axes |
| proposer | separate Adaptive NexAU H1, sampled sequentially K times; its SAH task prompt receives only the bounded brief, never the full dossier |
| builder | SAH `ProposeSession` + `merge_with_base`, not another LLM agent |
| validator/dedup | SAH `h2spec/1.0` validator plus deterministic dedup |
| reviewer | SAH static gates plus same-model repair for generated tool code |
| inner executor | a separate frozen NexAU Agent (`M0 + H2`) |

The analyzer team cannot call `validate_spec`, `submit_spec`, task tools,
filesystem, or external services. Runtime injects the same canonical dossier
directly into both child system contexts; it does not trust the coordinator to
copy a long dossier into Agent calls. The coordinator output must use the
fixed `sah.adaptive-v1-analysis-brief/1` schema and may cite only dossier
evidence IDs. Dossier construction preserves a bounded recent window plus any
retained successful-action references, declares an exact known-ID set, and
removes memory IDs that have no groundable evidence row. The round auditor
independently verifies that reference closure.

Runtime structurally sanitizes coordinator JSON before grounding: unsupported
evidence references and malformed/duplicate entries are removed with recorded
warnings, never admitted as facts. If coordinator synthesis is truncated or
otherwise unusable, runtime deterministically validates, de-duplicates, and
caps every usable child JSON summary (4 evidence items, 3 avoids, 3
directions, 3 uncertainties). A single complete child can therefore preserve
its bounded analysis while a truncated sibling is recorded; dossier-only
fallback is used only when no child summary is usable. The merge records
`synthesis=deterministic_subagent_merge` and preserves the coordinator and
nested child traces. Each specialist has a 1,536-token response allowance so
its own bounded JSON can close cleanly; the strict brief validator, rather
than a smaller truncation-prone generation cap, enforces compression.
The tool-free specialists use NexAU's XML final-response mode and an explicit
local sandbox declaration. The coordinator remains in structured mode because
its two subagents are its only tools. This avoids empty structured-tool and
optional-E2B warnings without adding any analyzer capability.

Before the brief reaches the proposer, runtime replaces every selected
free-form performance claim with the dossier's measured validity,
`learning_reward`, `relative_delta`, statistical-positive flag, outcome/SEM,
changed fields, and bounded inner error counts. The controller records only
small categorical outcome telemetry—such as overlap, index error,
invalid/evaluated step counts, edit modes, and generated-tool calls—not full
historical inner trajectories. Equivalent promotion telemetry is retained in
`round_summary.json` for audit and diagnosis, but is deliberately excluded
from the proposer archive so the champion-only channel cannot leak into
learning context. Design directions remain semantic, but their rationale is
deterministically labelled
either supported or exploratory from the cited evidence; unsupported
direction text is also neutralized so words such as
“successful”, “gain”, or “improvement” cannot survive as positive-result
claims. This prevents a high raw score that regressed against its matched
parent from being summarized as a gain. The validator enforces the advertised
4/3/3/3 item caps and 180-character string cap rather than relying on the model
to obey them.

The main proposer is the only analysis/proposal component allowed to call
`validate_spec` and `submit_spec`.

## What is shared

Adaptive reuses these SAH components directly:

- the current `h2spec/1.0` full candidate genome;
- generated tools, skills, and middleware already inherited by SAH;
- `outer.materialize` and the NexAU candidate package layout;
- NexAU `AgentConfig.from_yaml` and `Agent` for analyzers, proposer, and inner
  execution;
- the frozen `inner.harness_runner` and evaluator budget;
- split proposer/executor serving and vLLM lifecycle cleanup;
- the Weave/slime LoRA trainer, merger, and replay encoding.

Adaptive adds no duplicate task registry, evaluator, inner runner, model
service, or candidate filesystem.

Adaptive leaves SAH's fixed H1 package untouched and has its own root package:

```text
src/protocols/adaptive_v1_proposer_harness/
├── agent.yaml
└── system.md
```

That package references SAH's existing validator/submitter tool schemas and
bindings, harness-design skill, submit reminder, generated-code reviewer, and
materializer. A fresh Adaptive NexAU Agent is constructed for each sequential
sample and its complete tool-mediated history is recorded. Runtime overrides
only endpoint/model, timeout, per-sample seed, and thinking-off. Every round
records a hash over the Adaptive proposal runtime, its NexAU package, and all
shared SAH prompt/tool/skill/middleware assets plus validator, materializer,
generated-code gate, and reviewer source it uses.
The analyzer prompt/config, grounding runtime, and tokenizer preflight have a
separate versioned package hash recorded in both `round.json` and
`analysis/<task>/meta.json`. The Adaptive rollout/reward/state-transition
controller has a third version/hash in `round.json`. A fourth
`runtime_package_hash` covers the opt-in worker, inner-runner integration,
materializer dispatch, and replay bridge. An artifact audit can therefore
prove the proposer, analyzer, controller, and executable integration boundary
that produced a transition.
Within one batch, exact spec hashes and normalized intervention families are
both de-duplicated. This rejects repeated prompt paraphrases while leaving the
entire native action surface available to every sample. Exact effective-spec
hashes from earlier rounds are also rejected, while a genuinely different
design may revisit an axis when later evidence justifies it.

The analyzer package is separate again:

```text
src/protocols/adaptive_v1_context_harness/
├── agent.yaml
├── system.md
├── performance_analyzer/{agent.yaml,system.md}
└── design_analyzer/{agent.yaml,system.md}
```

The adapter itself is split along the same boundary:

- `src/protocols/adaptive_v1.py`: small public facade;
- `src/protocols/adaptive_v1_proposal.py`: evidence context and sequential
  Adaptive H1 wrapper;
- `src/protocols/adaptive_v1_analysis.py`: bounded dossier, two-subagent
  execution, strict brief validation, and nested trace artifacts;
- `src/protocols/adaptive_v1_tokens.py`: local Qwen tokenizer preflight;
- `src/protocols/adaptive_v1_controller.py`: reward, frontiers, plateau, commit.

## What remains protocol-specific

| concern | `sah` | `adaptive_v1` |
|---|---|---|
| proposal | existing H1 NexAU Agent emits YAML | separate Adaptive H1 emits native YAML from a compact analyst brief, sequential K sampling |
| per-batch diversity | independent threaded H1 runs | later samples see all prior valid actions |
| action | full/partial H2 YAML | native partial `h2spec/1.0` |
| context | SAH task prompt + feedback | SAH task prompt plus one bounded analyst JSON brief |
| reward | existing SAH v2 group reward | anchored sign-preserving relative credit |
| frontier | next best H2 | separate exploratory working and protected champion |
| proposer update | every accepted step/campaign rule | 3-round confirmed-record plateau + signed contrast |
| final round | campaign-owned | update explicitly skipped because it cannot be used |
| reviewer | SAH generated-code review | the same SAH generated-code review |

Promotion feedback is used only for the champion frontier. It is never copied
into Adaptive proposer context, archive rewards, or training rows.
When an unchanged working or champion harness is reevaluated in the next
matched-repeat round, the controller refreshes that frontier's stored score
from the new base/champion mean. This removes stale contradictions between the
seed-program score and harness score in the next prompt. The remeasurement
does not count as a new proposal, promotion, confirmed record, or positive
training reward; behavior-equivalent candidates remain exactly neutral.

## Isolation guarantee

`--protocol` defaults to `sah`. The original functions and
`src/outer/harness/` remain the default branch in `outer.outer_round`; the
Adaptive module and its two NexAU packages are loaded only after selecting
`adaptive_v1`.

Adaptive accepts the complete behavior surface represented by native
`h2spec/1.0`:
system/meta prompt, skill description/body, built-in tool descriptions,
sampling controls, agent iterations, middleware controls, generated tools,
removed optional tools, generated skills, and generated middlewares.
Each supplied scalar/text field is a whole-field replacement under SAH's
native merge semantics, not a textual patch. The Adaptive H1 therefore asks
for a complete self-contained value whenever it changes a prompt, skill body,
or tool description. It also derives the actual editable boundary from the
task program: imports and helpers inside `EVOLVE-BLOCK` are mutable and must be
restored by a full-block rewrite. These instructions live only in the
Adaptive proposer package; the default SAH H1 remains byte-identical to
upstream.

Every accepted partial spec goes through SAH `parse_and_validate`,
`merge_with_base`, generated-code safety/review gates, and
`outer.materialize`. The result has exactly the SAH NexAU package shape
(`agent.yaml`, `prompt.md`, `spec.yaml`, `tools/`, `skills/`,
`middlewares/`). Generated capabilities are reconstructed from a winning
package and inherited into the next round.
Adaptive compares those inherited `new_*` collections against the actual base
package before assigning `changed_fields`; a prompt-only proposal is therefore
not falsely credited for an unchanged inherited tool, skill, or middleware.
Only capabilities explicitly declared by the current partial spec are
re-reviewed, so an unrelated intervention cannot silently repair or mutate an
inherited tool and contaminate causal attribution. These ratchet semantics are
implemented in the Adaptive session and do not change SAH's historical
`differs_from_base` behavior.
If any declared generated tool or middleware still fails review after repair,
Adaptive rejects the entire candidate. It never materializes a partial
survivor whose prompt or skill may still refer to the dropped capability.
When review successfully repairs tool code, artifacts retain the raw
submission for traceability, but the native Qwen tool-call training target is
rebuilt from the reviewed partial spec that actually produced the rollout.
Positive credit therefore cannot reinforce pre-repair broken code.

Model identity/endpoint, evaluator, task, evaluation budget, ledger,
credentials, data split, and built-in runtime bindings remain protected so
candidate scores stay comparable. `meta.json` remains provenance rather than
an optimization target. Adaptive also rejects generated tool code that uses
private or dynamically resolved context attributes, or aliases/passes the
context object to bypass direct checks: tool implementations may reach the
executor only by using documented public `ctx` capability methods as the
direct receiver. This closes the gap between the protected-invariant contract
in the prompt and the code that is actually accepted, without widening or
modifying the default SAH proposer.

Analyzer dossiers are capped at 18,000 characters / 6,000 conservative tokens
and retain at most eight recent evidence rows. The analyzer input is
preflighted at 9,000 tokens. Main proposer inputs are counted with the actual
local Qwen chat template (including tool schemas) and rejected before model
execution above 23,000 tokens. With a 32,768-token serving window and a
4,096-token proposer output cap, this keeps explicit framework margin.

Those limits apply only to Adaptive's analyzer/proposer path. Native SAH H2
packages declare a 131,072-token context and an 8,192-token output budget, so
the frozen inner executor must still be served with SAH's existing
`--max-model-len 131072` contract. A smaller inner serving window is a launch
configuration error: long iterative H2 trajectories can otherwise pass
Adaptive proposal preflight and later fail at inference. Production SAH
workers already use 131,072; local Adaptive campaigns must fail before
rollouts if the service and package limits do not match.

Each task stores:

```text
analysis/<task>/
├── dossier.json
├── brief.json
├── coordinator_trajectory.json
├── nested_traces.json
└── meta.json
```

The small shared additions are backward-compatible:

- an optional inner request seed (unset for SAH);
- namespaced `ADAPTIVE_V1_DATASET_ROOT`, replay-batch, and source-root
  overrides that are never read by an ordinary SAH invocation;
- an explicit replay batch input whose per-row NeXAU tool schemas are enabled
  only in Adaptive batch mode (the existing `--rounds` behavior remains);
- Adaptive-only long-output cap scaling and nested rollout discovery; and
- Adaptive-only graceful vLLM shutdown/GPU cleanup logging.

The original SAH proposer/reviewer, one-level reward discovery, H1 package,
materializer defaults, Slurm entry file, and vLLM shutdown path are unchanged
when `--protocol sah` is selected or omitted. Adaptive rollout-plan
construction lives in `protocols.adaptive_v1`; the shared worker only invokes
it after the explicit protocol switch.

## Modes

```bash
# Existing SAH campaign; delegates to fresh_campaign.sh.
bash scripts/unified_campaign.sh sah <task> <steps> <round_base> [force_tool_frac] [workspace]

# Adaptive v1; defaults to K=4 and 3 matched outcome/promotion repeats.
bash scripts/unified_campaign.sh adaptive_v1 <task> <rounds> <round_base> [workspace]
```

`round_base` is only the collision-free SAH artifact directory number. Adaptive
context, proposal IDs, generation seeds, plateau timing, and final-round logic
use a separate zero-based protocol round, so a campaign stored in
`round300..round309` still behaves exactly like Adaptive rounds `0..9`.

### Production launch

Run the campaign driver from a login node inside `tmux` (or another persistent
shell). Do not submit `unified_campaign.sh` with `sbatch`: the driver submits
and monitors the outer, trainer, and merge Slurm jobs itself.

The checkout must be available at `$CODE_ROOT/self_adapt_harness`, with the
shared `$CODE_ROOT/Weave_v2` trainer and the model, dataset, run, log, and
environment roots provided by `workspace_env.sh`. A complete launch is:

```bash
tmux new -s adaptive-v1

source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
cd "$CODE_ROOT/self_adapt_harness"

TASK=eft__math__circle_packing
NROUNDS=10
ROUND_BASE=300
WORKSPACE="$RUN_ROOT/self_adapt_harness/adaptive_v1_cp_seed23"

OUT_TAG=adaptive-v1-cp-seed23 \
K=4 \
FORCE_TOOL_FRAC=0.25 \
ROLLOUT_REPEATS=3 \
PROMOTION_REPEATS=3 \
ROLLOUT_SEED=104729 \
PROPOSER_SEED=23 \
PLATEAU_ROUNDS=3 \
CONFIDENCE_Z=1.96 \
LR=3e-5 \
KL_COEF=0.05 \
NUM_EPOCH=3 \
bash scripts/unified_campaign.sh \
  adaptive_v1 "$TASK" "$NROUNDS" "$ROUND_BASE" "$WORKSPACE"
```

Choose a collision-free `ROUND_BASE`, `OUT_TAG`, and `WORKSPACE` for a new
experiment. Artifacts are written under
`$RUN_ROOT/self_adapt_harness/outer-$OUT_TAG/roundNNN`, while campaign state
and the resumable training transaction live in `$WORKSPACE`. To resume an
interrupted campaign, rerun the exact same command with the same task, round
count, round base, output tag, workspace, seeds, and controller settings. The
driver restores the working harness, active proposer adapter, completed
protocol round, and any pending train/merge jobs; it refuses to overwrite an
untracked partial round.

Do not resume a historical `MAX_EVALS=30` Adaptive workspace with this
`MAX_EVALS=20` version. Its evaluator ledger, artifact audit, and source
provenance intentionally fail closed. Start the 20-budget campaign with a new
round range, output tag, and workspace.

The positional arguments differ deliberately:

- SAH: `sah <task> <steps> <round_base> [force_tool_frac] [workspace]`;
- Adaptive: `adaptive_v1 <task> <rounds> <round_base> [workspace]`.

For Adaptive, pass `FORCE_TOOL_FRAC` as an environment variable, not as the
fourth positional argument. `LR`, `KL_COEF`, and `NUM_EPOCH` are inherited by
the shared SAH trainer when a plateau-gated update is required. The trainer
currently fixes LoRA rank/alpha to 64/128, uses four GPUs, global batch size
8, and micro batch size 1. `N_REPLICAS=4`, `PROPOSE_PAR=8`, and
`ROLLOUT_PAR=8` are optional capacity/concurrency overrides.

Useful Adaptive environment knobs:

```text
K=4
FORCE_TOOL_FRAC=0.25
ROLLOUT_REPEATS=3
PROMOTION_REPEATS=3
ROLLOUT_SEED=104729
PLATEAU_ROUNDS=3
CONFIDENCE_Z=1.96
PROPOSER_SEED=23
ADAPTIVE_TOKENIZER_PATH=/path/to/local/qwen3.5
ADAPTIVE_V1_DATASET_ROOT=/optional/local/dataset
```

Adaptive production fixes `MAX_EVALS=20` to match the original SAH evaluator
budget and fixes `EVAL_TIMEOUT=120` as a wall-time and cleanup invariant. Do
not pass either variable in the normal launch command; a conflicting override
is rejected before launch. The rollout plan records both contracts and the
round auditor verifies them. Each evaluator worker also starts in a fresh
process group; the group is terminated after normal completion as well as
timeout so an evaluator cannot leave candidate subprocesses behind. The
delegated default SAH campaign keeps its existing evaluator-budget behavior.

The default `CONFIDENCE_Z=1.96` uses matched-repeat delta uncertainty for
confirmed-record and champion promotion gates. Setting it to zero explicitly
recovers the original fixed-instance Adaptive v1 behavior, but treats every
positive measured delta as sufficient evidence.

`ADAPTIVE_TOKENIZER_PATH` enables exact local chat-template counting for the
Adaptive analyzer/proposer guards. Without it, Adaptive uses a conservative
dependency-free estimate. This environment variable is read only after
`--protocol adaptive_v1`; the shared SAH CLI and default H1 are unchanged.

## State and recovery

The Adaptive state is a task-keyed atomic JSON file containing:

- working and champion packages;
- public outcome attempts and operator statistics;
- pending/replay policy examples;
- confirmed-record plateau counters;
- committed proposer batches and the active adapter;
- an explicit pending-training record when a signed batch has not yet been
  committed.

Campaign startup reads this state through:

```bash
PYTHONPATH=src python -m protocols.adaptive_v1 campaign-status \
  --state <adaptive_v1_state.json> --task <task_id>
```

It restores the next protocol round, working H2, active adapter, and previous
LoRA checkpoint. Existing pending train/merge job IDs are resumed rather than
submitted twice, and partial/untracked artifact rounds fail closed instead of
being overwritten. Before any resumed round or pending training update, the
campaign also requires every collected protocol round to have a successful
`max_eval=20` audit whose H1, analyzer, controller, integration-runtime, and
auditor hashes match the current source, then re-runs the non-mutating round
audit against the live artifacts. A failed, missing, stale, or subsequently
corrupted post-collect artifact therefore cannot be bypassed by restarting
from the already-advanced state.

Collection writes `adaptive_train_batch.jsonl` and a digest-bound manifest
only when training is required. It does **not** claim training succeeded.
After the external SAH trainer and merge finish, the campaign calls:

```bash
PYTHONPATH=src python -m protocols.adaptive_v1 commit-update \
  --state <adaptive_v1_state.json> \
  --manifest <round>/adaptive_train_manifest.json \
  --adapter <merged_mphi> \
  --checkpoint <lora_checkpoint>
```

Only this commit clears pending examples, moves them to replay, resets the
plateau window, and increments `policy_updates`. A failed/interrupted trainer
leaves the controller truthfully uncommitted and blocks collection of a later
round. Commit also verifies the pending manifest/digest and requires a local
adapter directory containing safetensors (plus the checkpoint path when one is
declared), hashes every adapter safetensors shard into both state and the
committed manifest, and rechecks that digest during campaign recovery. A
scheduler success without usable weights—or a subsequently corrupted
adapter—cannot advance or resume state. An idempotent retry of the same commit
is allowed, while replaying an older manifest can never clear a newer pending
batch or rewrite its provenance.

Matched rollout evidence also fails closed: a missing base outcome aborts
collection; when the production `adaptive_rollout_plan.json` exists, every
planned base, valid-candidate, and champion channel must contain exactly the
declared number of completed summaries **and** corresponding completed result
files with a nonempty inner trace, matching finite score, and a ledger whose
declared/used evaluator budget is consistent with the round. A
missing/failed/duplicate rollout is never converted into a policy loss,
allowed to mutate controller state, or replaced with checkpoint/seed evidence.
Champion confidence uses paired promotion deltas because the repeat seeds are
matched. The rollout plan records every channel, package, repeat, and request
seed. Plan generation itself verifies `max_eval=20`, unique output paths, and
positive repeat counts; a planner or rollout process failure terminates the
worker before collection.

After each Adaptive Slurm round, `unified_campaign.sh` runs
`scripts/audit_adaptive_round.py` before accepting `next_bases.json` or
submitting proposer training. The audit reloads every valid native package via
`AgentConfig`, checks the analyzer/outer traces, requires one completed inner
trace per planned rollout, verifies the evaluator ledger stayed at
`max_eval=20`, validates native tool-call training rows, proves each valid
training spec merges to the exact effective harness hash that was rolled, and
cross-checks channel counts, harness paths, paired request seeds, unique output
directories, exact SAH round-directory placement, nonnegative evaluator-call
ledgers, protected seed scores, and per-run provenance against the rollout
plan. It then writes
`artifact_audit_complete.json`. Any failed gate stops the campaign before the
next state transition. The default SAH campaign never invokes this
Adaptive-only audit.

Analysis provenance has a similarly explicit contract. The audit accepts
either a valid coordinator/subagent result, or the protocol's deterministic
dossier fallback with `valid=false`, nonempty recorded model/parse errors, a
recognized fallback synthesis tag, and a brief whose schema and evidence IDs
validate against the stored dossier. It never treats arbitrary failed
analysis as usable context. It also requires the dossier's declared known-ID
set to equal its unique groundable evidence rows and rejects every
optimizer-memory evidence reference outside that set.

## Local validation

No model service or GPU is needed for the protocol suite:

```bash
PYTHONPATH=src python -m pytest -q
for script in scripts/unified_campaign.sh scripts/_outer_round_worker.sh \
  scripts/outer_round.sbatch scripts/train_mphi_step.sh; do
  bash -n "$script"
done
python -m compileall -q src tests
python scripts/audit_adaptive_round.py <completed-adaptive-round> \
  --expected-max-evals 20
git diff --check
```

The tests exercise default-SAH isolation, standalone Adaptive H1 loading,
analyzer topology and hard budgets, canonical child-dossier injection, strict
evidence-ID validation, deterministic fallback, full action-surface exposure,
actual NexAU trace preservation, sequential diversity, generated
tool/skill/middleware inheritance, package parity, dual-frontier selection,
plateau-triggered signed batches, missing-reference fail-closed behavior,
explicit adapter/working-frontier recovery, pending-batch blocking,
final-round skip, native tool-call replay, and the unchanged default SAH
collector.
