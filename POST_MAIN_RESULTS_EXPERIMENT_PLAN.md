# Main Results 之后的实验计划

状态：**实验设计冻结中；除已提交的 reward-routing controller 外，本文件不授权新 job**  
更新日期：2026-08-05

## 0. 目标

Main results 已经回答了：学习出的 harness 能否让 frozen 9B executor 在 11 个任务上取得强结果。
接下来的实验不再扩充 leaderboard，而集中回答三个 reviewer 最可能追问的问题：

1. **Why update the proposer?** 在相同 inference trajectory 预算下，更新 proposer weights 是否比
   更新 executor weights 或只更新 context 更 sample-efficient，并取得更高的有限预算终点？
2. **What transfers across tasks?** proposer weights 学到的是可迁移的 harness-design policy，还是只在
   单个 task 的 program、harness 和 history 共同演化时有效？
3. **Why harness?** 哪些 prompt、skill、tool、middleware 或 workflow 真正改变了 executor 的行为，
   哪些 proposal 被忽略、执行失败或导致搜索停滞？

本文档将实验分为：

| 优先级 | 实验 | 论文作用 | 当前状态 |
|---|---|---|---|
| P0 | 11-task × 3-method reward-routing evolution curves | 核心 method comparison | 4-task seed-0 subset controller 已提交；其余 7 tasks 尚未提交 |
| P1 | State-matched cross-task transfer | 检验 proposer policy 的可迁移性 | 设计已有，尚未运行 |
| P2 | Clean mechanism case study + component knockout | 回答 why harness / why proposer | 等待 P0 的 clean trajectories |
| P3 | Reward variance、cross-model 等 robustness | 补充与 future-work 边界 | P0--P2 后按预算运行 |

所有实验遵守以下总原则：

- 不从旧曲线拼接点，不把 legacy AC2 八节点当作修复后 pipeline 的因果证据。
- 不因看到结果后替换 task、改变终点或只延长某个方法。
- 保存失败、timeout、invalid、no-op 和未触发的 component；它们都计入成本。
- main table 的 campaign result 与新的 matched-budget result 分开报告，不能为了数值对齐而搬运
  historical best。
- “更高极限”只写成 **higher finite-budget endpoint / observed plateau**；有限轮实验不能证明真正的
  asymptotic limit。

## 1. 三种方法的冻结定义

### A. Update proposer weights（ours）

```text
8 H1 proposer trajectories
  -> 8 candidate H2 packages
  -> frozen executor 各运行 1 条 H2 trajectory
  -> downstream rewards
  -> update proposer LoRA only
```

- proposer 和 executor 从同一个 Qwen3.5-9B base checkpoint 初始化；executor 始终冻结。
- H2 包含 proposer-owned executor system prompt、skills、tools、middlewares、sampling 和 workflow。
- proposer 可读取、修改、新增和显式删除继承的 H2 文件。
- tool/skill 是否使用由 executor 决定；middleware 必须挂载并进入 hook，允许合法地 `fires=0`。
- program 与 H2 分别采用严格、可审计的 ratchet；继承 program 不能冒充本轮发现。

### B. Update context（Self-Harness-style controlled reference）

```text
2 个 frozen analyzer calls（cold batch 后）
  -> bounded analyst brief
  -> frozen proposer 生成 8 条 H1 trajectories
  -> frozen executor 运行 8 条 H2 trajectories
  -> 只更新下一轮可见的 context / external H2 state
```

- proposer weights 与 executor weights 都冻结。
- 与 A 使用相同 H1 action space、H2 文件结构、sampling、seed policy 和 ratchet。
- analyzer 只压缩前一轮 evidence，不训练 analyzer，也不把隐藏答案或 evaluator 实现放入 context。

这个实验是 **Self-Harness-style / context-update controlled reference**，不是官方 Self-Harness
reproduction。图例不能只写 `Self-Harness`，除非后续严格运行其官方实现与公开配置。

### C. Update executor weights（TTT-Discovery-style controlled reference）

```text
fixed initial H2 + current executor
  -> 16 H2 trajectories
  -> task-local PUCT archive + adaptive-beta entropic LOO replay
  -> update executor LoRA only
```

- 不运行 H1 proposer 或 analyzer，H2 固定为 initial H2。
- 每轮更新 executor LoRA；program parent 可由 task-local archive 选择。
- 这是 budget-scaled **TTT-Discovery-style reference**，不是 TTT-Discovery 官方复现。
- published TTT-Discovery 的 25,600-trajectory point 只能作为外部规模参照，不能与本地曲线连接，
  也不能称为 compute-matched endpoint。

### 三种方法共同与不同之处

| 项目 | Proposer weights | Context | Executor weights |
|---|---:|---:|---:|
| 每 batch H1 trajectories | 8 | 8 | 0 |
| 每 batch H2 trajectories | 8 | 8 | 16 |
| 每 batch generated-agent trajectories | 16 | 16 | 16 |
| 更新对象 | proposer LoRA | bounded context/H2 state | executor LoRA |
| executor 是否冻结 | 是 | 是 | 否 |
| proposer 是否冻结 | 否 | 是 | 不存在 |
| H2 是否可演化 | 是 | 是 | 否，固定 initial H2 |
| LoRA rank / alpha | 64 / 128 | -- | 64 / 128 |
| epochs / LR / KL | 3 / `3e-5` / `0.05` | -- | 3 / `3e-5` / `0.05` |

这是一组 **complete reward-routing systems** 的对比，而不是只替换一个变量的 gradient ablation。
两条 H1 route 可以改变 interface，executor route 得到两倍的直接 task-solving trajectories；训练文本和
credit objective 也不同。论文必须同时报告这些差异。

## 2. P0：三方法 evolution curve

### 2.1 核心问题与假设

预注册两个 primary estimands：

1. **Sample efficiency**：direction-corrected normalized best-so-far curve 在共同预算内的 AUC。
2. **Finite-budget performance**：共同终点 `Score@305`。

主要比较是 proposer weights 分别减去 context 和 executor 的 macro paired difference。11 个 task
等权进入 macro 统计；单 task 和 task-family 的胜负作为异质性分析，不要求 11 个 task 全面领先。

支持 “update proposer 更 efficient” 的最低证据标准：

- proposer 的 macro normalized AUC 高于两个 reference；
- paired-seed bootstrap 95% CI 不跨 0；
- raw score、失败率和 cost ledger 没有显示该优势来自漏记失败或不一致预算。

支持 “finite-budget endpoint 更高” 的标准：`Score@305` 的 macro paired difference 为正且 CI 不跨
0。若只在部分 task 为正，正文必须写成 task-dependent，而不是 uniform dominance。

### 2.2 冻结 11-task scope

公平对比覆盖 main results 的全部 11 个 task。四任务 subset 只能用于 pipeline pilot 或紧凑展示，
不能支持总体 method claim。

| Family | Panel | Task ID | Native direction | Human reference（native） |
|---|---|---|---:|---:|
| Mathematical discovery | Erdős min-overlap | `eft__math__erdos_min_overlap` | lower is better | 0.380927 |
| Mathematical discovery | Autocorrelation I | `eft__math__first_autocorr_ineq` | lower is better | 1.5097 |
| Mathematical discovery | Autocorrelation II | `eft__math__second_autocorr_ineq` | higher is better | 0.9015 |
| Mathematical discovery | Circle packing (n=26) | `eft__math__circle_packing` | higher is better | 2.634000 |
| Mathematical discovery | Hadamard max-det | `eft__math__hadamard_maximal_det` | higher is better | 0.935673 |
| Algorithm engineering | AHC039 | `eft__ahc_simpletes__ahc039` | higher is better | 566,997 |
| Algorithm engineering | AHC058 | `eft__ahc_simpletes__ahc058` | higher is better | 847,674,723 |
| System performance | EPLB | `adrs__eplb` | higher is better | 0.1265 |
| System performance | PRISM | `adrs__prism` | higher is better | 21.89 |
| System performance | LLM-SQL | `adrs__llm_sql` | higher is better | 0.6920 |
| System performance | Transaction scheduling | `adrs__txn_scheduling` | higher is better | 2724.80 |

Human reference 只用于 normalization，不进入任何 prompt、analyzer brief、reward 或 model context。
运行前必须把 11 个 task 的 native value、`human_best_combined_score`、display conversion、direction 和
reference source 全部冻结到一个 registry。目前 `results/human_best_references.json` 只有 9 个 task，
缺少 AC1 和 Circle Packing；在补齐并通过 conversion round-trip audit 前，不得启动这两个 task 的
canonical comparison。

七个新增 task 还需要以下 task-specific preflight，但不能改变共同的 `MAX_EVALS=20`：

- AC1：验证 lower-is-better native value 到 higher-is-better evaluator `combined_score` 的转换；
- Circle Packing：固定 n=26 evaluator 与 strict validity check；
- AHC039/AHC058：固定 aarch64-native official 150-case tester 与 tester hash；
- PRISM：固定 strict evaluator；
- LLM-SQL：固定 timeout policy，并禁止 curated note、reference recipe 或 historical program 进入输入；
- Transaction：固定 exact-permutation legality guard，并在 reward 前执行。

### 2.3 共同起点、横轴和终点

- 相同 base checkpoint、task specification、initial program、initial H2 和 evaluator。
- 每条 route 每 batch 固定启动 16 条 generated-agent trajectories，不 top-up。
- 主横轴：

```text
x = cumulative generated agent trajectories (H1 + H2)
x = 1, 17, 33, ..., 305
```

- `x=1` 是 immutable shared display anchor；其 program 不被三个 adaptive route 继承。
- 固定运行 19 个 batches；batch 19 只测量，不进行未被后续评测的 trailing update。
- proposer/executor 均有 18 次 update opportunities，并分别报告 applied/skipped updates。
- timeout、invalid、harness error 和 fallback 都占据原 slot，并计入 x 与成本。
- 三条线必须在同一个 `x=305` 结束；不得截到不同终点后比较 endpoint。

当前 `reward-route-inference16-v1` 只提交了 Erdős、AC2、Hadamard、EPLB 四个 task 的 seed-0
controller；它们是 11-task protocol 的首批 subset，不是完整公平对比。其余 AC1、Circle Packing、
AHC039、AHC058、PRISM、LLM-SQL 和 Transaction 尚未提交。已提交 controller 之后 pipeline 做过
关键修复。
截至本计划写入时，canonical namespace 尚无 `runtime_source_manifest.json`。因此接受数据前必须满足：

1. runtime source snapshot 来自修复后的代码；
2. 每 batch 开始和结束均验证 live code 与 immutable snapshot；
3. 若旧 controller 不能满足，使用新 namespace clean resubmit，不能原地补文件伪造 provenance。

现有 inference16 配置、driver、audit、plot、effect ledger、endpoint collector 和 cost collector 中有多处
四任务静态列表。启动剩余 7 tasks 前必须把这些入口统一改成一个 11-task registry，并加入
fail-closed coverage test：任何 task 在三条 route、19 batches、score conversion、endpoint 或 cost
ledger 中缺失，都使全套 11-task result 不可发布。禁止为七个新增 task 各写无法统一审计的临时脚本。

### 2.4 Replication

- 已提交的四任务 lineage 通过 gate 后只作为对应 task 的 **seed 0 subset**。
- 补齐其余 7 tasks 的 seed 0，然后对全部 11 tasks 另外运行两个完整 paired seed blocks，最终为
  3 independent lineages/task/method。
- 三种方法在一个 seed block 内共享对应的 model、sampling 与 executor seed schedule。
- 最终图显示每个 seed 的细线和跨 seed median 粗线；只有 3 seeds 时不画容易误导的 Gaussian
  standard-error band。
- endpoint 的最终 program 另做至少 5 次 evaluator revalidation；这些 repeats 计入 cost ledger，但不计入
  evolution x-axis。

完整 11-task 单 seed adaptive workload：

| Route | H1 | H2 | Total generated-agent trajectories |
|---|---:|---:|---:|
| Proposer weights | 1,672 | 1,672 | 3,344 |
| Context | 1,672 | 1,672 | 3,344 |
| Executor weights | 0 | 3,344 | 3,344 |
| **合计** | **3,344** | **6,688** | **10,032** |

三 seeds 合计 30,096 条 adaptive generated-agent trajectories，不含 shared anchors 和 endpoint
revalidation。最终共有 `11 tasks × 3 methods × 3 seeds = 99` 条完整 evolution lineages；若每个
lineage endpoint 做 5 次 revalidation，则另有 495 次 endpoint evaluator repeats，单独计费。

### 2.5 Score normalization

主图画相对 human reference 的 direction-corrected gap：

```text
maximize task:  gap_human(%) = 100 * (score - human) / abs(human)
minimize task:  gap_human(%) = 100 * (human - score) / abs(human)
```

- `0%` 表示 human reference，正值表示优于 human，负值表示尚未达到。
- 每个点同时保留 native raw score；统计分析先在 task 内 direction-correct，再做 macro aggregation。
- 每个 panel 可以使用预先冻结的独立 y-range 来显示细小差异，但必须保留 `0%` reference、完整三条线
  和 endpoint 数值，不能裁掉不利点。
- 不能用接近 0 的 native score 直接作为 percentage denominator；此类 task 改用冻结的
  initial-to-reference gap normalization。

### 2.6 Efficiency 与 observed plateau

每个 task/seed/route 输出：

1. normalized AUC over `x=1..305`；
2. `Score@305` 与 endpoint rank；
3. trajectories-to-human-reference，未达到时右删失；
4. valid/invalid/no-op/timeout 比例；
5. 最后 5 个 complete batches 的增益和 evaluator-noise-aware plateau flag。

如果任意 route 在 batch 15--19 仍产生超过该 task revalidation noise threshold 的新 incumbent，说明
`x=305` 尚不能称为 observed plateau。此时对该 task 的 **三条 route、三个 seeds 一起** 延长到同一个
预注册终点（建议 `x=609`），不得只延长 proposer 或只延长较弱 baseline。

### 2.7 Compute fairness ledger

matched trajectory count 不等于 matched compute。必须同时发布：

- H1、H2、analyzer 的 launched/completed/failed counts；
- input/output tokens 和 model calls；
- full evaluator calls、cheap probes 和 timeout；
- training rows、padding rows、epochs、optimizer boundaries；
- proposer/executor pre/post checkpoint hash；
- Slurm job IDs、allocated GPUs、elapsed time 和 allocated GPU-hours；
- serving topology。

至少提供四个横轴的可复算数据：

1. generated-agent trajectories（主图）；
2. task-solving H2 trajectories；
3. evaluator calls；
4. allocated GPU-hours。

如果 proposer 只在第一个轴领先，论文结论必须限定为 generated-agent trajectory sample efficiency，
不能泛化为 FLOP efficiency 或 wall-clock efficiency。

### 2.8 Figure 与表格

完整公平结果图：`3 x 4`（11 个 task panels + 1 个共享 legend/说明位），无装饰性总标题，只保留：

- 11 个 task panel；
- 三条方法曲线；
- 一个共享 legend；
- `human = 0%` 水平线；
- 相同 x 终点和 endpoint label。

若 main paper 版面只能容纳 `1 x 4`，该图必须明确标为 illustrative subset，并同时在 appendix 放完整
11-task figure。所有 aggregate AUC、win count、CI 和论文结论仍使用 11 tasks，绝不能只计算四个
展示 task。

建议图例：

- `Update proposer weights (ours)`
- `Update context (weights frozen)`
- `Update executor weights (TTT-style)`

另给一个 compact table：11 个 task 各自的 AUC、Score@305、trajectory-to-human、失败率和
GPU-hours，并增加 mathematical / algorithm-engineering / systems 三个 family macro 及 11-task macro。
published TTT-Discovery point 若 evaluator 完全可比，可作为没有连线的独立星标放到 appendix。

### 2.9 与 main results 的对齐规则

“对齐”指 condition semantic、task/evaluator、score direction 和 provenance 对齐，不要求不同预算实验得到
完全相同的数值：

- `initial` = fixed initial H2；
- `context` = proposer/executor weights frozen，只改变 bounded context 和 external H2 state；
- `weight` = 只更新 proposer LoRA，executor frozen；
- evolution curve 的 `Score@305` 与 main-result campaign best 分列报告；
- 禁止把 main-result historical best 搬到 clean curve endpoint；
- 若 clean ranking 与 main results 不同，先检查 evaluator/version/seed/program/H2 provenance。确认无 bug 后，
  诚实写成 matched-budget protocol 下的不同结果，而不是隐藏或换 task。

## 3. P1：State-matched cross-task transfer

### 3.1 要回答的问题

主问题不是“把 source adapter 放到一个空 target prompt 上是否有效”，而是：

> 在完全相同、且符合 proposer 正常输入分布的 target-task incumbent state 上，只替换 proposer adapter，
> source-task 训练过的 weights 是否优于 untrained proposer？

旧 heatmap 存在 target state distribution shift、single draw 和 source checkpoint compute 不一致，只能作为
exploration，不能进入 final claim。

### 3.2 Target-state bank

对 11 个 target task 各构造 3 个 adapter-independent states：

- 只用 untrained proposer 做一次标准 cold-start batch；
- 每个 state 固定 task spec、initial/candidate program、score、incumbent H2 和 structured feedback；
- analyzer off，无 proposer update；
- 不从多个 state 中选择最高分；全部 structurally valid states 都保留；
- 在任何 source adapter evaluation 前冻结完整 state bank hash。

State-bank 成本：264 H1 + 264 H2 trajectories。

### 3.3 Source adapters

- 11 个 source task 各训练一个 clean post-fix proposer adapter。
- 每个 adapter 固定 4 rounds，每 round `8 H1 + 8 H2`，配置完全相同。
- 每个 source 因此使用 32 H1、32 H2 和 4 个 update opportunities。
- checkpoint 按预注册 round 选择，不看 transfer 结果，不从 main campaign 挑最优 checkpoint。
- source training 不得访问 held-out target-state bank。

Source-adapter training 总成本：352 H1 + 352 H2 trajectories。

### 3.4 Uniform cell protocol

对 source adapter `phi_i`、target state `S_j,s` 和 paired seed block `r`：

1. 加载完全相同的 target state；不暴露 source program、source H2 或 source feedback。
2. adapter 与 untrained proposer 分别生成固定 8 个 H1 candidates。
3. 每个 candidate 由相同 frozen executor 运行一条 H2 trajectory。
4. 禁用训练、ratchet 和 cell-to-cell inheritance。
5. 使用 3 target states × 3 paired seed blocks，得到每 cell 9 个 paired Best@8 observations。
6. 保存全部八个 score、validity、component mounts/uses、tokens 与 cost，而不只保存 Best@8。

最终矩阵包含 11 个 trained source rows，加一个 untrained baseline。完整 evaluation 为：

- 9,504 H1 trajectories；
- 9,504 H2 trajectories；
- 共 19,008 generated-agent trajectories。

先运行少量预注册 cells 做 pipeline validation，但 pilot 结果不能用于删 task、选 source 或改变 full matrix。

### 3.5 Estimand 与展示

主 estimand 是 paired source-adapter effect over untrained proposer。每个 cell 报告：

- native paired Best@8 difference；
- direction-corrected initial-to-reference-gap effect；
- paired wins/ties/losses；
- hierarchical/bootstrap 95% CI over states and seed blocks；
- valid observations / 9；
- H1/H2 trajectories、tokens 和 GPU-hours。

最终必须拆成两幅视觉：

1. **State-matched matrix**：对角线和非对角线使用完全相同的 adapter-swap estimand。
2. **Full in-task campaign gain bars**：单独显示 initial-to-final campaign gain。

不能为了让对角线“看起来巨大”而把 full-campaign gain 填到 matrix diagonal；两者分别测量 portable
weight effect 与 weights/state/program 的共同演化。

预注册 aggregate：

- diagonal effect；
- within-family off-diagonal effect；
- cross-family off-diagonal effect；
- source adapter row mean；
- target sensitivity。

无论结果如何都可形成清楚结论：

- diagonal 强、off-diagonal 弱：学习主要 task-specific；
- 同 family transfer 为正：学习到 family-level harness policy；
- 广泛 off-diagonal 为正：支持 reusable proposer；
- 全部接近 0/负：收益主要来自 task 内 weights、program、H2 与 history 的 co-adaptation。

当前 conclusion 中“zero-shot cross-task transfer is negative”在该实验完成前不能作为已验证结论；应先
删除或标为 preliminary，最终按 state-matched 结果重写。

### 3.6 可选的 stronger transfer test

如果 pairwise transfer 弱，但我们仍想检验跨任务 amortization，可预注册一个新的实验：

- leave-one-task-out pooled proposer；
- 在 10 个 source tasks 上以完全相同总更新预算训练；
- 在 held-out target state bank 上与 compute-matched untrained/multitask controls 比较。

这是新的 multi-task learning claim，不能用来改写 pairwise adapter transfer 的结果，且优先级低于完成
11×11 state-matched matrix。

## 4. P2：Clean mechanism case study

### 4.1 冻结 task

- **AC2**：主要回答 why update proposer；观察 context 的一次性 instruction 与 proposer preference
  是否形成不同的持续行为。
- **EPLB**：主要回答 why harness；观察能改变诊断/search interface 的 H1 routes 与 fixed-H2
  executor update 的差别。

这两个 task 已在 clean curve 结果前确定。若新 lineage 不再展示预期机制，仍报告 null/contrary case，
不能事后替换成最有利 task。其他 task 只进 appendix audit。

### 4.2 每个 node 必须保存的 artifact

```text
task spec + exact evaluator/version
incoming agent.yaml / prompt.md / component source files
H1 full conversation and every file read/write/delete action
parent -> child H2 structured diff and canonical package hash
H2 full executor conversation
tool calls/results; skill loads; middleware mounts/invocations/fires/errors
seed program, output program, hashes, raw and validated scores
analyzer brief and exact next-round prompt (context route)
pre/post checkpoint, replay rows and advantages (weight routes)
job ID, tokens, evaluator calls, timeout/error state
```

只保存 proposal text 不够；必须证明 component 被 materialize、挂载，并在 trajectory 中实际参与或被
executor 明确选择不使用。

### 4.3 Event chain

每个标注必须沿同一条证据链：

```text
proposal / analyzer brief / weight update
  -> materialized harness or fixed interface
  -> executor actually did ...
  -> program changed / no-op / invalid
  -> validated result
  -> accepted or rejected by ratchet
```

统一标签：

- `IMPROVE`：新 program 超过 incoming incumbent，且 provenance/validation 全部通过；
- `DROP`：raw candidate 或 complete batch 低于起点；best-so-far 曲线仍保持单调；
- `BLOCK`：至少两个连续 batches 重复同一失败族，且实际 trajectory 支持这个判断；
- `NOT ENACTED`：提议存在，但 tool/skill 未被 executor 使用或 middleware 合法地 `fires=0`；
- `INVALID`：component/runtime/program 失败，不能发布 score；
- `UNATTRIBUTABLE`：score 变化存在，但 program/H2/seed credit chain 不完整。

自然 campaign trace 只能写 “consistent with”。若要写 “component X caused the gain”，必须做下面的
controlled knockout。

### 4.4 Harness component knockout / replay

对每个 clean winning H2，固定：

- target state、seed program 和 evaluator；
- frozen executor checkpoint；
- decode seeds、temperature、token/evaluator budget；
- 除被测 component 外的全部 H2 bytes。

比较：

1. parent H2；
2. full winning H2；
3. minus tool；
4. minus skill；
5. minus middleware；
6. prompt-only diff（适用时）。

每个 condition 至少 5 paired repeats。报告 final score、trajectory validity、probe/full-eval allocation、
component use 和 program-family change。若 tool 从未被调用，结论是 proposer 提出了但 executor 未采用，
不能把自然曲线的提升归因于该 tool。

### 4.5 展示

- 主文放一张简洁的 multi-panel static figure：每个 panel 一个关键 node，三方法共享小型 evolution
  context，右侧只写 `Proposed / Actually used / Result`。
- HTML 放完整可交互 evolution：按 batch 播放，点击 node 展开 H1/H2 conversation、H2 diff、component
  invocation 和 program diff。
- 旧 AC2 八节点保留为 debugging history，不进入 clean causal figure。

## 5. P3：Robustness 与扩展实验

### 5.1 Harness reward variance

当前一个 harness 通常只由一条 executor trajectory 估计 reward，方差可能较大。在相同每-round H2
trajectory 预算下比较：

- 8 harnesses × 1 executor rollout；
- 4 harnesses × 2 executor rollouts；
- 2 harnesses × 4 executor rollouts。

在 AC2、Hadamard、EPLB 上各跑 3 seeds，保持总 H2 trajectories、训练配置和 evaluator budget 相同。
报告 harness ranking stability、reward variance、effective training groups 和 final score。这个实验决定
“breadth of harness search” 与“更可靠地估计少量 harness”之间的 trade-off。

### 5.2 Cross-model harness transfer

冻结 proposer checkpoint 和最终 H2，不再训练，在一个更大但仍 frozen 的 executor 上测试：

- initial H2 vs learned H2；
- small-executor-discovered H2 在 larger executor 上是否仍改善；
- evaluator、program seed 和 trajectory budget 保持相同。

该实验回答 harness artifact 是否跨 executor 可复用；它不等同于 proposer weights 的 cross-task
transfer，单独成节。

### 5.3 官方 baseline reproduction（可选）

若时间允许，可另跑官方 TTT-Discovery 或 Self-Harness code。但由于模型、batch size、action space 或
training objective 可能无法完全匹配，官方 reproduction 应单列：

- 官方设置结果；
- 本地 controlled reward-routing 结果；
- published result。

不得用官方远端 endpoint 替换本地 matched curve 的某一个点。

## 6. 执行顺序与停止条件

### Gate 0：代码与 provenance

- [ ] `60/60` unit tests 继续通过。
- [ ] 11-task static protocol audit 通过；每个 task 都有三条 route、19 batches 和共同终点。
- [ ] 每个新 run 在第一条 trajectory 前写 immutable runtime source manifest。
- [ ] H2 inheritance、middleware participation、trajectory retention 和 program credit smoke test 通过。
- [ ] 冻结 task/reference/config/seed registry 的 hash。

### Milestone 1：P0 seed 0（11 tasks）

- [ ] 审计现有 submitted controller 是否真正从 post-fix snapshot 启动。
- [ ] 把现有四任务 subset 作为 pipeline/provenance pilot，而不是 final scope。
- [ ] 完成其余 7 tasks 的 reference registry、evaluator 和 legality preflight。
- [ ] 11 tasks × 3 methods 全部到相同 `x=305`。
- [ ] 生成 curve data、effect ledger、cost ledger 和 endpoint revalidation。
- [ ] 不满足 provenance 的 lineage 整体作废并换 namespace clean rerun。

### Milestone 2：P0 replication 与 paper figure

- [ ] 对全部 11 tasks × 3 methods 完成另外两个 paired seeds。
- [ ] 冻结 macro AUC 与 Score@305 analysis。
- [ ] 生成最终 11-panel figure、compact result table 和 compute table。
- [ ] 若另做 `1 x 4` main-paper view，明确标记为 illustrative subset，统计仍使用全部 11 tasks。
- [ ] 根据预注册 plateau rule 决定是否对某个 task 的三条 route 一起延长。

### Milestone 3：P1 cross-task

- [ ] 构造并 hash target-state bank。
- [ ] 训练 11 个 matched source adapters。
- [ ] 先做 pipeline-only pilot，再完成 11×11 matrix。
- [ ] 输出 state-matched matrix 与 separate in-task campaign gain bars。

### Milestone 4：P2 mechanism

- [ ] 从 clean P0 lineage 生成 AC2/EPLB event manifest。
- [ ] 人工核对每个 proposal → enactment → program → score 链条。
- [ ] 运行 component knockouts。
- [ ] 生成简洁 static figure 与完整 HTML artifact explorer。

### Milestone 5：论文同步

- [ ] reward-routing 正文改成 16-trajectory、r64、3-epoch canonical setting。
- [ ] TTT-Discovery-style 与 Self-Harness-style 的措辞准确，不写成官方 reproduction。
- [ ] main result、matched curve、cross-task、case study 的数值与 estimand 分开。
- [ ] cross-task conclusion 只使用 state-matched final result。
- [ ] 所有图、表、正文数值都能回溯到 immutable manifest 和 revalidation record。

## 7. 最终希望支持的论文表述

如果实验结果通过上述 gate，最强但仍准确的表述是：

> Under the same number of generated test-time agent trajectories, routing reward into a
> harness proposer yields higher sample efficiency and a stronger finite-budget endpoint
> than a frozen-weight context route and a budget-scaled executor-update reference on the
> full eleven-task suite. The advantage is explained by inspectable changes to the search
> interface—tools, skills, middleware, and workflow—rather than by silently adapting the
> executor.

如果只有部分任务领先，则改成：

> Updating the proposer is most effective when the bottleneck lies in the search interface;
> context updates can redirect search transiently, while executor updates can be competitive
> when improvement remains within a fixed solution family.

Cross-task 部分单独根据结果选择：`task-specific`、`family-transferable` 或 `broadly transferable`，不在
实验前预设必须得到正 transfer。
