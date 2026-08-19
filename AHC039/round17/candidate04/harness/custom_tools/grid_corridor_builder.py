def run(ctx, args):
    import math

    seed_x = args.get("seed_x")
    seed_y = args.get("seed_y")
    direction = args.get("direction")

    if seed_x is None or seed_y is None or direction is None:
        return {"error": "missing args"}

    # Parse fish positions from program
    program = ctx.get_program()
    mackerels = []
    sardines = []
    lines = program.split("\n")
    for line in lines:
        line = line.strip()
        # Expect: x y for mackerel, or x y for sardine (next N lines are sardines)
        # Heuristic: look for numbers at start
        try:
            xs = [int(x.strip()) for x in line.split() if x.strip().isdigit()]
            if len(xs) >= 2:
                x, y = xs[0], xs[1]
                # Infer type: assume first N in evolve block are mackerels, next N are sardines
                # Count lines to estimate
                count = sum(1 for l in lines[:len(lines)//2] if len([c for c in l.split() if c.strip().isdigit()]) >= 2)
                if "mackerel" in line.lower() or count < len(lines)//2:
                    mackerels.append((x, y))
                else:
                    sardines.append((x, y))
        except:
            continue

    grid_size = 200
    cell_size = 100000 // grid_size

    # Build grid
    grid = [[{"m": 0, "s": 0} for _ in range(grid_size)] for _ in range(grid_size)]
    for mx, my in mackerels:
        cx, cy = mx // cell_size, my // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            grid[cy][cx]["m"] += 1
    for sx, sy in sardines:
        cx, cy = sx // cell_size, sy // cell_size
        if 0 <= cx < grid_size and 0 <= cy < grid_size:
            grid[cy][cx]["s"] += 1

    # Direction deltas
    deltas = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
    dr, dc = deltas[direction]

    # Convert seed to grid cell
    sr, sc = seed_y // cell_size, seed_x // cell_size
    if not (0 <= sr < grid_size and 0 <= sc < grid_size):
        return {"error": "seed out of bounds", "corridor": []}

    corridor = []
    curr_r, curr_c = sr, sc
    while True:
        corridor.append({
            "row": curr_r,
            "col": curr_c,
            "m": grid[curr_r][curr_c]["m"],
            "s": grid[curr_r][curr_c]["s"],
            "score": grid[curr_r][curr_c]["m"] - grid[curr_r][curr_c]["s"]
        })

        # Check stop condition
        curr_m = grid[curr_r][curr_c]["m"]
        curr_s = grid[curr_r][curr_c]["s"]
        if curr_s > curr_m + 1:
            break

        new_r, new_c = curr_r + dr, curr_c + dc
        if not (0 <= new_r < grid_size and 0 <= new_c < grid_size):
            break

        curr_r, curr_c = new_r, new_c

    return {
        "corridor": corridor,
        "length": len(corridor),
        "final_score": corridor[-1]["score"] if corridor else 0
    }
