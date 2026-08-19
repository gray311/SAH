---
name: smart-cascade-search
description: Guide for implementing cascade-aware search with action_analyzer integration. Key - Account for cascade timing when evaluating actions.
---

# Smart Cascade Search for APPLE ARTIS

## Understanding the Cascade
The game has a critical cascade mechanic:
- Turn actions happen FIRST (choose one machine to strengthen)
- THEN all machines cascade in order L0→L1→L2→L3
- L0 produces apples, L1+ multiplies counts of lower levels

## Why Simple Greedy Fails
A greedy "pick highest marginal gain" policy misses the big picture:
- Investing in L3 early when you have few apples is wasteful
- You need L0 to generate apples first to afford L3
- The optimal sequence depends on current apple count

## Smart Search Strategy

### Phase 1: Building Apple Base (apples < 1000)
- Prioritize L0 actions that generate most apples per cost
- Build up B and P of L0 machines
- Don't invest in L3 yet (too expensive relative to apple count)

### Phase 2: Leveraging the Cascade (1000 <= apples < 100000)
- When you have enough apples, start investing in L3
- L3 multiplies L2 counts, which multiply L1, which multiply L0
- Small L3 investment can lead to exponential growth

### Phase 3: Maximizing Production (apples >= 100000)
- Balance L3 investments with continued L0 production
- The cascade has kicked in, so L3 investments compound
- Maximize total output by maintaining both sources

## Using action_analyzer
- Call action_analyzer at the start of each turn
- It considers current apples, cascade multipliers, and affordability
- Search ONLY within its pruned list (top 20 actions)
- Use probe_solution to rank these 20 before full evaluation

## Implementation Checklist
1. Read current state (apples, B, P, costs)
2. Call action_analyzer to get pruned action list
3. For each pruned action:
   - Simulate 100 turns with smart policy based on apple count
   - Track final apple count
4. Pick action with highest projected final apples
5. Execute and cascade, repeat for 500 turns
