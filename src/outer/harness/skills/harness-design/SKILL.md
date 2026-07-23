---
name: harness-design
description: Design one improved H2 harness spec for a frozen executor LLM on a specific program-discovery task instance. Use for analyzing the task and the current harness's performance on it, forming a mutation hypothesis, drafting an h2spec/0.1 YAML, and validating it with validate_spec before submit_spec.
---

# Harness design (instance-wise)

One tool call per turn: draft a spec, `validate_spec` it, fix what it reports,
then `submit_spec`. Never submit a draft that has not validated cleanly — an
invalid or no-op submission scores the minimum reward.

Read the task first: what does its evaluator reward, what structure does the
seed program have, and where is the current harness's score relative to the
seed? "Stuck at seed" means the executor never found ANY improvement — usually
a method problem (wrong search strategy for this task family), not a sampling
problem. A score well above seed but plateaued suggests exploration or
iteration-budget limits instead.

Form ONE hypothesis about the failure mode on THIS task, then express it
structurally. Strong levers: rewrite the system prompt's *method* section with
a strategy specific to this task family (e.g. for combinatorial constructions:
run a bounded internal search loop inside the per-eval time limit instead of
emitting one fixed construction; for algorithm-speed tasks: name the library
functions worth trying); rewrite the skill playbook around that concrete
strategy; sharpen tool descriptions so the executor stages complete edits;
adjust sampling temperature for more exploration when scores plateau; raise
max_iterations when the eval budget is not being exhausted. A spec that only
nudges one number is usually wasted — prefer coherent bundles (prompt + skill +
sampling) that implement one idea.

Keep every text field self-contained and executor-facing (the executor never
sees your reasoning, only the harness text). Respect the schema caps; include
only fields you change; keep the fixed entry-function/EVOLVE-BLOCK contract and
the evaluation budget untouched (they are not yours to change).

Before submitting, re-read your spec as the executor would: is the method
actionable on a task it has never seen, with 20 evaluations and no memory of
your intent?
