def run(ctx, args):
    grid_size = 100
    cell_size = 100000 // grid_size  # 1000 per cell

    grid = [[{"m": 0, "s": 0} for _ in range(grid_size)] for _ in range(grid_size)]

    # Get fish positions from input
    names = ctx.list_task_inputs()
    if not names:
        return {"error": "no task inputs"}

    input_text = ctx.read_input_sample(names[0], nrows=10000)
    
    mackerels = []
    sardines = []
    
    lines = input_text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            try:
                x, y = int(parts[0]), int(parts[1])
                cx, cy = x // cell_size, y // cell_size
                if 0 <= cx < grid_size and 0 <= cy < grid_size:
                    if i < 5000:
                        grid[cy][cx]["m"] += 1
                        mackerels.append((x, y))
                    else:
                        grid[cy][cx]["s"] += 1
                        sardines.append((x, y))
            except:
                continue

    # Compute density scores
    for cy in range(grid_size):
        for cx in range(grid_size):
            score = grid[cy][cx]["m"] - grid[cy][cx]["s"]
            grid[cy][cx]["score"] = score
            grid[cy][cx]["key"] = (cx, cy)

    # Return top cells by score
    cells_with_scores = []
    for cy in range(grid_size):
        for cx in range(grid_size):
            cells_with_scores.append(grid[cy][cx])

    # Sort by score descending
    cells_with_scores.sort(key=lambda c: c["score"], reverse=True)

    return {
        "grid_size": grid_size,
        "cell_size": cell_size,
        "top_50_cells": cells_with_scores[:50],
        "grid_stats": {
            "avg_m_per_cell": sum(c["m"] for c in cells_with_scores) / (grid_size * grid_size),
            "avg_s_per_cell": sum(c["s"] for c in cells_with_scores) / (grid_size * grid_size),
            "max_score": max(c["score"] for c in cells_with_scores),
            "min_score": min(c["score"] for c in cells_with_scores)
        }
    }
