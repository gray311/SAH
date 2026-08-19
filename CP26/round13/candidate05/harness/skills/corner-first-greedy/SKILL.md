---
name: corner-first-greedy
description: Place smallest circles in 4 corners first, then edges, then interior. This captures wasted corner space that symmetric packings miss. AUTO-ENACTED.
---

# Corner-First Greedy Construction

**Strategy:** Abandon concentric rings. Place circles in order: corners → edges → interior.

**Step 1: Corners (4 circles)**
- Place at (0.05, 0.05), (0.95, 0.05), (0.05, 0.95), (0.95, 0.95)
- These capture wasted corner space

**Step 2: Edges (8 circles)**
- Top/bottom: (0.25, 0.05), (0.75, 0.05), (0.25, 0.95), (0.75, 0.95)
- Left/right: (0.05, 0.25), (0.05, 0.75), (0.95, 0.25), (0.95, 0.75)

**Step 3: Interior (14 circles)**
- Use greedy placement: for each position, maximize radius given all prior circles
- Try positions along diagonals and midlines
- Allow radii to vary based on local constraints

**Key insight:** Corner-first breaks symmetry and captures ~0.3-0.5 radius sum that rings waste.
