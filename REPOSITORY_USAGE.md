# SAH 仓库使用与实验复现教程

本文档说明如何在当前 GB200 + Slurm 环境中检查、运行和审计
`self_adapt_harness`。论文实验的统计定义与停止条件以
[`POST_MAIN_RESULTS_EXPERIMENT_PLAN.md`](POST_MAIN_RESULTS_EXPERIMENT_PLAN.md)
为准；本教程只解释如何正确使用代码和保存证据。

## 1. 先区分两类运行

| 运行类型 | 当前入口 | 是否可以直接运行 |
|---|---|---|
| 单轮 pipeline smoke test | `scripts/smoke_test_fixed_pipeline.sh` | 可以；会申请一个 4-GPU 节点 |
| 单任务 proposer campaign | `scripts/run_campaign.sh <config.yaml>` | 可以；先使用新的 workspace 与 round range |
| 11-task × 3-method paper comparison | 见实验计划 P0 | 尚需通过 11-task registry、reference 和 provenance gates |
| State-matched cross-task transfer | 见实验计划 P1 | 尚需实现最终 state-bank protocol |

`scripts/cross_task_transfer.sh` 和早期 reward-routing 脚本保留用于历史探索与
pipeline debugging，不能直接当成最终论文复现入口。

## 2. 集群规则

- 登录节点只用于编辑、轻量测试、查看状态和提交 Slurm job。
- GPU job 必须通过 Slurm 申请；当前 QoS 每个 job 至少使用一个完整的 4-GPU 节点。
- 不在 `/home` 保存数据、模型、环境、checkpoint 或大缓存。
- VS Code/Cursor 只能运行在专用 vscode 节点；不能在 login 节点启动其 server。
- 不把 GitHub、Hugging Face 或 registry token 写进仓库、脚本、日志或 remote URL。
- 数据、模型和实验结果不提交到 Git；只提交小型配置、manifest、汇总和论文需要的审计产物。

完整集群说明位于当前工作区的 `workspace.md`，容器说明位于 `sqsh/readme.md`。

## 3. 工作区和依赖

在当前集群部署中先加载统一环境：

```bash
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
export SAH="$CODE_ROOT/self_adapt_harness"
cd "$SAH"
```

关键路径变量如下：

| 变量 | 内容 |
|---|---|
| `CODE_ROOT` | Git 仓库，以及外部的 NexAU、Weave_v2 |
| `DATASET_ROOT` | EFT/ADRS evaluator 数据 |
| `MODEL_ROOT` | base model、LoRA checkpoints 和 merged exports |
| `ENV_ROOT` | vLLM/Python 环境 |
| `RUN_ROOT` | round、trajectory、manifest 和 score artifacts |
| `LOG_ROOT` | Slurm stdout/stderr |

当前 pipeline 依赖以下未 vendored 资源：

```text
$CODE_ROOT/NexAU
$CODE_ROOT/Weave_v2
$MODEL_ROOT/base/Qwen3.5-9B/<pinned-revision>
$ENV_ROOT/weave-qwen35-vllm/0.17.1
$DATASET_ROOT/self_adapt_harness/
/lustre/fsw/portfolios/av/users/yingzim/sqsh/dgemma-core-aarch64.sqsh
```

提交 job 前做只读检查：

```bash
test -d "$CODE_ROOT/NexAU"
test -d "$CODE_ROOT/Weave_v2"
test -d "$MODEL_ROOT/base/Qwen3.5-9B/c202236235762e1c871ad0ccb60c8ee5ba337b9a"
test -x "$ENV_ROOT/weave-qwen35-vllm/0.17.1/bin/python"
test -r /lustre/fsw/portfolios/av/users/yingzim/sqsh/dgemma-core-aarch64.sqsh
mkdir -p "$LOG_ROOT/slurm"
```

若在另一台机器或另一个账户复现，必须先修改 `workspace_env.sh`、Slurm account、
container image、base-model revision 和 evaluator paths；本仓库不是一个脱离这些外部资源
即可运行的纯 PyPI package。

## 4. 获取和更新代码

首次 clone：

```bash
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
git clone https://github.com/gray311/SAH.git "$CODE_ROOT/self_adapt_harness"
cd "$CODE_ROOT/self_adapt_harness"
git rev-parse HEAD
```

更新已有 checkout 前，先确认没有自己的未提交修改：

```bash
git status --short
git fetch origin
git pull --ff-only origin main
```

不要使用包含 token 的 remote URL，也不要在有未提交实验修改时直接 pull 或 reset。

## 5. 不申请 GPU 的 preflight

### 5.1 Python contract tests

```bash
cd "$SAH"
PYTHONPATH="$SAH/src:$SAH" python3 -m unittest discover -s tests -v
```

测试失败时不能启动新的 canonical experiment。测试数量会随 pipeline contract 增长，
不要在文档或论文中写死某个历史数量。

### 5.2 配置校验

下面命令只解析 YAML、检查未知字段并打印将要导出的环境变量：

```bash
PYTHONPATH="$SAH/src" \
  python3 -m outer.campaign_config "$SAH/config/examples/adaptive_full.yaml"
```

配置中的未知字段会 fail closed。不要为了绕过校验而直接在 shell 中散落未记录的参数。

### 5.3 Slurm 资源检查

```bash
sbatch --test-only scripts/outer_round.sbatch
squeue -u "$USER" -o '%.18i %.12P %.20j %.10q %.2t %.10M %.10l %R'
```

`--test-only` 不占用 GPU，只检查调度请求。Slurm controller 不可用时先等待恢复，
不要把空的 `squeue` 输出误判为 job 已完成。

## 6. 一轮 smoke test

smoke test 使用独立、可丢弃的 namespace，并主动启用严格 program ratchet、task-text pinning
和修复后的 component enforcement：

```bash
source /lustre/fsw/portfolios/av/users/yingzim/config/workspace_env.sh
cd "$CODE_ROOT/self_adapt_harness"

OUT_TAG="smoke-fix-$(date +%Y%m%d-%H%M%S)" \
TASKS=eft__math__second_autocorr_ineq \
K=4 MAX_EVALS=5 \
bash scripts/smoke_test_fixed_pipeline.sh
```

它会提交 `scripts/outer_round.sbatch`，申请 4 张 GPU。检查：

```bash
squeue -u "$USER" -n sah-outer
sacct -X -S today -u "$USER" \
  --format=JobID,JobName%24,State,Elapsed,AllocTRES,ExitCode
```

成功的 round 至少应包含 `round.json`、`trajectories.json`、候选 H2 package、完整
inner trajectories、`round_summary.json`、`grpo_batch.jsonl` 和 provenance/audit 记录。
失败、timeout、invalid、no-op 与 fallback slot 同样必须保留。

## 7. 运行单任务 proposer campaign

### 7.1 建立自己的配置

不要原样运行带有历史 resume checkpoint 的 example。为每条 lineage 创建独立配置、workspace
和未使用过的 `round_base`：

```bash
CFG_DIR="$RUN_ROOT/self_adapt_harness/configs"
mkdir -p "$CFG_DIR"
CFG="$CFG_DIR/ac2_seed0.yaml"
```

建议配置：

```yaml
protocol: sah
task: eft__math__second_autocorr_ineq
rounds: 12
round_base: 1200
workspace: /lustre/fsw/portfolios/av/users/yingzim/runs/self_adapt_harness/ac2_seed0

phi:
  resume_export: null
  resume_ckpt: null

sampling:
  K: 8
  mode: parallel
  max_evals: 20
  eval_timeout: 300
  force_tool_frac: 0.25

reward:
  impl: v3
  hist_lambda: 0.3

analysis:
  enabled: false

training:
  kl_coef: 0.05
  num_epoch: 3
  plateau_rounds: 1
```

`round_base` 是全局 artifact namespace 的一部分，必须与其他运行错开。重复 round ID 可能污染
lineage；completed round 被视为不可变证据，不能覆盖。

### 7.2 校验并启动

```bash
PYTHONPATH="$SAH/src" python3 -m outer.campaign_config "$CFG"
bash scripts/run_campaign.sh "$CFG"
```

`run_campaign.sh` 会启动一个 detached CPU-side controller。controller 逐轮提交：

```text
M_phi + H1 -> 8 candidate H2 packages
frozen M0 + each H2 -> 8 executor trajectories
collect rewards -> proposer replay -> proposer LoRA update -> merge
```

executor 的 base weights 始终冻结。训练的是 proposer LoRA，而不是 executor。

### 7.3 监控、停止和恢复

```bash
WS=/lustre/fsw/portfolios/av/users/yingzim/runs/self_adapt_harness/ac2_seed0
tail -f "$WS/driver.log"
squeue -u "$USER" -o '%.18i %.20j %.2t %.10M %R'
```

请求 controller 在当前安全边界停止：

```bash
touch "$WS/STOP"
```

恢复时使用最后一个完整的 proposer export/checkpoint，选择新的、未使用过的 `round_base`，并在
YAML 中填写：

```yaml
phi:
  resume_export: /path/to/model_weights/exports/self_adapt_harness/mphi_<tag>
  resume_ckpt: /path/to/model_weights/checkpoints/self_adapt_harness/mphi_<tag>
```

不要从只有部分文件的 round 恢复，也不要让两个 controller 写同一个 workspace、feedback file
或 `OUT_TAG`。

## 8. 查看 round 与 trajectory

默认 artifacts 位于：

```text
$RUN_ROOT/self_adapt_harness/outer[-<OUT_TAG>]/roundNNN/
├── round.json
├── prompts.json
├── trajectories.json
├── tasks/<task>/candNN/          # materialized H2 package
├── rollouts/<task>/candNN/       # complete executor trajectory
├── h2_slot_plan.json
├── round_summary.json
├── grpo_batch.jsonl
├── replay.jsonl
└── next_bases.json
```

列出一个 round 的所有 candidates：

```bash
python3 scripts/show_trajectory.py "$ROUND_DIR" <task_id>
```

查看某个 candidate 的 H1 输入、文件操作、提交的 H2、component validation 与 inner rollout：

```bash
python3 scripts/show_trajectory.py "$ROUND_DIR" <task_id> <candidate_index>
```

分析时必须沿同一证据链：

```text
H1 proposal / context brief / weight update
  -> materialized H2 diff
  -> tool/skill/middleware mounted and invoked
  -> executor action and produced program
  -> validated score
  -> ratchet accept/reject
```

只有 proposal 文本、没有 executor trajectory 或 component invocation record，不能用于 case-study
因果归因。

## 9. 三方法 evolution curve 的 canonical setting

完整定义、11-task registry、统计量和停止条件见实验计划 P0。核心预算如下：

| 方法 | 每 batch H1 | 每 batch H2 | 每 batch generated-agent trajectories | 更新对象 |
|---|---:|---:|---:|---|
| Update proposer weights | 8 | 8 | 16 | proposer LoRA |
| Update context | 8 | 8 | 16 | bounded context / external H2 state；weights frozen |
| Update executor weights | 0 | 16 | 16 | executor LoRA；initial H2 fixed |

共同设置：

- 11 tasks，3 paired seeds，19 batches；
- shared display anchor 为 `x=1`，之后为 `17, 33, ..., 305`；
- 三条路线都在 `x=305` 结束；失败和 invalid slot 也计入横轴；
- proposer/executor LoRA 均为 rank 64、alpha 128、3 epochs、LR `3e-5`、KL `0.05`；
- 主统计为 direction-corrected normalized AUC 与 `Score@305`；
- 另报 H2 trajectories、evaluator calls、tokens、wall time 与 allocated GPU-hours。

正式运行前必须完成实验计划 Gate 0。尤其要注意：

1. 当前 generic `context_ablation.sh` 与 `train_ttt_executor.sh` 不能单独证明已满足 final matched protocol；
2. 历史四任务 inference16 controller 只是 pilot/subset；
3. main-result historical best 不能搬到 matched curve endpoint；
4. 任何 task/method/seed 缺失，11-task aggregate 都必须 fail closed；
5. 不允许看到结果后只延长某一方法或替换展示任务。

## 10. State-matched cross-task transfer

最终 cross-task 不是把 source adapter 放到空 target prompt 上跑一次。实验计划 P1 要求：

1. 每个 target task 先用 untrained proposer 构造 3 个 adapter-independent target states；
2. state 固定 task spec、program、score、incumbent H2 和 structured feedback，并冻结 hash；
3. 11 个 source adapters 各用完全相同的 4-round source-training budget；
4. 每个 source-target cell 使用相同 target state，对 trained adapter 与 untrained proposer 做 paired
   Best@8 comparison；
5. 每 cell 使用 3 states × 3 paired seed blocks；不训练、不 ratchet、不跨 cell 继承；
6. 对角线和非对角线使用相同 estimand；full in-task campaign gain 另画一幅图。

现有 `scripts/cross_task_transfer.sh` 使用的是早期 zero-shot initial-state protocol，只能用于
pipeline exploration。最终论文不得用它的 heatmap 支撑 state-matched transfer claim。

## 11. 数据、checkpoint 与 Git 边界

| 内容 | 保存位置 | 是否提交 Git |
|---|---|---|
| source/config/small manifest | repo | 是，审阅后提交 |
| raw/processed evaluator data | `$DATASET_ROOT` | 否 |
| base model | `$MODEL_ROOT/base` | 否 |
| proposer/executor training checkpoint | `$MODEL_ROOT/checkpoints` | 否 |
| merged model export | `$MODEL_ROOT/exports` | 否 |
| round、完整 trajectory、runtime manifest | `$RUN_ROOT/self_adapt_harness` | 否；只提交必要小型审计摘要 |
| Slurm logs | `$LOG_ROOT/slurm` | 否 |

每条 canonical lineage 至少记录 Git SHA、runtime source manifest、task/reference/config/seed registry
hash、base/adapter checkpoint hash、container、Slurm job ID、完整 trajectory counts 和 evaluator version。

## 12. 常见故障

### Job 一直 pending

```bash
scontrol show job <job_id>
sinfo -o '%P|%a|%l|%D|%G'
```

查看 `Reason=`，不要通过重复提交制造多个相同 controller。

### `squeue` 突然为空

必须再用 `sacct -j <job_id> -X` 确认。Slurm controller 短暂不可用时，空输出不代表 job 完成。

### vLLM 启动失败

检查 round namespace 对应的 `vllm-*.log`、container image、base checkpoint 和 4 张 GPU 是否完整
可见。不要在 login node 直接启动 vLLM。

### AHC score 异常为 0

AHC039/AHC058 必须使用 aarch64 native official tester，并保存 tester hash。不能使用在 ARM 上静默
失败的 x86 binary。

### Harness component 被提出但没有生效

依次检查 `agent.yaml` mount、component source file、prompt disclosure、middleware invocation record、
executor trajectory 和 runtime error。tool/skill 可由 executor 决定不使用；middleware 必须挂载并进入
hook，即使合法结果为 `fires=0`。

### 想重跑 completed round

不要覆盖。使用新的 `OUT_TAG`、workspace、round range 和 run manifest；旧 lineage 保留用于审计。

## 13. 主要文档入口

- [`README.md`](README.md)：方法概览与仓库结构。
- [`plan.md`](plan.md)：核心算法与实现规格。
- [`POST_MAIN_RESULTS_EXPERIMENT_PLAN.md`](POST_MAIN_RESULTS_EXPERIMENT_PLAN.md)：三方法曲线、
  cross-task、case study 与 robustness 的冻结实验计划。
- [`PIPELINE_FIX_SUMMARY.md`](PIPELINE_FIX_SUMMARY.md)：pipeline 修复内容。
- [`config/README.md`](config/README.md)：YAML campaign schema。
- [`src/README.md`](src/README.md)：源码模块和数据流。
- [`src/outer/README.md`](src/outer/README.md)：H1 → H2 outer loop。

