def run(ctx, args):
    try:
        # Access the program's best solution to understand what we're working with
        best_code = ctx.get_best_program()
        
        # The task is to find optimal axis-aligned polygon
        # Return heuristic guidance based on typical task characteristics
        
        return {
            "task_type": "fish_polygon_optimization",
            "recommended_approach": "bounding_box_with_sardine_exclusion",
            "heuristic": "Start with minimal bounding box of mackerels, then expand to cover more while avoiding sardine clusters",
            "key_strategies": [
                "1. Bounding box of all mackerels - covers 100% of mackerels",
                "2. Centroid-centered rectangle - balances coverage",
                "3. L-shaped polygon - excludes sardine regions",
                "4. Multi-rectangle union - flexible coverage with perimeter constraints"
            ],
            "constraints_reminder": {
                "max_vertices": 1000,
                "max_perimeter": 400000,
                "edge_alignment": "axis_parallel_only",
                "coordinate_range": "0_to_100000"
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "recommended_approach": "bounding_box_with_sardine_exclusion",
            "heuristic": "Start with minimal bounding box of mackerels"
        }
