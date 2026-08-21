# CP26 · Qwen3.8-27B proposer/executor · 两轮 evolve 正式记录

## 结论

状态：**COMPLETE**。CP26（`eft__math__circle_packing`）已经用 Qwen3.8-27B 完整执行两轮 evolve，并在两轮之间完成一次真实的 27B LoRA/FSDP 权重更新与 full-model merge。

- 初始验证分数：`0.36423689449571406`
- round 0 ratchet 后程序分数：`0.9563198356641971`
- round 1 最终 ratchet 分数：`0.9959631265863883`
- round 1 相对上一轮程序提升：`+0.03964329092219121`（`+4.1454%`）
- 相对初始程序总提升：`+0.6317262320906742`（`+173.4383%`）
- 最终程序：round 1 `cand02`
- 最终程序 SHA-256：`919e3c0265875ebc80f71d12fd2dcbc89b5a804305a992822665096757798911`

这个 CP26 单任务实验给出的方向性证据是正面的：训练后的 proposer 在 round 1 产生了 8/8 合法 proposal、0 次 repair，并找到 `0.9959631266` 的新程序；但它仍然只是一个任务、一个 post-update round，不能单独证明 27B 在更广任务分布上必然优于小模型。

## 模型与运行拓扑

- proposer 与 executor 都是 `Qwen/Qwen3.8-27B`，base revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`。
- frozen executor：`/lustre/fsw/portfolios/av/users/yingzim/model_weights/base/Qwen3.8-27B`。
- round 0 proposer：同一个 frozen 27B base。
- round 1 proposer：7/8 charged slots 使用 round 0 合并后的 27B proposer；第 8 个 slot 是同架构 frozen-base 27B diversity/repair arm。所有 proposer slot 都是 27B。
- round 1 实际更新后 proposer：`update_harness/circle/exports/round00`。
- inference：8×GPU，4 个 vLLM replicas，tensor parallel `TP=2`，每 replica `max_num_seqs=6`，context `49152`，guard safety `512`。
- executor 阶段重新启动 4 个 frozen-base 27B replicas；没有复用训练后 proposer pool。
- 每轮逻辑预算固定为 24 条 agent trajectories：8 proposer + 8 candidate executor + 8 paired same-seed controls；两轮累计逻辑轴 `x=48`。

round 1 的 `runtime/topology.json` 是模型状态解析前写入的静态配置视图，因此 proposer path 仍显示 base。权威执行证据是 `round.json.proposer.checkpoint` 与 `artifact_exports/round001/artifact_index.json.proposal_server_commands`：前三个 TP=2 server 明确加载 `exports/round00`，第四个加载 frozen-base diversity arm；executor 的四个命令全部加载 frozen base。

## Slurm 作业

| 阶段 | parent job | array task | 状态 | ExitCode | Elapsed | GPU |
|---|---:|---:|---|---|---:|---:|
| initialize / 60 tests | 6459930 | — | COMPLETED | 0:0 | 00:01:17 | 0 |
| evolve round 0 | 6459931 | 3 | COMPLETED | 0:0 | 00:48:30 | 8 |
| LoRA/FSDP train + merge | 6459932 | 3 | COMPLETED | 0:0 | 00:31:00 | 8 |
| evolve round 1 | 6459934 | 3 | COMPLETED | 0:0 | 02:47:28 | 8 |

完成标记：

- `update_harness/circle/rounds/round000/ROUND_COMPLETE`
- `update_harness/circle/rounds/round000/training/TRAIN_COMPLETE`
- `update_harness/circle/rounds/round001/ROUND_COMPLETE`

## Round 0：frozen-base 27B proposer + frozen-base 27B executor

Proposal gate：8/8 valid，2 repaired（k0、k6），gate `min6` passed。Candidate 与 paired-control trajectory audits 都是 8 valid / 0 invalid。

| k | candidate | paired control | causal delta | reward | advantage | proposal |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 0.9563198357 | 0.6449133104 | +0.3114065253 | -1.0000000000 | -0.1636618417 | repaired；无 phi credit |
| 1 | 0.8091700643 | 0.7226897384 | +0.0864803259 | +0.3103211779 | +1.1456328916 | valid；causal-credit winner |
| 2 | 0.9218341675 | 0.9882930511 | -0.0664588836 | -1.0000000000 | -0.1636618417 | valid |
| 3 | 0.8349146110 | 0.9394595253 | -0.1045449143 | -1.0000000000 | -0.1636618417 | valid |
| 4 | 0.6733387534 | 0.9527408051 | -0.2794020517 | -1.0000000000 | -0.1636618417 | valid |
| 5 | 0.7345443416 | 0.9863375129 | -0.2517931714 | -1.0000000000 | -0.1636618417 | valid |
| 6 | 0.7534154309 | 0.9108159393 | -0.1574005084 | -1.0000000000 | -0.1636618417 | repaired；无 phi credit |
| 7 | 0.7901050024 | 0.9418434584 | -0.1517384560 | -1.0000000000 | -0.1636618417 | valid |

双轨选择是有意的：训练 credit 选择同 seed 因果赢家 k1；`strict_single` program ratchet 选择绝对程序分数最高的 k0，将可执行程序从 `0.3642368945` 提升到 `0.9563198357`。

## Round 0 → 1：27B LoRA/FSDP 更新

- 训练数据：8/8 bounded replay rows，token budget `18000`，0 dropped，最大 `|advantage|=1.1456328916`。
- Ray/FSDP：world size 8，data parallel size 8。
- LoRA：rank 64，alpha 128；target modules `q/k/v/o/gate/up/down_proj`。
- trainable parameters：`318,767,104 / 27,675,495,664 = 1.1518%`。
- 训练完成 3 个 optimizer steps，无 OOM；每步都保存 512-tensor adapter checkpoint。

| step | loss | KL loss | grad norm |
|---:|---:|---:|---:|
| 0 | 3.7252902985e-09 | -3.2855992232e-11 | 0.0297944956 |
| 1 | 3.7327408791e-05 | 0.0003732199984 | 0.0268378537 |
| 2 | 0.0001028608531 | 0.0010286333491 | 0.0259221122 |

训练被正式分类为 `real_weight_update`。三个 adapter checkpoints 位于 `update_harness/circle/checkpoints/round00/iter_000000{1,2,3}`。最终 adapter 合并成完整 27B 模型：

| merged shard | bytes | SHA-256 |
|---|---:|---|
| model-00001-of-00002.safetensors | 49,825,162,976 | `13d77856e6a5fda2c4c51a598334891dfbe4c2076003af21ac200b7b046df859` |
| model-00002-of-00002.safetensors | 4,888,445,168 | `4c4a5365523d0dcd7472d0f6b45cddf59f73c343726249fcd079272cb8322a3a` |

`merged_manifest.json` 记录 `weights_changed_vs_previous_manifest=true`；merge sanity check 记录 256 个 `lora_B` tensors、`sum|B|=4519.97`。

## Round 1：updated 27B proposer + frozen-base 27B executor

Proposal gate：8/8 valid，0 repaired，gate `min6` passed。前 7 个 proposal 的行为策略为 `trained_phi`；k7 为 frozen-base 27B diversity arm。Candidate 与 paired-control trajectory audits 都是 8 valid / 0 invalid。

| k | candidate | paired control | causal delta | reward | advantage | change / policy |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 0.9567421907 | 0.9563198357 | +0.0004223550 | +0.0095873609 | -0.0738902316 | prompt / trained phi |
| 1 | 0.9563198357 | 0.9563198357 | 0.0000000000 | 0.0000000000 | -0.0820076377 | prompt / trained phi |
| 2 | 0.9959631266 | 0.9789794998 | +0.0169836268 | +0.7758429895 | +0.7367420271 | prompt / trained phi；winner |
| 3 | 0.9710026663 | 0.9723030681 | -0.0013004018 | -0.0463272156 | -0.1210256319 | prompt / trained phi |
| 4 | 0.9563198357 | 0.9573996110 | -0.0010797754 | -0.0251266049 | -0.1032105755 | prompt + skill / trained phi |
| 5 | 0.9644863569 | 0.9563198357 | +0.0081665212 | +0.1851431771 | +0.0782106679 | prompt / trained phi |
| 6 | 0.9563198357 | 0.9563198357 | 0.0000000000 | 0.0000000000 | -0.0820076377 | prompt / trained phi |
| 7 | 0.9628878634 | 0.9721358714 | -0.0092480079 | -0.3275123353 | -0.3528109806 | prompt + generated tool / frozen 27B |

Reward mean/std 为 `0.0714509215 / 0.2969642805`。k2 同时是 causal winner、absolute winner 和 program-ratchet winner；`strict_single` ratchet 从 incoming program `0.9563198357` 推进到 `0.9959631266`。

Proposal-side 的可观察变化：round 0 共记录 67 次 proposer LLM calls 且需要 2 次 repair；round 1 共 60 次 calls、8/8 直接有效、0 repair。它支持“更新后的 27B proposer 在本次 CP26 上更干净且找到了更高分 proposal”的结论，但不构成跨任务统计显著性结论。

## Context-window debug 与恢复披露

round 1 最初有 3 个 paired-control attempts（k2、k3、k6）在 vLLM 的移动诊断边界上失败：`42500 input + 6653 requested output = 49153`，比 `49152` context 多 1 token。失败轨迹没有删除，完整移动到 `round001/failed_rollouts/paired_controls/...`。

恢复只针对这 3 个同 seed、同模型、同程序、同预算的基础设施失败：

| slot | seed | recovered score | eligible | context-guard behavior |
|---|---:|---:|---|---|
| control k2 | 420018 | 0.9789794998 | true | 1 reactive retry，8192 → 5632 |
| control k3 | 420019 | 0.9723030681 | true | 同 seed 并发轨迹自然分叉，未再次触发边界 |
| control k6 | 420022 | 0.9563198357 | true | 2 rejected provider requests，均 8192 → 5632 |

恢复 overlay 只改变 context guard 及其测试；base source snapshot 保持不可变。overlay manifest 记录 base bundle SHA-256 `6c244d4c05c1f05a54f5f8fd884014c51966a231d49ee4da0f7015ad578baef8`，精确容器测试 27 passed。新的 backoff 同时使用 provider limit 与额外 safety token，避免再次卡在一 token 边界。

因此 round 1 的协议逻辑预算仍是 24，但透明披露的实际物理 trajectory attempts 是 27；两轮合计逻辑 48、实际物理 51。正式 collector 只包含每个 slot 唯一的 eligible terminal result，3 个失败尝试保留在 collector root 之外。

另有 evaluator timeout 后的 orphan child 清理。每次操作都经过 UID、PPID=1 与该 Slurm cgroup 精确匹配，记录在 `round001/runtime/manual_interventions.jsonl`；未来运行的 `eval_runner.py` 已改为 process-group cleanup。没有更改任何候选输出或分数。

## Artifact 导航

以下均相对于本次 run root：

- 人读总报告：`artifact_exports/EXPERIMENT_SUMMARY.md`
- 机器读总报告：`artifact_exports/experiment_summary.json`
- 全量逐文件 SHA-256 清单：`artifact_inventory.json`
- round 0 可视化 bundle：`artifact_exports/round000/REPORT.html`
- round 1 可视化 bundle：`artifact_exports/round001/REPORT.html`
- round 0 raw artifacts：`update_harness/circle/rounds/round000/`
- round 1 raw artifacts：`update_harness/circle/rounds/round001/`
- 每个 round bundle 都为 8 个 candidates 保存 proposer exact input/full trajectory/raw submission、生成的 harness、executor exact input/full trajectory/reward/output program、GRPO row、Qwen replay row、paired-control trajectory/reward。
- adapter checkpoints：`update_harness/circle/checkpoints/round00/`
- merged 27B proposer：`update_harness/circle/exports/round00/`
- 最终程序 package：`update_harness/circle/rounds/round001/tasks/eft__math__circle_packing/cand02/`
- 不可变运行源码：`source_snapshot/` 与 `source_snapshot_manifest.json`
- 不可变训练源码：`training_source_snapshot/` 与 `training_source_manifest.json`
- recovery overlay：`recovery_source_snapshots/context_guard_v2/`
- 失败与恢复原始轨迹：`update_harness/circle/rounds/round001/failed_rollouts/`、`paired_controls/` 与 `runtime/control*_infrastructure_recovery.json`
- Slurm accounting 摘要：`artifact_exports/slurm_accounting.tsv`

`artifact_inventory.json` 是完整性入口：它递归列出本次 run root 下的所有普通文件和 symlink，对每个普通文件保存 bytes 与 SHA-256，并按顶层目录汇总数量与体积。
