---
name: debug-validation-errors
description: Troubleshooting guide when the program produces validity=0 or errors.
---

# Debugging Validation Errors

## Common Causes of validity=0

### 1. Perimeter Exceeded
- Perimeter > 400000
- Fix: Reduce polygon size, remove unnecessary vertices, use fewer vertices

### 2. Too Many Vertices
- Vertices > 1000
- Fix: Merge collinear vertices, use simpler polygon shape

### 3. Coordinate Out of Range
- Any vertex has x or y outside [0, 100000]
- Fix: Clamp coordinates to valid range

### 4. Self-Intersection
- Edges cross each other
- Fix: Use non-overlapping construction, check edge ordering

### 5. Duplicate Vertices
- Two vertices at same position
- Fix: Ensure all vertices have distinct coordinates

## Debug Strategy
1. Check error message in evaluate_solution output
2. Add print statements to trace vertex coordinates and perimeter
3. Use analyze_fish_distribution to verify input was read correctly
4. Test with a minimal valid polygon first (4 vertices, rectangle)
5. Gradually add complexity while monitoring constraints
