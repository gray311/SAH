---
name: verified-mutation-protocol
description: One-mutation-at-a-time protocol with mandatory verification. Prevents invalid edits and wasted evals.
---

# Verified Single-Mutation Protocol for C₂ Maximization

## CRITICAL: ONE MUTATION PER EDIT

The seed's 13 step patterns are fragile. You MUST:

1. Call pattern_mutator for ONE mutation proposal
2. Call mutation_verifier BEFORE editing (MANDATORY - don't skip!)
3. Implement ONLY that mutation with edit_solution
4. Evaluate with evaluate_solution
5. If improvement: repeat with same mutation TYPE
6. If NO improvement after 3 attempts: try next mutation TYPE
7. Only after exhausting all 4 types, try new architectures

## Why Verification is Mandatory

- Syntax errors: The seed has precise boundary calculations (int(0.25*n)). A bad edit breaks the whole program.
- Semantic errors: Small changes (<1%) don't meaningfully alter the function.
- Type consistency: Ensure the edit matches what pattern_mutator proposed.

## Mutation Types (in order)

### Type 1: Single Height Perturbation (try 3 variants)
- Change ONE peak height by +0.05 to +0.10
- Example: 1.40 → 1.45
- Verify with mutation_verifier before edit

### Type 2: Single Width Adjustment (try 3 variants)
- Change ONE interval boundary by 3-8%
- Example: int(0.25*n) → int(0.26*n)
- Verify with mutation_verifier before edit

### Type 3: Single Center Shift (try 3 variants)
- Shift ONE boundary pair by 1-3%
- Example: 0.25n → 0.26n and 0.75n → 0.76n
- Verify with mutation_verifier before edit

### Type 4: Asymmetric Pair Adjustment (try 3 variants)
- Change TWO adjacent heights with opposite perturbations
- Example: 1.40 → 1.43 and 1.45 → 1.42
- Verify with mutation_verifier before edit

## Failure Patterns to Avoid

- ❌ Implementing multiple mutations in one edit (only ONE parameter per edit)
- ❌ Skipping mutation_verifier (trust it to catch your errors)
- ❌ Changing multiple heights/widths simultaneously
- ❌ Trying to "fix" a bad edit without calling pattern_mutator first

## Execution Loop

for mutation_type in [Type1, Type2, Type3, Type4]:
    for attempt in 1..3:
        pattern = pattern_mutator(mutation_type=mutation_type)
        if not mutation_verifier(pattern).verified:
            continue
        edit_solution(pattern.verified_code)
        score = evaluate_solution()
        if score > best_score:
            best_score = score
            continue
        else:
            break  # Try next mutation type
    if best_improved:
        # Continue with same mutation_type
        continue
    else:
        # Move to next mutation type
        pass
        
If all types exhausted without improvement, then try new architectures.
