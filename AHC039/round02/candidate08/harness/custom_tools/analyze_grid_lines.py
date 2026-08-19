def run(ctx, args):
    return {
        "step1_extract": {
            "description": "Get unique X and Y coordinates from mackerels using std::map",
            "cpp_template": "Use std::map<int,int> to count occurrences of each coordinate",
            "note": "Mackerels are at indices 0 to N-1 in your fish array"
        },
        "step2_select": {
            "description": "Select top-k grid lines by mackerel density using std::sort",
            "cpp_template": "Sort map by value descending, take first k elements",
            "note": "Top-k lines by count capture most mackerels"
        },
        "step3_construct": {
            "description": "Build polygon from grid lines - options:",
            "patterns": [
                "Bounding box: (min_x,min_y)->(max_x,min_y)->(max_x,max_y)->(min_x,max_y)",
                "L-shape: Use grid_x[0],grid_x[1],grid_y[0],grid_y[1] for corner split",
                "Union: Multiple small rectangles around dense clusters"
            ],
            "note": "Perimeter must stay <=400000, vertices <=1000"
        },
        "step4_probe": {
            "description": "Use probe_solution before evaluate_solution",
            "note": "probe is ~10x faster, checks subset, separate budget"
        },
        "common_pitfalls": [
            "Do not change input fish arrays",
            "Perimeter constraint: 400000",
            "Vertex count: 4-1000",
            "Time limit: keep search <0.15s",
            "Always verify no self-intersection"
        ],
        "recommendation": "Start with bounding box, then try L-shapes using top-2 grid lines"
    }
