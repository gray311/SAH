# Cross-model harness transfer cases

This package contains two matched, full-stack transfer cases from the immutable
`20260814-full-v2` run. Both use Qwen-235B, seed `540001`, 48 OpenEvolve
iterations, active NexAU, and the same frozen executor and evaluator. The only
experimental arm change is the initial versus evolved harness package.

| Case | Initial harness | Evolved harness | Matched effect |
|---|---:|---:|---:|
| AHC058 | 40.2678% of human best | 71.3375% | +31.0698 pp |
| Circle Packing | 68.0023% of human best | 94.9886% | +26.9862 pp |

The cases expose two complementary transfer modes:

- **AHC058: skill-mediated internalization.** The harness supplies a
  cascade-aware search skill, an action-pruning tool, and a persistent
  middleware reminder. Qwen calls the tool, then writes its own C++ search
  procedure implementing top-action pruning and four policy regimes.
- **Circle Packing: tool-mediated transfer.** The harness supplies explicit
  packing guidance, an executable construction tool, an indexing guard, and a
  probe-before-evaluate workflow. The construction tool directly stages the
  complete candidate solver.

Each case includes the initial and evolved result JSON, exact best programs,
the winning proposal audit and full trajectory, the runtime harness component
files, and an aggregate component-frequency JSON. The result JSON files bind
the programs, configuration, evaluator provenance, and runtime compatibility
metadata with SHA-256 hashes.

These paired results identify the causal effect of the evolved harness as a
package. The trajectory makes the mechanism inspectable, but it is not a
single-component ablation and therefore does not assign a numeric causal
effect to an individual skill, tool, or middleware hook.

The archived runs used a documented compatibility migration for legacy
generated-tool bindings. It changed neither the model-visible component
semantics nor the executor source. The relevant runtime metadata and repair
record are retained in the case directories.
