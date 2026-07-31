# Case study — why the score improved: baseline vs evolved harness

**Task:** Circle Packing, n=26 (maximize sum of radii of 26 non-overlapping circles in a unit square).
**Round:** outer/round300, winning candidate `cand06`.
**Result:** M0 climbed **0.3642 → 0.7340** under the evolved harness (breaks Finch-9B 0.7347's neighborhood); the generic baseline harness stalled at ~0.561.

Everything below is real, extracted data. Frozen executor = Qwen3.5-9B; only the
proposer M_φ was trained. The three artifacts:

| # | artifact | files |
|---|---|---|
| 1 | **harness config** (baseline vs evolved) | `1_harness_config.md`, `baseline_agent.yaml`, `evolved_agent.yaml` |
| 2 | **proposer I/O** (M_φ input → the spec it emitted) | `2_proposer_io.md`, `proposer_output_spec.yaml` |
| 3 | **M0 I/O** (the solution trajectory) | `3_m0_io.md` |

---

## The one-paragraph answer

The generic harness told M0 only "optimize the program"; M0 blindly nudged the
seed and stalled near 0.56. The **evolved harness converted the task's geometry
into three concrete aids** — a *tool* that reads the current packing and names
the right lattice, a *skill* that spells out the hexagonal/ring construction for
n=26, and a *middleware* that forces cheap `probe` ranking before spending evals
— plus a **longer, hotter search** (60 iterations, temperature 1.2). With that
scaffolding M0 stopped nudging and started **replacing the whole construction**:
four full rewrites took it 0.36 → 0.62 → 0.64 → 0.67 → **0.73** in five evals.

## What specifically helped — attributed to each change

| harness element | baseline | evolved | how it moved M0 |
|---|---|---|---|
| **new TOOL** `analyze_geometry` | — | reads centers, emits lattice hints ("hexagonal spacing ≈0.557", "16-circle outer ring 0.4/0.6/0.8/1.0") | gave M0 a *named target structure* instead of blind coordinate nudging |
| **new SKILL** `circle-packing-strategies` | generic "optimize" skill | n=26 playbook: hexagonal lattice density π/(2√3), ring counts 1·6·12·18·25, edge effects | told M0 *which construction family* to write, not just to tweak |
| **new MIDDLEWARE** `probe_reminder` (before_model) | generic budget reminder | injects "use probe_solution to rank 2–3 variants before spending an eval" | made the 5-eval budget go far — M0 probed then evaluated only winners |
| **sampling** | temp 0.7 | **temp 1.2** | hotter edits → M0 proposes *structurally different* rewrites, not near-copies |
| **trajectory length** | max_iterations 36 | **60** | more edit→probe→evaluate cycles to iterate the construction |

## The proof it's the harness, not luck

- **M0 is frozen** — identical weights in baseline and evolved runs. The only
  difference is the harness (tools/skill/middleware/sampling/iterations).
- M0's edit mode flipped from *nudge* (generic) to **`full_rewrite`** (evolved):
  every improving step replaced the entire EVOLVE-BLOCK with a new construction —
  exactly what the skill instructed ("write a hexagonal/ring construction").
- Monotonic climb across four rewrites (0.62→0.64→0.67→0.73), 5 evals, 59 LLM
  turns — efficient because the middleware front-loaded cheap probes.

## Honest scope

The improvement is M0's own work: the tool only *reports structure it reads from
M0's own program*, the skill names known packing families (public math, not a
solution), the middleware only schedules probes. No solution, score, or
evaluator internal was injected — the frozen 9B derived the 0.73 packing itself.
