# Qwen-235B × AHC058: skill-mediated transfer

## Matched result

| Field | Initial harness | Evolved harness |
|---|---:|---:|
| Model | Qwen-235B | Qwen-235B |
| Seed | 540001 | 540001 |
| OpenEvolve iterations | 48 | 48 |
| Best iteration | 21 | 42 |
| Combined score | 0.758532476 | 1.343800736 |
| Total evaluator score | 341,339,614 | 604,710,331 |
| Normalized score | 40.2678% | 71.3375% |
| Validity | 1.0 | 1.0 |

The evolved harness improves the matched normalized score by **31.0698
percentage points**.

## What transferred

1. `smart-cascade-search` explains the task's cascade timing and recommends
   early-L0, aggressive-L3, conservative-L3, and balanced policies.
2. `action_analyzer` exposes action-pruning as an external operation. Qwen
   invokes it in the winning proposal.
3. `cascade_search_reminder` fires before every model turn and keeps the
   proposal focused on long-horizon, threshold-aware cascade search.
4. Qwen then generates its own C++ implementation with top-22 candidate
   pruning, four policy simulators, and per-action cross-policy comparison.

The final program explicitly records the interface transition:

```cpp
// Use action_analyzer to get pruned list - replaced with internal heuristic
```

This is evidence of skill-mediated internalization: the tool does not stage the
answer. The model consumes the external component and re-expresses the strategy
inside its own proposal.

## Winning-proposal audit

Proposal `edc3cd56c71a43f79303f2eb02429470` improves its selected parent from
`1.18056742` to `1.3438007356`. It contains five LLM turns, one successful
`action_analyzer` call, one full rewrite, one frozen-evaluator call, and no
invalid result. The skill is present before the first edit, and the middleware
fires on all five model turns.

Across all 48 evolved proposals:

- skill delivery before first edit: 48/48;
- `action_analyzer`: 36 attempts, 36 completions, 0 errors;
- `cascade_search_reminder`: 252 fires;
- probes: 8; formal evaluator calls: 47.

The matched initial arm has 48 proposals and no generated skill, custom tool,
or generated middleware use.

## Files

- `results/`: immutable cell-level result JSON for both arms.
- `programs/`: exact initial- and evolved-arm best programs.
- `evidence/winning_audit.json`: compact structured audit.
- `evidence/winning_trajectory.json`: full model/tool trajectory.
- `evidence/component_frequency.json`: run-level component totals.
- `evolved_harness/`: exact runtime prompt, spec, skill, tool, and middleware.

The +31.0698 pp number is a package-level paired effect. Isolating the numeric
contribution of each component requires a component ablation.
