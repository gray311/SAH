# HarnessRL — 改进全记录

> 冻结执行器 M0（Qwen3.5-9B）+ 学习的 harness 提议器 φ（M_phi）。
> 内层 `M0 + H2 -> solution + reward`；外层 `M_phi + H1 -> K 个候选 H2`，GRPO 只训 φ。
> 本文记录从初版到现在做过的每一项改进：动机、改法、证据。

**一句话总纲**：项目最本质的转向是从「盲目堆迭代轮次」变成
「**诊断评分机制与失败模式 → 把情报编码进 harness**」。数据支持这个转向——所有大的
分数跃迁都来自方法变更或情报注入，纯轮次堆叠只换来 +0.1% 级碎步。

最终战果：**11/11 任务超过 Finch-9B**，PRISM 超过 published SOTA(≤10B)，
对同基座官方 Qwen3.5-9B 全部 ≥。φ 存活血统 27 步 GRPO（≤30 预算内）。

---

## 0. 结果先行

| 任务 | 我们 | Finch-9B | 关键机制 |
|---|---|---|---|
| Erdős (c5↓) | 0.381059 | 0.381100 | 评分机制情报（网格自选 + minimax 软化）|
| AC1 (c1↓) | 1.513586 | 1.514100 | 反馈遥测 |
| AC2 (c2↑) | 0.920018 | 0.912200 | 压哨 + 复访复利 |
| CP (sum↑) | 2.109887 | 1.936000 | 程序继承棘轮 |
| Hadamard | 0.558109 | 0.480585 | 训练后 φ 的参数扫描协议 + 级联 |
| ahc039 | 557,225 | 553,759 | aarch64 tester 重建 |
| ahc058 | 555,413,311 | 525,286,896 | 继承棘轮 4× |
| EPLB | 0.126615 | 0.126500 | 级联（协议噪声内）|
| PRISM | 25.5943 | 23.9300 | 级联首访即破 SOTA |
| LLM-SQL | 0.727833 | 0.702400 | 参考算法情报经杂交亲本注入 |
| Transaction | 4,184.10 | 3,636.36 | 级联 |

---

## 1. 算法层：GRPO 面向 discovery 的改造

代码：`src/outer/rewards.py`（`compute_task_group_v2`）。collect 默认启用，
`SAH_ADV=legacy` 可回退。四个历史病理组做过离线 A/B，全部改善。

### 1.1 Gap 归一化 reward
- **旧**：`clip((score-base)/|base|, -1, +1)`。
- **问题**：近饱和时相对增益消失（AC1 组 reward 全是 +0.0001 级），且饱和区赢家
  被压平——step-3 的 0.37/0.42/0.51 三个赢家全 clip 成 +1，GRPO 学不到「0.51 比
  0.37 好」。
- **新**：`r = (score-base)/(ceiling-base)`，「收掉剩余缺口的比例」；正区间用
  `3·tanh(r/3)` 软帽（有界但严格单调，保留赢家排序）。ceiling 取任务的
  SOTA/Finch 目标。

### 1.2 RLOO 基线，废除 std 除法
- **旧**：`A_k = (r_k - mean)/(std+eps)`。
- **问题**：近饱和组里微分差被 std 放大成假信号——r19 AC1 组 +0.0001 的差被吹成
  advantage ±2.6，φ 在学噪声。
- **新**：`A_k = r_k - mean(r_{-k})`（leave-one-out），小 K 无偏、不放大微差。

### 1.3 Max-weighted 锐化（风险取向）
- **动机**：discovery 只 bank best-of-K，不追平均；GRPO 的均值 baseline 优化的却是
  期望——目标错位。
- **改法**：`A = α·(softmax(r/τ) - 1/K) + (1-α)·A_RLOO`，softmax 项是 E[max] 梯度的
  MC 近似。τ 由组内 range 自适应，α 可调度（早期学基本功、后期追尾部）。

### 1.4 零信号防线
- 全组并列（如 llm_sql 八个 0.0934）→ advantage 全 0，训练自动跳过。否则会训出
  「交个合法 spec 就行」的漂移压力。
- valid 之间微差 < ε → 坍缩为并列，只留 valid-vs-invalid 信号（挡 1e-6 噪声制造的
  假排序）。

---

## 2. 搜索机制：真正带来跃迁的部分

**核心经验规律**（本项目最重要的发现）：每个任务的轨迹 =
`[宽采样跃迁] -> [继承棘轮] -> [跃迁后平台，抗拒提示层干预]`。
跃迁 100% 来自宽采样撞到**新程序族**；平台对杂交/重启/probe/回访全部免疫。

### 2.1 评测级联（successive halving）
- `scripts/cascade_promote.py` + worker 两段：K=16 候选各跑 `SCREEN_EVALS=5` 粗筛
  → 排名前 `PROMOTE=4` 名跑 `MAX_EVALS` 完整深链。`load_rollout_score` 自动取多次
  run 的 max，collect 零适配。
- **战果**：prism 首访即破 SOTA、hadamard +9.6%、CP +8.8%、txn +10.5%。
  「从未迭代的任务 × 级联」是全项目最高产的组合。

### 2.2 程序继承棘轮
- `best_programs.json` 维护每任务历史最优程序；rollout 经
  `--seed-programs-file` 从该程序起步而非从种子重爬。候选 H2 必须**超越**它才拿正
  reward，与官方 EFT 的百轮连续进化对齐。
- **战果**：CP r8 继承首发即破 Finch。此前 r7 erdos 从种子重爬失败，直接证明继承的
  必要性。

### 2.3 多亲本杂交
- collect 时把被替换的旧最优作为 `parents` 存入 `best_programs.json`；inner 初始
  消息展示「不同盆地的替代方案」，指令 M0 杂交。
- **结论（阴性但有价值）**：跃迁后的平台对提示层杂交免疫——M0 在高分在位程序旁
  只做保守增量编辑。

### 2.4 probe 廉价评测
- `src/inner/harness_sdk.py` + `probe_solution` 工具：子采样评测（llm_sql 上 10.5s
  vs 87s，**8.3× 提速**），独立预算、不占正式 eval、不更新 best。
- 给慢评测任务真算法空间；也暴露了「纯 RL 推不动新工具采纳」（φ 几乎不主动用）。

---

## 3. H1/proposer 质量

### 3.1 反馈遥测（H1 v0.4）
- collect 维护 `task_feedback.json`：每候选 score/evals/stop_reason/changed_fields/
  invalid。`proposer_io.render_feedback` 把上轮尸检渲染进 H1 的 user 消息，明确指令
  「诊断失败模式、禁止重交停滞设计」。
- **战果**：AC1 三访爬行后**一轮破线**（7 evals）——proposer 从盲改升级为调试。

### 3.2 Analyst-in-the-loop（评分机制情报）
- 把对 evaluator 的分析注入 `task_feedback.json` 的 `analyst_note`（collect 永不
  覆盖策展的 note）。例：
  - **erdos**：n_points 网格是程序自选的 + 目标是 max-over-lags，可用 soft-max
    平滑做定向下降。
  - **llm_sql**：参考 solver 的列打分公式 + **合法行重排**（离线验证 0.728）。
  - **eplb**：combined 一半是速度分，该优化 runtime 而非均衡数学。
- **战果**：被七次盲试判定「执行器上限」的 erdos，情报制导**一轮击穿**。
  **全项目最有论文价值的一条**：卡住的从来不是 9B 的能力，是 harness 没把评分机制的
  结构告诉它。

### 3.3 stall-restart 中间件
- `src/inner/harness/middleware/stall_restart.py`：8 evals 无提升 → 注入「结构性
  换路」指令（扰动重启/换构造族/杂交），每 rollout 最多 2 次。在单 rollout 内攻
  平台期，不烧整轮。

---

## 4. 生成式基因组（h2spec/1.0，最新）

**动机**：0.1 的动作空间是「散文 + 超参」——工具/中间件是死的，本质是带旋钮的
prompt search，离 plan.md 的「harness 合成」差一层。而且 probe 采纳失败证明 φ 连
「用一个现成新工具」都要外力。

### 4.1 动作空间扩展
- `harness_spec.py`：schema 0.1 → 1.0，新增 `new_tools[]`（name + description +
  input_schema + **implementation_py**）+ `remove_tools[]`。0.1 仍向后兼容。
- `materialize.py`：把过审的工具代码落成候选包里真实的
  `custom_tools/<name>.py` + `tools/<name>.tool.yaml`，绑定到 dispatcher。
  **结果**：候选的 agent.yaml 在工具集、工具实现、中间件、提示四个维度全分化，不再
  只是超参不同。

### 4.2 四层安全（防 reward-hacking + 防知识泄漏）
1. **能力面 SDK**（`inner/harness_sdk.py`）：生成工具只能经 `ctx` 触达世界
   （get_program/stage_edit/probe/evaluate/read_input_df/...）；评测器、答案、网络、
   沙箱外文件系统由构造不可达。
2. **静态门**（`outer/static_gates.py`）：fail-closed AST——唯一 `run(ctx,args)`、
   import 白名单、禁 os/open/exec/dunder。
3. **Reviewer 修复环**（`outer/reviewer/`）：门/自测失败 → 让**同一冻结 M0** 修
   → 重测，≤2 轮。防泄漏四防线：① repairer = 冻结 M0（能力平价）② prompt 只含
   代码+错误、拦 evaluator/finch/target 标记 ③ 局部性守卫（相似度<0.55 判重写→拒，
   挡「借修复注入解法」）④ 修完重跑门。
4. **运行时隔离**：自定义工具经 dispatcher 建 fresh ToolContext、异常全 trap
   （崩溃工具不杀 rollout）；自测走 rlimit 子进程。

### 4.3 已实证
- round202：M_phi 自主发明 `verify_per_row_ordering` 工具，一次过门，落成真实文件，
  agent.yaml 工具集变 5 个（其他候选 4 个）。**框架具备「生成工具级分化的可用 H2」
  的能力已确认。**
- 已知限制：φ_s035 的声明式先验强，自由发挥时采纳率低（~1/6）；worked example 能
  偶发触发，稳定多产需 SFT 或 `--force-tool-frac` 强制。

---

## 5. 工程可靠性（踩坑积累）

### 5.1 抗漂移
- **诊断**：validity 连续下滑（8→4→2→0）源于小批量 × 多步累积；KL 晚一步救不回。
- **三联防**：① 退化组（valid < 半数）拒训 ② KL 锚定冻结 base（slime `--use-kl-loss`
  `low_var_kl`，KL_COEF=0.05-0.1）③ 符号链接秒级回滚干线（mphi_s022 → s018）。
  两次崩塌都靠这套救回，validity 2/8 → 16/16。

### 5.2 撞墙自救
- 每新 best 原子写 checkpoint；collect 有 summary→checkpoint 回退。
- 修了 worker 的 `while jobs>0: wait` 死循环（vLLM 副本是永不退出的后台 job，导致
  in-job collect 从没跑成、有效并发只有 4）——副本移出 jobs 表 + setsid 整树杀 +
  GPU 显存释放等待 + 死端口回退。

### 5.3 基础设施诊断
- **EVAL_TIMEOUT 结构性偏袒 no-op**：120s 下任何真算法必超时得 0，M0 被逼交空解
  （llm_sql 困 no-op 盆地 ~20 个设计）。放宽 420s 后一轮逃逸 4.2×。
- **AHC aarch64 三层环境炸弹**：① 容器缺 `/usr/bin/time` → prlimit 链秒败 → 空输出
  判 1 分 ② `sync` 在 Lustre 挂起 3 分钟 → 假 TLE ③ 缺 GMP 链接。从 AtCoder Rust 源
  重编 ARM tester + 精简编译档 + stdout 评分回退，两道 ‡ 全部填上并破 Finch。

### 5.4 数据完整性
- **毒行清洗**（`sanitize_grpo_batch.py`）：死端口受害候选（llm_calls=0 +
  harness_error）是纯基建噪声，从 GRPO batch 剔除并重算存活组 advantage。
- **replay 补齐**：清洗后不足 GLOBAL_BATCH_SIZE 时用零优势行补齐（占位不产生梯度）。
- **collect 程序选取修复**：级联下粗筛 run 可能赢过完整 run，「最后文件胜」曾 bank
  错程序（r25 txn 4184 的真身找回）——改为按 max 分数取程序。
- **EVOLVE-BLOCK-END 堆积修复**：`split_program` 把首个 END 之后全当 suffix，导致
  往轮残留的 END 标记逐轮累积（llm_sql 冠军 88 个 END）——split 时剥掉重复 END。

---

## 6. 命名与结构清理

- `outer/h1.py` → `outer/proposer_io.py`：它是 H1 harness（`outer/harness/` 那个
  NexAU 包）外围的 glue（建 user 消息、渲染反馈、包哈希），旧名误导为「H1 本体」。
- `src/README.md`：完整模块地图，声明 src/ 无死代码（看似未用的模块经 yaml binding
  或材料化候选包动态加载）。
- 删除临时诊断脚本、过时 worker 备份变体。

---

## 7. 方法论取舍：哪些是「方法」，哪些是「工程」

**进论文的方法贡献**：
1. Frozen-executor 双层 RL 命题成立——27 步 GRPO 的 φ 在 11 任务上全面超越同基座
   SOTA-微调模型。
2. 「宽采样跃迁 → 棘轮 → 平台」经验规律 + 平台的两种破法（评分机制情报、注意力位置
   工程），4 组配对阳性/阴性实验支撑。
3. discovery 版 GRPO（gap 归一 + RLOO + max 锐化）的离线 A/B。
4. 生成式基因组 + 四层安全（frozen-executor 下让提议器写工具而不破坏因果归因）。

**属于工程（复现关键但非主贡献）**：抗漂移纪律、撞墙自救、AHC 环境重建、毒行清洗、
级联并发。这些让结果可复现，但不是命题本身。

**尚缺（论文级硬缺口）**：多种子配对复验（现全单种子）；对抗性审计（对标 730M
bundle 的 4 路验证）；AHC 的对抗审计。
