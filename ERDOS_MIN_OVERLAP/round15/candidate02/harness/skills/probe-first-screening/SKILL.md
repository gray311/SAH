---
name: probe-first-screening
description: Use probes to screen all h(x) candidates before spending evaluations.
---

# Probe-First Screening
## Budget Strategy - 30 probes available - use ALL to screen - Only 2-3 full evaluations should be needed
## Screening Process For each h(x) from create_piecewise_h: 1. EDIT seed to use that h(x) 2. Call probe_solution 3. If integral != 1 (within 5%) or c5_bound >= 0.37: SKIP 4. If c5_bound < 0.37: KEEP for full evaluation
## Expected Flow - 5 h(x) vectors generated - 5 probe calls (one per vector) - 2-3 pass probe - 2-3 full evaluations - Best result reported
## Why This Works - Probes are cheap (~10s) and don't consume eval budget - Lets you discard bad candidates early - Full evaluations only on promising candidates
