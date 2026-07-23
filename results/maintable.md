| Model | Erdős (↓) | AC1 (↓) | AC2 (↑) | CP(n=26) (↑) | Hadamard (↑) | ahc039 (↑) | ahc058 (↑) | EPLB (↑) | PRISM (↑) | LLM-SQL (↑) | Transaction (↑) | Avg. (↑) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | 0.385512 | 1.5186 | 0.8801 | 1.172702 | 0.397184 | 553,582 | 134,486,700 | 0.1269 | 22.36 | 0.6858 | 3584.23 | – |
| Finch-9B | 0.381100 | 1.5141 | 0.9122 | 1.936000 | 0.480585 | 553,759 | 525,286,896 | 0.1265 | 23.93 | 0.7024 | 3636.36 | – |
| Qwen3.5-9B + H2 (ours) | 0.456591 | 1.518245 | 0.896091 | 1.477767 | 0.360961† | ‡ | ‡ | 0.126539 | 24.0217 | 0.093440 | 3610.1083 | – |
| Qwen3.5-9B + learned M_phi H2 (ours, campaign) | **0.381274** (r4) | 1.518245° | 0.896091° | 1.800528 (r1) | **0.509002** (r3) | ‡ | ‡ | 0.126539° | 24.0217° | 0.093440° | **3787.8788** (r2) | – |

> **Ours = M0 (Qwen3.5-9B, frozen) + initial H2 (NexAU agent), single seed, GB200.** 20 evaluations/task, except **† Hadamard = 60 evals** (job 2656605; at 20 evals it was stuck at the seed 0.1433).
> **Filled 8 / 11 columns.** Math (5): job 2656067. PRISM / Transaction / LLM-SQL: job 2656677 (imported ADRS tasks, run standalone on CPU; LLM-SQL 0.093 vs official 0.686 is a weak spot — seed scored 0).
> vs official **Qwen3.5-9B**: **beats it on CP (1.478 vs 1.173), AC2 (0.896 vs 0.880), PRISM (24.02 vs 22.36 — also > Finch 23.93), Transaction (3610 vs 3584)**; ~tie on AC1; **behind on Erdős (0.457 vs 0.386) and Hadamard (0.361 vs 0.397, but 60-eval run closes most of the gap from the stuck 0.143)**.
> Caveat: not a strictly matched comparison — official numbers use EFT's own harness/budget; ours is the initial H2 at a fixed budget, single seed (stochastic).
> **EPLB filled** (job 2657027, 20 evals, final): 0.126539 — ≈ official Qwen (0.1269) / Finch (0.1265); the seed alone (0.1262) was already at that level. (Downloaded the workload `expert-load.json` from HF `abmfy/eplb-openevolve`; torch in-container.) 
> **‡ ahc039 & ahc058 — not filled.** The official numbers use SimpleTES's 150-case scoring with **x86 AtCoder tester binaries**; our compute is aarch64. Docker is bypassable (native g++-13 compile + native run both work) and qemu-x86_64 was installed, but the x86 tester **silently fails under qemu-user emulation**. The clean fix (rebuild the two testers natively for aarch64 from AtCoder's Rust `tools`) was deprioritized. ALE-Bench only covers ahc039 (not ahc058) and uses a different scoring scale, so it can't fill these comparably.
> **Campaign row (outer-loop RL, instance-wise):** **(rN) = M_phi 迭代过的任务(round N 的最优候选 H2)**;**° = 尚未迭代,仍是 initial H2 的 20-eval 基线值**。已迭代:CP(r1)、Transaction(r2)、Hadamard(r3)、Erdős(r4);待迭代:AC1(r5 进行中)、AC2、EPLB、PRISM、LLM-SQL。 per-task best from the M_phi iteration (rounds 001-003, 20 evals): CP sum_radii 1.8005 (combined 0.6833, round001/cand01), **Hadamard 0.509 > Finch 0.4806** (round003/cand06), **Transaction 3787.88 > Finch 3636.36** (round002/cand00), **Erdős c5 0.381274 < official Qwen 0.385512** (round004/cand04; Finch 0.381100 — 0.05% away). Campaign targets/status: results/finch_targets.json.
> **9 / 11 columns filled; beats official Qwen3.5-9B on 4** (CP, AC2, PRISM, Transaction) and ties/near-ties on AC1 & EPLB.
> The 5 Algorithmic-Heuristics tasks (affine, convolve2d, polynomial, psd, fft_conv) also ran (job 2656067) but are not columns here.

