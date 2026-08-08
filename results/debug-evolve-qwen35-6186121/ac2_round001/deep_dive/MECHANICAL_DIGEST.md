# AC2 round001 mechanical trajectory digest

This file is generated from the immutable inspection bundle. It records
tool chronology and source fields; interpretation belongs in `REPORT.md`.

## cand00

- changed fields: `['system_prompt']`
- score: seed `0.9548269841969006` -> best `0.992403556450761`
- old training reward/advantage: `-0.007386896643712506` / `0.05746333384839138`
- proposer calls: harness_shell -> harness_shell -> harness_shell -> edit_harness_file -> edit_harness_file -> validate_harness -> submit_harness
- executor calls: LoadSkill({'skill_name': 'discovery-optimization'}) -> edit_solution[hyperparameters,shape_change] -> evaluate_solution(score=0.992404, valid=1, left=1) -> edit_solution[hyperparameters,step_or_plateau,exponential_tail,shape_change] -> evaluate_solution(score=0.974413, valid=1, left=0) -> finish({'summary': 'Increased discretization from 50 to 200 intervals and extended optimization from 15000 to 25000 steps with refined learning rate schedule. Best combined_score: 0.992404 (C₂=0.889471), improving from baseline 0.954827.'})

Prompt delta:

```markdown
## Task-Specific Search Guidance: C₂ Maximization

**Objective**: Maximize the combined_score (currently best: 0.999789). The score represents how well the discovered function achieves the second autocorrelation inequality constant C₂.

**Key Search Directions to Explore**:
1. **Symmetry exploitation**: Consider whether restricting to even functions (f(-x) = f(x)) helps reduce the search space while maintaining optimality.
2. **Multi-resolution approach**: Try starting with coarse discretization and refining around high-value regions of the convolution.
3. **Step-function-inspired initialization**: The historical best used step functions; consider initializing near such profiles.
4. **Adaptive learning schedules**: Experiment with learning rate schedules that start aggressive and decay carefully.
5. **Numerical precision**: Higher discretization resolution may be needed to capture subtle features.

**Evaluation Strategy**:
- Use `probe_solution` for quick ranking of variants
- Use `evaluate_solution` for definitive scoring (budget: 36 evaluations)
- `finish` when you cannot improve or budget is exhausted

**Remember**: The best version is retained automatically after each evaluation. Focus on structural changes that meaningfully improve the objective.
```

## cand01

- changed fields: `['system_prompt']`
- score: seed `0.9548269841969006` -> best `0.9805204322650442`
- old training reward/advantage: `-0.019272529949836303` / `-0.008883756437446912`
- proposer calls: harness_shell -> harness_shell -> harness_shell -> edit_harness_file -> validate_harness -> submit_harness
- executor calls: LoadSkill({'skill_name': 'discovery-optimization'}) -> edit_solution[hyperparameters,step_or_plateau,exponential_tail,shape_change] -> evaluate_solution(score=0.978245, valid=1, left=1) -> edit_solution[hyperparameters,step_or_plateau,exponential_tail,gaussian,shape_change] -> evaluate_solution(score=0.98052, valid=1, left=0) -> finish({'summary': 'Achieved combined_score 0.98052 (C₂ = 0.878821) using step-function-like initialization with a sharp transition at 70% of the interval and Gaussian decay tail, beating the baseline 0.954827.'})

Prompt delta:

```markdown
## Task-Specific Strategy: C₂ Optimization

**Objective**: Maximize C₂ = ||f ★ f||₂² / ((∫f)² ||f ★ f||_{∞}) by evolving a non-negative function f: ℝ → ℝ.

**Key Insights from Task Context**:
1. Step functions achieved 0.8962799441554086 (current record)
2. The current H2 achieves 0.999789 - very close to optimal!
3. Further gains require exploiting piecewise-constant structure

**Recommended Approach**:
1. **Initialize with step-function-like structure**: Start with a piecewise-constant function (few distinct levels) rather than random values
2. **Multi-scale refinement**: Begin with coarse discretization (e.g., N=20-30), optimize, then refine to N=50-100
3. **Bias toward sparsity**: Use L1 regularization or prefer solutions with fewer distinct values
4. **Adaptive learning rate**: Use a more aggressive initial LR (0.1-0.5) with faster decay
5. **Symmetry exploitation**: Try even functions (f(-x) = f(x)) to reduce search space

**Specific Edits to Consider**:
- Change initialization from `jax.random.uniform` to a piecewise-constant pattern
- Add L1 penalty to encourage sparse solutions
- Try different optimizer: AdamW with weight decay, or RMSprop
- Increase warmup steps or use linear warmup instead of cosine
- Add early stopping when improvement stalls

**Evaluation Strategy**:
- Probe with N=20 first to find promising structure
- Refine with N=50, then N=100 if time permits
- Monitor C₂ convergence - stop when < 1e-6 improvement over 500 steps
```

## cand02

- changed fields: `['system_prompt']`
- score: seed `0.9548269841969006` -> best `0.970224531137343`
- old training reward/advantage: `-0.029570605055964726` / `-0.033556731517047245`
- proposer calls: harness_shell -> harness_shell -> harness_shell -> edit_harness_file -> validate_harness -> submit_harness
- executor calls: LoadSkill({'skill_name': 'discovery-optimization'}) -> edit_solution[hyperparameters,step_or_plateau,exponential_tail,symmetry,positivity_change,objective_or_convolution,shape_change] -> evaluate_solution(score=0.970225, valid=1, left=1) -> edit_solution[hyperparameters,step_or_plateau,exponential_tail,symmetry,positivity_change,objective_or_convolution,shape_change] -> evaluate_solution(score=0.95626, valid=1, left=0) -> finish({'summary': 'Improved C₂ from 0.855 to 0.869593 (combined_score 0.970225) by initializing with multi-plateau even-symmetric step function structure. Best score achieved: 0.970225.'})

Prompt delta:

```markdown
# Task-Specific Guidance: Second Autocorrelation Inequality (C₂)

## Objective
Maximize C₂ = ||f ★ f||₂² / (||f ★ f||₁ ||f ★ f||_{∞}) where f: ℝ → ℝ is non-negative.
Current best: 0.999789 (very close to theoretical max 1.0).

## Critical Strategies for Breaking Through

### 1. Exploit Even Symmetry
The optimal function is likely even (f(x) = f(-x)). This reduces complexity by ~50% and may help the optimizer converge to better solutions. Define f on [0, ∞) and mirror it.

### 2. Adaptive Discretization
Uniform 50 intervals may miss important features. Use:
- More intervals (200-500) for final optimization
- Cluster intervals where |f'(x)| is large
- Use logarithmic spacing for functions with decay tails

### 3. Function Family Hierarchy
Try these in order, increasing complexity:
- **Step functions**: Current best baseline (multiple plateaus)
- **Piecewise linear**: Smoother transitions between plateaus
- **B-splines**: Smooth basis functions with optimized coefficients and knots
- **Mixture models**: α·exp(-|x|/σ) + β·exp(-|x|/σ') + γ·step(x)
- **Rational functions**: P(x)/Q(x) with positivity constraints

### 4. Optimization Strategy
- Use **AdamW** with weight decay for better generalization
- Implement **learning rate scheduling**: high LR for exploration, low LR for fine-tuning
- Consider **CMA-ES** or **Cobyla** for derivative-free optimization
- Use **multi-start**: random restarts from different initializations

### 5. Key Insight from AlphaEvolve Success
Step functions work because they concentrate mass in specific regions. Consider:
- Functions with compact support (zero outside [-L, L])
- Functions with multiple peaks at strategic locations
- Piecewise constant with smooth (C¹ or C²) transitions

### 6. Computational Tips
- Use FFT-based convolution (O(n log n)) for large n
- Pre-compute norms to avoid redundant calculations
- Monitor gradient norms to detect convergence
- Use subsampling for early iterations, full precision near convergence

## Evaluation Budget
- You have 2 evaluations total
- Use probe_solution for quick ranking, evaluate_solution for final confirmation
- Aim for >1.0 combined_score to establish a new world record
```

## cand03

- changed fields: `['system_prompt', 'new_skills.c2-optimization']`
- score: seed `0.9548269841969006` -> best `0.9957583321880714`
- old training reward/advantage: `-0.00403141254586218` / `0.09225050604484299`
- proposer calls: harness_shell -> harness_shell -> harness_shell -> write_harness_file -> edit_harness_file -> edit_harness_file -> validate_harness -> submit_harness
- executor calls: LoadSkill({'skill_name': 'discovery-optimization'}) -> edit_solution[hyperparameters,shape_change] -> evaluate_solution(score=0.967526, valid=1, left=1) -> edit_solution[hyperparameters,shape_change] -> evaluate_solution(score=0.995758, valid=1, left=0) -> edit_solution[hyperparameters,shape_change] -> finish({'summary': 'Improved C2 from 0.867 to 0.892478 (combined_score 0.995758) by increasing discretization to 200 intervals, learning rate to 0.1, and steps to 30000 - very close to the 0.89628 target but evaluation budget exhausted.'})

Prompt delta:

```markdown
# C₂ Optimization Task Guidance

## Current Best Score: 0.999789 (C₂ ≈ 0.8961)
## Target: Exceed 0.8962799441554086 (combined_score > 1.0)

## Task-Specific Skill: `c2-optimization`
Load this skill for targeted guidance on maximizing the second autocorrelation inequality constant.

## Key Strategy: Step-Function Optimization
The current record holder (0.8962799441554086) uses step functions. Your optimization should:
1. **Increase discretization**: Use 100-200 intervals instead of 50 for sharper steps
2. **Aggressive learning rate**: Try LR=0.05-0.1 with warmup for faster convergence
3. **More iterations**: Consider 20000-30000 steps for thorough exploration
4. **Non-negative enforcement**: Use `jax.nn.relu` or `jax.nn.softplus` consistently

## Concrete First Edit
Modify the seed program to:
- Set `num_intervals = 100` (or higher)
- Increase `learning_rate = 0.05`
- Optionally increase `num_steps = 20000`

## Evaluation Budget: 2 evaluations
Make your first edit count: implement the step-function enhancement strategy immediately.

## Success Criteria
- combined_score > 1.0 means C₂ > 0.8962799441554086 (new world record!)
- Validity must be 1.0 (no errors, non-negative function, positive integral)
```

## cand04

- changed fields: `['system_prompt']`
- score: seed `0.9548269841969006` -> best `0.9607464215643968`
- old training reward/advantage: `-0.039050715930738375` / `-0.04686146941614589`
- proposer calls: harness_shell -> harness_shell -> harness_shell -> edit_harness_file -> validate_harness -> submit_harness
- executor calls: LoadSkill({'skill_name': 'discovery-optimization'}) -> edit_solution[hyperparameters,step_or_plateau,exponential_tail,gaussian,triangular_or_ramp,symmetry,positivity_change,objective_or_convolution,shape_change] -> evaluate_solution(score=0, valid=0, left=1) -> edit_solution[hyperparameters,step_or_plateau,symmetry,positivity_change,objective_or_convolution,shape_change] -> evaluate_solution(score=0.960746, valid=1, left=0) -> finish({'summary': 'Improved combined_score from 0.954827 to 0.960746 by using better initialization (step-function-inspired), more intervals (200), proper convolution normalization, and fixing JIT boolean conversion error. Still below target of 1.0 but progress made.'})

Prompt delta:

```markdown
# TASK-SPECIFIC GUIDANCE: Second Autocorrelation Inequality Constant C₂

## Problem Summary
Maximize C₂ = ||f ★ f||₂² / ((∫f)² ||f ★ f||_{∞}) for a non-negative function f: ℝ → ℝ.
Current best lower bound: **0.8962799441554086** (AlphaEvolve, step functions).
Target: Surpass this to establish a new world record.

## Key Insights & Strategies

### 1. Beat the Step Function Record
- Step functions achieved 0.8962799441554086 - this is your baseline
- Try **piecewise-linear functions** with optimized breakpoints
- Consider **smoothed step functions** (sigmoid-based transitions)
- Explore **multi-scale piecewise functions** with different slopes in different regions

### 2. Function Families to Explore
- **Piecewise linear**: Define f on intervals with linear segments; optimize breakpoints and slopes
- **B-splines**: Optimize spline coefficients with positivity constraints
- **Mixture models**: Weighted sums of basis functions (Gaussians, exponentials, polynomials)
- **Fourier-based**: Optimize Fourier coefficients, ensure inverse transform is non-negative

### 3. Optimization Approach
- Use **gradient-based methods** but with careful learning rate scheduling
- Try **multi-start optimization**: Different initializations can find better basins
- Consider **coarse-to-fine**: Optimize on coarse grid, then refine
- Use **adaptive discretization**: More points where the function varies rapidly

### 4. Implementation Tips
- Ensure f(x) ≥ 0 everywhere (use softplus, exponential, or squared transformations)
- Use FFT for convolution: O(n log n) vs O(n²)
- Start with num_intervals=50-100, increase if needed
- Monitor convergence: if C₂ stalls, try a different function family

### 5. Success Criteria
- **combined_score > 1.0** means you've beaten the current best (0.8962799441554086)
- Prioritize beating 0.8962799441554086 over any other metric
- If your current approach stalls, try a fundamentally different function representation

## Evaluation Budget
You have limited evaluations. Each edit should be a **substantive change**:
- Don't just tune hyperparameters; change the function family or structure
- Use probe_solution to quickly rank variants before full evaluation
- When evaluations are low, focus on the most promising direction
```

## cand05

- changed fields: `['system_prompt']`
- score: seed `0.9548269841969006` -> best `0.9857115313515428`
- old training reward/advantage: `-0.014080334763318101` / `0.01238888562444855`
- proposer calls: harness_shell -> harness_shell -> edit_harness_file -> edit_harness_file -> edit_harness_file -> validate_harness -> submit_harness
- executor calls: LoadSkill({'skill_name': 'discovery-optimization'}) -> edit_solution[hyperparameters,shape_change] -> evaluate_solution(score=0.985712, valid=1, left=1) -> edit_solution[hyperparameters,step_or_plateau,exponential_tail,triangular_or_ramp,positivity_change,shape_change] -> evaluate_solution(score=0.977895, valid=1, left=0) -> finish({'summary': "Improved C₂ from ~0.856 to 0.8835 (combined_score 0.985712) by increasing discretization resolution (50→200 intervals) and using smaller learning rate (0.01→0.001). Step function initialization was tried but didn't improve further. Best result achieved with higher resolution and stable optimization."})

Prompt delta:

```markdown
## Task: Maximize C₂ (Second Autocorrelation Inequality Constant)

**Target**: Surpass 0.8962799441554086 (current record)

**Key Insight**: Historical record achieved by step functions. Prioritize piecewise-constant or piecewise-linear representations with sufficient resolution.

**Search Strategy**:
1. Increase discretization resolution to capture finer function shapes
2. Use smaller learning rates for stable fine-tuning
3. Employ multiple random restarts with different initializations
4. If optimization stalls, consider structural changes to function representation

**Monitor**: C₂ values approaching 0.8963 indicate proximity to new record.
```

## cand06

- changed fields: `['system_prompt']`
- score: seed `0.9548269841969006` -> best `0.9548269841969006`
- old training reward/advantage: `-0.0449714031868047` / `-0.053245732859932865`
- proposer calls: harness_shell -> harness_shell -> edit_harness_file -> validate_harness -> submit_harness
- executor calls: LoadSkill({'skill_name': 'discovery-optimization'}) -> edit_solution[hyperparameters,shape_change] -> evaluate_solution(score=0.952974, valid=1, left=1) -> edit_solution[hyperparameters,exponential_tail,symmetry,multi_start,positivity_change,objective_or_convolution,shape_change] -> evaluate_solution(score=0, valid=0, left=0) -> finish({'summary': 'Could not beat baseline 0.954827; multi-seed with symmetry enforcement caused negativity issues. Best score remains 0.954827 (C2 ≈ 0.8557).'})

Prompt delta:

```markdown
## Task-Specific Search Strategy: Second Autocorrelation Inequality

### Current State
The seed program uses gradient descent on a piecewise-linear function with 50 intervals. Best achieved: ~0.8959 (combined_score 0.999789). Target: exceed 0.8962799441554086.

### Key Insights for Improvement
1. **Step functions dominate**: AlphaEvolve's best (0.8962799441554086) uses step functions. The seed's gradient approach may not reach sharp step-like features.

2. **Multi-resolution search**: Start with coarse discretization (10-20 intervals), identify promising regions, then refine locally with higher resolution.

3. **Symmetry exploitation**: The objective is invariant under f(x) → f(-x). Enforce even symmetry (f[i] = f[-i]) to reduce search space and stabilize optimization.

4. **Strategic breakpoint placement**: Instead of uniform intervals, concentrate breakpoints around the origin where convolution peaks.

### Concrete Search Plan

**Iteration 1: Symmetry-enforced optimization**
- Modify to enforce even symmetry: `f_values = jnp.concatenate([f_values[:N//2], f_values[:N//2][::-1]])`
- This halves the search space and may find cleaner step-like solutions

**Iteration 2: Adaptive discretization**
- Start with 20 intervals, identify peak region of convolution
- Refine that region with 50+ local intervals
- Use `jax.random.uniform` seeded differently for diversity

**Iteration 3: Step-function initialization**
- Initialize with a multi-step pattern (e.g., 3-5 steps with varying heights)
- Use gradient descent to fine-tune step positions and heights
- This directly targets the known optimal structure

**Iteration 4: Multi-start ensemble**
- Run 3-5 independent optimizations with different seeds
- Keep the best result
- Try different initializations: uniform, step-like, Gaussian-smoothed steps

**Iteration 5: Hybrid approach**
- Combine piecewise-linear with exponential decay in certain regions
- Use `f = jax.nn.softplus(w1 * piecewise + w2 * decay)` to enforce positivity and smoothness

### Critical Implementation Details
- **Seed management**: Use `jax.random.PRNGKey(seed)` with seeds 42, 123, 456, 789, 1011 for diversity
- **Learning rate schedule**: Consider adaptive LR: start 0.001, peak 0.01, decay to 0.0001
- **Numerical stability**: Use `jax.lax.stop_gradient` on non-negative constraints to avoid vanishing gradients
- **Early stopping**: Monitor c2 improvement; if no gain in 500 steps, try different initialization

### Evaluation Protocol
1. First, test symmetry-enforced version (expected improvement)
2. Then try multi-start ensemble
3. Finally, attempt hybrid step+decay approach
4. Call `finish()` when best result exceeds 0.8963

### What NOT to Do
- Don't increase intervals without strategy (50 → 200 uniformly)
- Don't use aggressive learning rates (causes instability)
- Don't rely on a single random seed
```

## cand07

- changed fields: `['system_prompt']`
- score: seed `0.9548269841969006` -> best `0.9768788326581587`
- old training reward/advantage: `-0.022914898480091178` / `-0.019555035287110018`
- proposer calls: harness_shell -> harness_shell -> harness_shell -> edit_harness_file -> validate_harness -> submit_harness
- executor calls: LoadSkill({'skill_name': 'discovery-optimization'}) -> edit_solution[hyperparameters,step_or_plateau,exponential_tail,triangular_or_ramp,shape_change] -> evaluate_solution(score=0, valid=0, left=1) -> edit_solution[step_or_plateau,triangular_or_ramp,shape_change] -> evaluate_solution(score=0.976879, valid=1, left=0) -> finish({'summary': 'Improved initialization with plateau (flat-top) function inspired by step functions, plus adjusted learning rate schedule. Achieved combined_score=0.976879, beating baseline 0.954827.'})

Prompt delta:

```markdown
## Task-Specific Strategy for C₂ Optimization

### Objective
Maximize C₂ = ||f ★ f||₂² / ((∫f)² ||f ★ f||_{∞}) where f ≥ 0.
Current best: 0.8962799441554086 (step functions). Target: > 0.8962799441554086.

### Key Insights
1. **Step functions** are the current champion - focus on piecewise-constant or piecewise-linear functions
2. **Symmetry**: Even functions (f(-x) = f(x)) reduce complexity and often work well
3. **Multi-scale optimization**: Start coarse, then refine around promising regions
4. **Better initialization**: Don't start random; start with informed guesses

### Recommended Improvements

#### 1. Function Representation
- Use **piecewise-linear** with N intervals (increase from 50 to 100-200)
- Enforce **non-negativity** via softplus or exponential: f = exp(base)
- Consider **even symmetry**: optimize only x ≥ 0, mirror to x < 0

#### 2. Initialization Strategy
- **Step-function inspired**: Start with a flat-top function
  ```python
  # Initialize with a plateau: high in center, low at edges
  f = jnp.concatenate([
      jnp.linspace(0, 1, N//4),      # ramp up
      jnp.ones(N//2),                 # plateau
      jnp.linspace(1, 0, N//4)       # ramp down
  ])
  ```
- Or **Gaussian-inspired**: smooth bell curve that can evolve into step-like

#### 3. Optimizer Improvements
- Use **Adafactor** or **AdamW** instead of plain Adam
- Implement **two-stage optimization**: coarse grid → fine grid
- Use **learning rate annealing**: start high, decay aggressively
- Add **gradient clipping** for stability

#### 4. Advanced Techniques
- **Multi-resolution**: Optimize on 50 points, then 100, then 200
- **Ensemble averaging**: Combine multiple runs with different seeds
- **Perturbation search**: After convergence, try small structural changes
- **Fourier-based**: Optimize in frequency domain with inverse transform

#### 5. Specific Code Changes
```python
# Replace random init with step-function inspired init
def initialize_step_like(N):
    quarter = N // 4
    return jnp.concatenate([
        jnp.linspace(0.5, 1.0, quarter),
        jnp.ones(quarter * 2),
        jnp.linspace(1.0, 0.5, quarter)
    ])

# Use two-stage optimization
# Stage 1: Coarse grid (50 points), 5000 steps, LR=0.1
# Stage 2: Fine grid (200 points), 10000 steps, LR=0.01
```

### Evaluation Strategy
1. First evaluation: Test the improved initialization
2. If score improves, continue refining
3. If not, try symmetry constraint or multi-scale approach
4. With only 2 evaluations, make each count - test one major idea per eval

### Critical Constraints
- Keep the same entry function signature: `run()` returns `(f_values_np, c2_val, loss_val, N)`
- Preserve all imports and the fixed entry point
- Ensure numerical stability (no NaN/Inf)
- Maintain reproducibility (fixed seeds)
```

