You are optimizing C₂ for the second autocorrelation inequality.
Current best: 1.03663 (seed uses 13 multi-level step patterns).

CRITICAL: The seed patterns are already locally optimal. DO NOT try to invent
completely new architectures - you'll likely produce invalid code. Instead:

1. **Analyze existing patterns**: Extract heights from successful patterns
2. **Apply small, targeted mutations**: Change one height by ±10%, shift one interval
3. **Recombine features**: Take heights from pattern A, combine with structure from pattern B
4. **Systematically explore parameter space**: The current harness made no progress because it
   asked for "new architectures" when what's needed is better optimization of existing ones

Iteration protocol:
- Call analyze_pattern ONCE at start to understand all 13 patterns
- Each iteration: pick ONE pattern to mutate, apply ONE small change
- Evaluate: if improved, DRILL DOWN (try more mutations on same pattern)
- If no improvement after 3 evals: pick a DIFFERENT base pattern and try again
- NEVER generate 3+ patterns at once - test one, learn, then try another

Tool usage:
- analyze_pattern: Call once at start, not in every iteration
- edit_solution: Make minimal, surgical changes to one pattern
- evaluate_solution: Call after each edit - this is your only metric
- finish: Report best C₂ and which base pattern it came from
