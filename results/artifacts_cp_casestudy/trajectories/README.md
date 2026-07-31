# Complete raw trajectories — CP round300 / cand06

Unedited trajectory files pulled straight from the run
(`outer/round300/…/cand06`). Nothing summarized — these are the actual
proposer and executor traces behind the 0.3642 → 0.7340 case study.

| file | what it is | source |
|---|---|---|
| `proposer_Mphi_chat_cand06.json` | **M_φ (trained proposer) full chat trajectory** — 8 messages: system + task/seed/scores prompt → tool calls (`validate_spec`, `submit_spec`) → the emitted h2spec. This is the harness being designed. | `round300/replay.jsonl` k=6 |
| `proposer_grpo_record_cand06.json` | **GRPO training record** for this rollout: prompt, response, full `trajectory`, `reward=0.3918`, `advantage=0.3652`, `valid=True`, `score=0.7340`, `spec_hash`. | `round300/grpo_batch.jsonl` k=6 |
| `m0_solution_trajectory.json` | **M0 (frozen Qwen3.5-9B) complete solution trajectory** — all 32 steps (kind/edit_mode/edit_note/combined_score/validity/is_new_best), the resource `ledger`, `best_program`, seed/best scores. | `round300/…/cand06/…/summary.json[0]` |
| `m0_best_program_0.734.py` | the winning packing M0 actually wrote (the 0.7340 construction). | extracted from `best_program` |

## What the M0 trajectory shows (32 steps, real)

seed 0.3642 → **5 full_rewrites**, 24 cheap **probes** in between, 5 evaluator
calls total:

```
 0 seed          0.3642   (new best)
 9 full_rewrite  0.6213   (new best)   ← after probes 1-8 ranked variants
13 full_rewrite  0.6399   (new best)
16 full_rewrite  0.6685   (new best)
21 full_rewrite  0.7340   (new best)   ← winner; probe@20 found it first
28 full_rewrite  0.6869                 (explored, kept 0.7340)
```

The 24 probes vs 5 evals is the `probe_reminder` middleware working: M0 ranks
candidates with cheap probes and spends a scarce evaluator call only on a probe
that already beat the incumbent (e.g. probe@20 = 0.7340 → commit@21). Every
improving step is a `full_rewrite`, not a nudge — the `circle-packing-strategies`
skill in action.

## Leakage note

Both traces are the system's own outputs: M_φ is the trained proposer, M0 is the
frozen 9B. No strong-model text enters either — the 0.7340 packing is M0's own
work. Safe to share as-is.
