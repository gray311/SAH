---
name: systematic-mutation-playbook
description: Concrete playbook for mutating seed patterns systematically. Start from best pattern, apply targeted height/position/width mutations, use c2_analyze for feedback.
---

# Systematic Pattern Mutation Playbook

## NEVER Generate Patterns from Scratch

Always start from the current best pattern. The 13 seed patterns are well-optimized.

## Step 1: Identify the Current Best

Call analyze_current_pattern to see all pattern structures.
The best is likely a multi-level pattern (3-5 levels) with a tall central peak (~2.0-2.3).

## Step 2: Choose Mutation Type

Priority order:
1. **Height tuning** (most effective): Adjust the tallest peak by ±10%, ±5%, ±2%
   - If current center = 2.10, try: 2.0, 2.15, 2.20, 2.25, 2.30
   - Also tune side peaks: 1.50 → 1.45, 1.40
2. **Position shifting**: Move boundaries by 1-2 intervals
   - Central: int(0.40*n) → int(0.39*n) or int(0.41*n)
3. **Width adjustment**: Change peak width by ±10%
   - Narrower: int(0.40*n):int(0.60*n) → int(0.38*n):int(0.62*n)
4. **Wing modifications**: Add/remove small side steps

## Step 3: Apply Single Mutation

Make ONE small change at a time. Don't mutate multiple parameters simultaneously.

## Step 4: Analyze with c2_analyze

After editing, call c2_analyze to see:
- Did L2 norm increase? (good)
- Did infinity norm decrease or stay stable? (good)
- Is the ratio moving up? (promising)

## Step 5: Evaluate Only if Promising

Only call evaluate_solution if c2_analyze shows:
- L2 norm increased AND (infinity norm stable or decreased)
- Ratio already improved in analysis

## Step 6: Iterate or Pivot

- If improving: make finer mutations (±2%, ±1 interval)
- If stuck (5+ iterations): try different mutation type
- If worse: backtrack to last good state

## Example Success Path

1. analyze_current_pattern → pattern 12: heights [0.70, 1.50, 2.10, 1.50, 0.70]
2. c2_analyze on 2.10 → L2=0.85, inf=2.3, ratio=1.036
3. Mutate center to 2.20 → c2_analyze → L2=0.87, inf=2.25, ratio=1.042 (GOOD!)
4. Mutate to 2.25 → c2_analyze → L2=0.88, inf=2.22, ratio=1.044 (BETTER!)
5. Mutate to 2.30 → c2_analyze → L2=0.89, inf=2.20, ratio=1.047 (BETTER!)
6. evaluate_solution → 1.050 (NEW RECORD!)
7. Fine-tune: 2.32, 2.33, 2.31 → find optimum at 2.32

## Key Rules

- ONE mutation per iteration
- Use c2_analyze for feedback before full eval
- Never make large jumps (stick to 2-5% changes initially)
- Once you improve, go deeper, not wider
