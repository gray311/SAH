# Artifact 3 — M0 (frozen Qwen3.5-9B) input → output

M0 is the frozen executor. It receives the materialized harness (agent.yaml =
Artifact 1) + the seed program, then runs its edit→evaluate loop. Same weights
in both runs; only the harness differs.

## INPUT to M0
- system prompt + skills (generic vs packing-specific) from the harness.
- tools it may call (baseline: edit/evaluate/probe/finish; evolved: **+ analyze_geometry**).
- the seed program (a weak packing, scores 0.364).
- eval budget 20; middleware messages injected each turn.

## OUTPUT — the solution trajectory

### Baseline harness (generic)
- M0 nudges the seed, no lattice target, no probe discipline.
- **Stalls at ≈0.56** (the "current harness best" the proposer was shown).

### Evolved harness (cand06) — real step trace
```
seed          score 0.3642   <- start (same weak seed)
full_rewrite  score 0.6213   <- BEST   (replaced construction with a lattice)
full_rewrite  score 0.6399   <- BEST
full_rewrite  score 0.6685   <- BEST
full_rewrite  score 0.7340   <- BEST   winner
full_rewrite  score 0.6869            (explored, kept the 0.734)
```
`evaluator_calls = 5 · llm_calls = 59`

## What the trace shows
- **Edit mode changed**: baseline nudges; evolved does `full_rewrite` every
  improving step — M0 *rewrote the whole construction*, exactly what the
  `circle-packing-strategies` skill instructed (write a hexagonal/ring lattice).
- **Monotonic climb** 0.36→0.62→0.64→0.67→**0.73** across four rewrites — the
  geometric target from the tool/skill let each rewrite build on the last.
- **Budget efficiency**: 0.73 reached in only 5 evals because `probe_reminder`
  pushed M0 to rank variants with cheap probes before spending an eval.

## Bottom line
Same frozen 9B. The generic harness → 0.56 plateau; the evolved harness (tool +
skill + middleware + hotter/longer search) → 0.73. The gain is M0 escaping blind
nudging and writing a lattice construction, scaffolded — not solved — by the
harness M_φ designed.
