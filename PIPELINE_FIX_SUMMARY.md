# Pipeline fix summary — 2026-08-05 addendum (sections 12–14 of PIPELINE_FIX_LOG.md)

Three fixes landed on top of the MW/INHERIT/H2OWN/CREDIT/TRAJ/TOOLSEC/FAIR/PROV
change set. Scope: pipeline code only; no paper, figure, or legacy artifact was
modified, and no GPU job was launched.

## 1. MWGATE-001 — middleware gains mechanical authority

**Problem.** A generated `before_model` hook could only inject advisory text.
The AC2 nodes showed the executor ignoring injected imperatives (a probe-first
gate followed by zero probes) — a hook-capability limitation shared by every
route, so gate-style middleware had no real enforcement power.

**Fix.** A hook may now return, instead of a plain string,
`{"note": str?, "require_tools": [tool, ...]?}`:

- The hook stays a pure function; the **trusted wrapper** applies effects.
- `require_tools` arms a session-level gate over
  `probe_solution` / `edit_solution` / `evaluate_solution`: a disallowed tool
  call is refused with a structured message and **consumes no budget**.
- `finish` is never gated; two refusals auto-lift the gate (no hard-locking).
- Full per-middleware accounting: `enforced` / `satisfied` / `refused` /
  `auto_lifted` inside `middleware_audit[name]["gate"]`.
- Malformed dict shapes are hook errors (score-eligibility rules unchanged).
- Hook state gains read-only `active_tool_gate`; the static gate whitelists
  it; the H1 contract (`src/outer/harness/system.md`) documents the return
  shape with an example.

Files: `src/inner/session.py`, `src/inner/harness/tools/discovery.py`,
`src/outer/materialize.py`, `src/inner/harness/middleware/generated_context.py`,
`src/outer/static_gates.py`, `src/outer/harness/system.md`,
`src/inner/run_baseline.py`.

## 2. NOTEGUARD-001 — the note channel can no longer carry a solution

**Problem.** `leak_guard.sanitize` drops marker words (evaluator / target
score), but the historical solution-injection note carried a *program* plus an
adopt-VERBATIM instruction — no marker word at all. A note channel that can
carry code can carry solutions.

**Fix.**

- `leak_guard.code_signals` / `sanitize_note`: a code fence, a line-start
  statement keyword (`def` / `import` / `from` / `class` / `return` /
  `lambda` / `@`), the token `verbatim`, or an over-length note
  (>1500 chars) drops the **whole note fail-closed**. Keywords match only at
  line start, so mid-sentence English ("derived from the run", "a class of
  schedules") is unaffected.
- Wired into the analyst-note path in `outer_round`; dropped notes print
  their named signals.
- **Task-text pinning**: `scripts/build_task_text_registry.py` pins sha256 of
  every task's spec text and initial program from the frozen dataset into
  `provenance/task_text_registry.json` (25 tasks, built). Every round
  verifies the texts it is about to serve and writes
  `task_text_provenance.json`; a mismatch is fatal under
  `SAH_TASK_TEXT_ENFORCE=1`. (`config/` sits on a read-only sub-mount, hence
  the `provenance/` location; `SAH_TASK_TEXT_REGISTRY` overrides the path.)

Files: `src/outer/leak_guard.py`, `src/outer/outer_round.py`,
`src/outer/task_text_registry.py`, `scripts/build_task_text_registry.py`.

## 3. RATCHETMODE-001 — strict_single is enforceable, not conventional

**Problem.** The program-ratchet mode defaulted silently to `legacy_qd`;
a canonical run that forgot the env var would use the wrong inheritance
semantics without any trace.

**Fix.** `program_ratchet_audit.json` records the mode and its source
(`env` vs `default`); `SAH_REQUIRE_STRICT_RATCHET=1` turns any mode other
than `strict_single` into a hard error before the round runs.

Files: `src/outer/outer_round.py`.

## Operational switches

| Env | Effect | Canonical driver |
|---|---|---|
| `SAH_REQUIRE_STRICT_RATCHET=1` | non-strict ratchet mode → hard error | exported |
| `SAH_TASK_TEXT_ENFORCE=1` | task-text mismatch vs registry → hard error | exported |
| `SAH_TASK_TEXT_REGISTRY` | registry path override | default `provenance/…` |
| `SAH_LEAK_NEUTRALIZE` (existing) | note sanitization incl. new code guard | default on |

`scripts/drive_reward_route_inference16_h1.sh` exports both enforcement flags.

## Verification

- `PYTHONPATH=.:src python3 -m unittest discover -s tests`: **73/73 passed**
  (13 new: `test_tool_gate.py` 5, `test_note_injection_guard.py` 4,
  `test_task_text_registry.py` 2, gate cases in
  `test_generated_middleware_runtime.py` 2).
- Wrapper template compiles standalone; `outer_round.py` parses; driver
  passes `bash -n`.
- Registry built from the frozen dataset: 25 tasks pinned, `adrs__llm_sql`
  included.

## Boundaries

- The gate steers the next tool call; it does not (and should not) override
  `finish` or hard-lock the executor.
- The note guard is a text-side defense; generated *tool code* keeps its own
  static/sandbox chain (TOOLSEC-001).
- These fixes change future runs only; legacy artifacts and scores are
  untouched, and the four-task clean rerun remains the standing requirement
  for route-comparison claims (PIPELINE_FIX_LOG §11.6).
