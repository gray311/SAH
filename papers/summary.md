下面这版可以直接作为 project proposal、论文 introduction 和 experiment section 的骨架。

# Project Summary

暂定标题：

**Learning to Propose Agent Harnesses for Efficient Hard-Problem Discovery**

一句话定义：

> 我们冻结负责解题的 executor，用最终 solution reward 训练一个独立的 harness proposer，使其逐渐学会生成更有效、可执行、可检查的 prompt、tool、skill、parameter 和 workflow 组合。

核心不是让模型“学会直接解题”，而是让模型学会：

> **如何为一个固定的 executor 构造更好的求解环境。**

---

## 1. Motivation

### 1.1 Hard-problem discovery 的核心是如何利用历史 reward

对于 Erdős、AlphaEvolve-style mathematical discovery、algorithm engineering 和 system optimization，模型需要经过多轮尝试，利用前面 solution 的 reward 改进后续搜索。

现有方法本质上都在解决同一个问题：

> 如何把 previous outcomes/rewards 传递给未来的 executor？

三类方法的 reward transport mechanism 不同：

| 方法类型 | Previous reward 更新什么 | 如何影响未来 solution |
|---|---|---|
| TTT-Discover、ThetaEvolve | Executor / solution generator 的 weights | Reward → executor weights → new solution |
| OpenEvolve、Meta-Harness、AHE、Self-Harness | 外部 program、history、context 或 harness | Reward → artifact/context → frozen model |
| 我们 | 独立 harness proposer 的 weights | Reward → proposer weights → explicit harness → frozen executor |

形式化地：

\[
\text{Executor TTT:}\quad
(\tau,r)\rightarrow \Delta\theta
\rightarrow M_{\theta'}\rightarrow y
\]

\[
\text{Context/Harness Evolution:}\quad
(\tau,r)\rightarrow H'
\rightarrow M_0(\cdot\mid H')\rightarrow y
\]

\[
\textbf{Ours:}\quad
(\tau,r)\rightarrow \Delta\phi
\rightarrow H\sim\pi_{\phi'}
\rightarrow M_0(\cdot\mid H)\rightarrow y
\]

我们的关键设计是将 adaptation 和 execution 分开：

- \(M_0\)：固定 executor，负责生成 solution。
- \(\pi_\phi\)：可训练 proposer，负责生成 executor harness。
- \(H\)：显式、可执行、可检查的中间控制层。

---

### 1.2 为什么不直接 update executor？

TTT-Discover 和 ThetaEvolve 直接把 reward 训练进 solution-generating model。它们的优点是直接，但存在两个问题。

第一是 optimization cost 很高。

TTT-Discover 的报告配置为：

- 每步 512 solutions；
- 50 training steps；
- 共 25,600 solutions/problem；
- 报告成本约 \$500/problem。

ThetaEvolve 的典型 Qwen3-8B 配置为：

- 每步 \(32\times16=512\) programs；
- 65 steps；
- 共 33,280 programs/seed。

我们的当前配置为：

- 每步生成 \(K=8\) 个 candidate harnesses；
- 每个 harness 只让 frozen executor 生成一个 solution；
- 每步仅 8 个 reward-bearing executor rollouts。

因此，我们目前可以准确地说：

> 相比每步 512 solutions 的 TTT/Theta 配置，我们每个 optimization step 使用的 executor rollouts 少 64 倍。

但不能提前说 total compute 少 64 倍，因为总成本还取决于训练步数、proposer forward/backward、harness runtime 和 token 长度。最终应比较 score–compute curve，而不只是 per-step batch size。

第二是 attribution 不够显式。

Executor weight update 可能提高结果，但很难直接回答：

- 是增加了什么工具？
- 学会了什么 search procedure？
- 哪个 prompt instruction 有效？
- 哪个 solver parameter 发生了作用？
- 哪一步 workflow 导致提升？

这并不意味着 TTT 完全“不可解释”，更准确的表述是：

> Direct executor adaptation 缺少一个显式的 artifact-level attribution interface。

我们通过 harness bottleneck，让所有对 executor 的适应最终表现为可检查的 artifact。

---

### 1.3 为什么不只用 context management 或 self-edit harness？

OpenEvolve 更准确的机制不是简单地“让一个模型总结所有 history”，而是维护 program population/archive，再把选出的 parent programs、metrics 和 feedback 放回上下文中。Meta-Harness、AHE、Self-Harness 等方法则让固定的 proposer/editor 持续修改外部 harness。

这种 external adaptation 有明显优点：无需训练，而且 artifact 可见。但随着迭代深入，需要不断解决：

- 哪些历史 solution 应该保留？
- 哪些 examples 应该放进有限 context？
- 如何压缩失败轨迹？
- 如何在 exploitation 和 diversity 之间选择？
- Context 越来越长时，哪些信息真正影响了 proposal？

也就是说，history selection 本身成为了新的 hard problem。

我们的做法是把 task-specific reward history **internalize 到 proposer policy 中**：

\[
\phi_{t+1}
=
\operatorname{GRPOUpdate}
\left(
\phi_t,\{H_{t,k},r_{t,k}\}_{k=1}^{K}
\right)
\]

这样 proposer 不只是看到历史 candidate，而是改变未来生成 harness 的概率分布。它形成一个 amortized search policy，在固定大小的输入下逐渐偏向高回报的 harness construction strategy。

最简洁的区别是：

> Existing harness-evolution methods update the harness with a fixed proposer; we update the policy that proposes harnesses.

需要明确限制：目前每个 task 对应一个 task-specific LoRA。我们尚不能声称单个 task 上训练出的 proposer 能泛化到其他 task。Cross-task transfer 是后续实验问题，而不是当前结论。

---

## 2. Method

### 2.1 Components

对于 task \(\tau_j\)，系统包含：

- \(M_0\)：frozen executor；
- \(M_\phi\)：proposer base model；
- \(\phi_j\)：该 task 对应的 trainable LoRA；
- \(H_1\)：指导 proposer 如何设计 agent harness 的 meta-harness；
- \(H_2\)：proposer 生成、供 executor 使用的 candidate harness；
- \(R_j\)：task-specific evaluator。

每个 \(H_2\) 最好输出为 typed manifest：

\[
H_2 =
(
H_{\text{prompt}},
H_{\text{tools}},
H_{\text{skills}},
H_{\text{params}},
H_{\text{memory}},
H_{\text{workflow}}
)
\]

并记录：

- add / modify / remove；
- component configuration；
- executable files；
- rationale；
- 相对前一版本的 structured diff。

---

### 2.2 Training loop

在第 \(t\) 步：

1. Proposer 生成 \(K=8\) 个 candidate harnesses：

\[
H_{t,k}\sim\pi_{\phi_t}(\cdot\mid \tau,H_1),
\quad k=1,\ldots,8
\]

2. 同一个 frozen executor 使用每个 harness 生成一个 solution：

\[
y_{t,k}\sim M_0(\cdot\mid\tau,H_{t,k})
\]

3. Evaluator 返回 downstream reward：

\[
r_{t,k}=R_\tau(y_{t,k})
\]

4. 八个 reward 构成一个 GRPO group，计算 relative advantage：

\[
A_{t,k}
=
\frac{r_{t,k}-\operatorname{mean}(r_t)}
{\operatorname{std}(r_t)+\epsilon}
\]

5. 仅更新 proposer LoRA \(\phi\)，保持 \(M_0\) 完全冻结。

整体目标为：

\[
\max_\phi
\mathbb{E}_{H\sim\pi_\phi,\,
y\sim M_0(\cdot\mid H)}
[R_\tau(y)]
-
\beta
D_{\mathrm{KL}}(\pi_\phi\Vert\pi_{\phi_0})
\]

从 solution 的角度看，我们优化的是一个由 harness 混合得到的 effective policy：

\[
p_\phi(y\mid\tau)
=
\sum_H
\pi_\phi(H\mid\tau)
M_0(y\mid\tau,H)
\]

---

### 2.3 当前最大的技术风险

每个 harness 只生成一个 solution，因此：

\[
r(H)\approx R(y),\qquad y\sim M_0(\cdot\mid H)
\]

这是 harness quality 的高方差估计。GRPO 可能把“偶然采样到的好 solution”误认为“好 harness”。

必须加入以下实验：

- \(8\) harnesses × \(1\) solution；
- \(4\) harnesses × \(2\) solutions；
- \(2\) harnesses × \(4\) solutions；
- low-temperature 或 deterministic executor；
- 每隔若干步，对 top harnesses 用 4–8 个 solutions 重新评估。

最终 best score 应来自 re-evaluated harness，而不是训练过程中一次幸运 rollout。

---

# 3. Main Result

主结果应回答：

> 在相同 frozen executor、相同 evaluator 和相同 executor-rollout budget 下，学习 harness proposer 是否比直接 solution search、context-only evolution、harness editing 和 executor TTT 更有效？

所有方法应使用同一个 ≤10B base executor、相同工具权限、token limit 和 task evaluator。

## 3.1 Main table 结构

下面是最终 camera-ready 主表应该采用的结构。现在不能提前填入 “ours 最好”的数字；实验需要真正证明这一点。

| Method | Updated object | Budget | Erdős↓ | AC1↓ | AC2↑ | CP26↑ | Had.↑ | ahc039↑ | ahc058↑ | EPLB↑ | PRISM↑ | SQL↑ | Txn↑ | Avg. gap closed↑ | Avg. rank↓ | Wins |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Frozen \(M_0+H_1\) | None | \(B\) |  |  |  |  |  |  |  |  |  |  |  | 0 |  |  |
| Best-of-\(B\) | None | \(B\) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| OpenEvolve | Program/archive | \(B\) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Context-only harness edit | Harness/context | \(B\) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| HASE-style | Shared solver/editor | \(B\) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| TTT-Discover | Executor weights | \(B\) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ThetaEvolve | Generator + population | \(B\) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **Ours** | **Harness proposer weights** | **\(B=8T\)** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

≤10B best-known reference values可以放在单独一行，但不应与 matched-budget results 混为一谈：

| Reference | Erdős↓ | AC1↓ | AC2↑ | CP26↑ | Had.↑ | ahc039↑ | ahc058↑ | EPLB↑ | PRISM↑ | SQL↑ | Txn↑ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Current ≤10B reference | .380932 | 1.503133 | .9472 | 2.635983 | .5764* | 557,168 | 525,286,896 | .1270 | 24.70 | .7341 | 4761.90 |

其中 Hadamard 的 .5764 使用了额外 proprietary-model-derived meta-information，应加脚注，避免被当作完全同条件结果。

---

## 3.2 “比这些方法好”应该如何定义

最可信的主张不是简单说 11 个 task 全部最高，而是证明 compute–performance Pareto advantage：

1. 在相同 executor-rollout budget \(B\) 下，ours 有最高的平均 normalized improvement。
2. 达到相同 target score 时，ours 所需 executor rollouts 更少。
3. Ours 的 score-vs-rollout AUC 更高。
4. Harness gains 能通过重复评估保持，而不是 winner’s curse。
5. 输出的改进可以被定位到具体 harness components。

由于不同 task 的 metric scale 差异很大，而且 ahc058 的 initial score 接近零，不适合直接平均 relative percentage。建议使用 normalized gap closed：

最大化任务：

\[
G_j=
\frac{R-R_{\text{initial}}}
{R_{\text{reference}}-R_{\text{initial}}}
\]

最小化任务：

\[
G_j=
\frac{R_{\text{initial}}-R}
{R_{\text{initial}}-R_{\text{reference}}}
\]

主表同时报告：

- 11 个 raw scores；
- average gap closed；
- average rank；
- wins/ties；
- executor rollouts；
- generated tokens；
- wall-clock/GPU hours。

论文主 claim 可以写成：

> Proposer adaptation achieves a better score–compute trade-off than direct executor adaptation and context-only harness evolution, while exposing the behavioral changes applied to a frozen executor through explicit, executable harness artifacts.

---

# 4. Experiment 1：Cross-Task Proposer Transfer

我们有 11 个 task，每个 task 训练一个 LoRA：

\[
\phi_1,\phi_2,\ldots,\phi_{11}
\]

构造 \(11\times11\) transfer matrix。第 \(i\) 行表示在 source task \(i\) 上训练的 proposer，第 \(j\) 列表示让它为 target task \(j\) 生成 harness。

关键是：

- 不在 target task 上继续更新；
- frozen executor 相同；
- 每个 cell 生成 Best@8；
- 每个 cell 重复 5–10 次；
- 加入 initial proposer \(\phi_0\) 作为额外 baseline row。

定义：

\[
S_{ij}
=
\mathbb{E}
[
\operatorname{Best@8}
(\phi_i,\tau_j)
]
\]

用户希望报告 updated proposer / initial proposer，也可以作为附加数据；但由于存在最小化 metric 和 near-zero baseline，主 heatmap 应使用方向修正后的 normalized improvement：

\[
T_{ij}
=
\frac{
U(S_{ij})-U(S_{0j})
}{
\operatorname{Scale}_j+\epsilon
}
\]

其中 \(U\) 将所有 metric 转成 higher-is-better，\(\operatorname{Scale}_j\) 可以使用 initial-to-reference gap 或经验分位数范围。

这张图可以回答：

- 对角线：in-task proposer learning；
- 非对角线：zero-shot cross-task transfer；
- row mean：哪个 task 学到的 proposer strategy 最通用；
- column mean：哪个 target task 最容易被其他 proposer 帮助；
- asymmetry：\(i\rightarrow j\) 是否不同于 \(j\rightarrow i\)；
- domain blocks：数学、算法、系统任务是否形成 transfer clusters；
- negative transfer：哪些 learned biases 会伤害其他任务。

5 次重复的基本成本为：

\[
11\times11\times5\times8
=
4,840
\]

次 executor rollouts。

这是 exploratory experiment。即使 off-diagonal transfer 很弱，也不会推翻主结果；它只说明目前的 proposer adaptation 是 task-specific 的。

---

# 5. Experiment 2：Cross-Model Harness Transfer

这个实验测试：

> 在小模型上训练的 proposer 所发现的 harness，是否能帮助不同甚至更大的 frozen executor？

例如：

- 原始 ≤10B executor；
- Qwen3.5-32B；
- GPT-OSS-120B；
- 其他兼容 tool interface 的模型。

严格的 artifact-transfer protocol：

1. 只使用原始 \(M_0\) 的 reward 训练 proposer。
2. 在 \(M_0\) 上选择并冻结 harness bank。
3. 不允许大模型重新编辑或根据自身 score 选择 harness。
4. 将完全相同的 semantic harness 应用于其他 executor。
5. 只允许 model-specific syntax adapter，例如 chat template 和 tool-call schema。

每个 executor 至少比较：

| Condition | Harness source | Purpose |
|---|---|---|
| \(E+H_1\) | Default | 每个模型自己的基础能力 |
| \(E+H_{\phi_0}\) | Initial proposer | 控制“生成了额外 harness”本身的收益 |
| \(E+H_{\phi_j}\) | Updated proposer | 核心 transfer result |
| \(M_0+H_{\phi_j}\) | Original executor | Harness 的 source-domain 效果 |

需要报告：

- absolute score；
- 相对该 executor 自己 \(H_1\) 的 gain；
- token/cost overhead；
- tool-call success rate；
- harness instruction adherence；
- component activation rate。

该实验能区分两种可能：

- Harness 学到的是可迁移的 algorithmic/search strategy；
- Harness 只是利用了原 executor 的 model-specific behavior。

也可以增加一个不同问题：

> 固定 proposer weights，但让 proposer 读取 target executor 的 model card 后生成适配 harness。

这属于 model-conditioned proposal，应和严格 artifact transfer 分开报告。

---

# 6. Experiment 3：What Does the Proposer Learn?

这里的表述必须准确：

> 不是 frozen executor 学到了新技能，而是 proposer 越来越倾向于提出能够激活 executor 有效行为的 tools、skills、parameters 和 workflows。

每个 harness 都需要 structured manifest 和 diff，从而生成四类 evolution curves。

### 6.1 Performance curve

横轴统一使用 cumulative executor rollouts，画出：

- group mean reward；
- group max reward；
- validated best reward；
- periodically re-evaluated checkpoint reward；
- OpenEvolve、TTT、Best-of-\(B\) 等基线曲线。

主图不要只用 training step，因为一次 TTT step 是 512 rollouts，而 ours 是 8。

### 6.2 Component discovery curve

对每个 component \(c\) 统计：

\[
P_t(c)
=
\Pr(c\text{ is proposed at step }t)
\]

观察 proposer 是否从 generic prompt edits 逐渐转向：

- task-specific tools；
- verification procedures；
- decomposition skills；
- search parameters；
- iterative refinement；
- memory/archive policy；
- domain-specific workflow。

### 6.3 Activation funnel

“被提出”不等于“真正有用”，因此需要记录：

\[
\text{proposed}
\rightarrow
\text{loaded}
\rightarrow
\text{invoked}
\rightarrow
\text{successful use}
\rightarrow
\text{reward improvement}
\]

例如一个 tool 被写进 harness 但 executor 从未调用，不能算 learned useful tool。

### 6.4 Causal component attribution

对 high-performing harness \(H_t\)，逐个移除或恢复 component：

\[
\Delta_c(t)
=
R(H_t)-R(H_t\setminus c)
\]

只有同时满足以下条件，才能称为 “validated new skill/component”：

1. 初始 \(H_1\) 中不存在；
2. proposer 后续主动提出；
3. executor 实际加载并使用；
4. 完整 harness 显著优于 component-reverted harness；
5. 结果在多个 executor samples/seeds 上保持。

最终可以画一条 cumulative validated components staircase，并在 reward jumps 上标出：

- 新 tool 出现；
- verifier 加入；
- search depth 改变；
- parameter 调整；
- workflow 从 single-shot 变为 propose–test–refine。

这会成为论文中最强的 qualitative evidence：不仅展示 reward 上升，也展示 proposer 具体发现了什么。

---

# 7. 最终论文结构

建议形成四个 Research Questions：

- **RQ1 — In-task efficiency:** 学习 proposer 是否比 executor TTT 和 context-only evolution 更 compute-efficient？
- **RQ2 — Cross-task transfer:** Task-specific proposer LoRA 是否包含可迁移的 harness construction strategy？
- **RQ3 — Cross-model transfer:** 学到的 harness 是否能帮助不同规模、不同架构的 frozen executor？
- **RQ4 — Mechanism:** 哪些 tools、skills、parameters 和 workflows 导致了提升？

最核心、最稳健的论文结论应是：

> Hard-problem discovery does not require adapting the solver itself. By training a separate policy to propose explicit agent harnesses, downstream rewards can be internalized into an efficient search policy while keeping the executor frozen and preserving an inspectable interface for behavioral adaptation.

目前不要提前 claim：

- single-task LoRA 已经能够 cross-task generalize；
- 总成本一定比 TTT 少 64 倍；
- proposer weights 本身完全可解释；
- executor 学会了新技能；
- 单次 rollout 的最高 reward 就代表 harness 真正更好。

真正需要主表证明的是：**在 matched compute 下，ours 的 validated score–compute frontier 优于这些方法。**