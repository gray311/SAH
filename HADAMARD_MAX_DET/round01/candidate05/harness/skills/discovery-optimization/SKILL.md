---
name: discovery-optimization
description: "Optimize Hadamard matrix construction (29\u00d729, \u00b11 entries) to maximize determinant magnitude.\nUse probe_solution for cheap ranking before evaluate_solution. Focus on combinatorial\nconstruction strategies over local search."
---

# Hadamard Matrix Optimization Strategy

## Core Insight
Hadamard determinant maximization is a combinatorial problem. The seed's hill-climbing
is TOO SLOW and gets stuck. You must try DIFFERENT CONSTRUCTIONS.

## Multi-Phase Strategy

### Phase 1: Probe-Driven Exploration (Use ALL probes)
- Call probe_solution on your edited code (FAST, ~10s, separate budget)
- Make 3-5 variants with DIFFERENT construction methods:
  * Paley construction (using different quadratic residue sets)
  * Modified random initialization with structured perturbations
  * Different hill-climbing schedules (temperatures, iterations)
  * Block-based constructions
- Keep the TOP 3 by probe score

### Phase 2: Confirm Best Candidate (Use sparingly)
- Call evaluate_solution ONCE on the #1 probed variant
- If it improves, use that as new best; otherwise try different construction

## Construction Methods to Try
1. **Paley Construction**: H[i][j] = 1 if (i-j) is QR mod p, else -1 (p ≡ 3 mod 4)
2. **Modified Quadratic Residues**: Try different offset transformations
3. **Random Seeds**: Try multiple random seeds (0, 1, 42, 123, 456)
4. **Multiple Restarts**: Run hill-climbing with different starting points
5. **Block Construction**: Use small structured blocks that tile together

## Critical Rules
- NEVER call evaluate_solution without first probing
- NEVER try hill-climbing parameter tuning alone - change the CONSTRUCTION
- ALWAYS use probe_solution to compare multiple variants
- Keep internal search WELL UNDER 350s (aim for <200s to be safe)
- Each edit must change the CONSTRUCTION method, not just parameters

## When to Call Each Tool
- edit_solution: Always, to implement a new construction method
- probe_solution: ALWAYS after editing, before any full evaluation
- evaluate_solution: ONLY ONCE per best probed candidate
- finish: When budget exhausted or no improvement after exhaustive probing
