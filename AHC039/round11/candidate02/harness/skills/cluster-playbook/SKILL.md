---
name: cluster-playbook
description: Direct cluster analysis with large shifts. Find mackerel groups via 10000-unit proximity, build bounding boxes, connect clusters, aggressive hill climbing with ±500..5000 shifts.
---

# Cluster Playbook

## Core Idea
Find mackerel clusters via 10000-unit proximity, build bounding boxes, connect top clusters, use LARGE hill climbing shifts.

## Steps
1. Parse mackerel coordinates
2. Cluster using 10000-unit proximity
3. Build bounding boxes for each cluster
4. Select top 10-15 by net score
5. Connect with corridors
6. AGGRESSIVE hill climbing: shifts ±500..5000, 2 rounds
7. 10-15 diverse restarts

## Key Difference
Use LARGE shifts (±500..5000) instead of small shifts (±5..25). This allows moving edges between fish clusters for dramatic score improvements.
