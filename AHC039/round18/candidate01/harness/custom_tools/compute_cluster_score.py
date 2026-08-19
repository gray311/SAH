def run(ctx, args):
    grid_r = args.get("grid_r")
    grid_c = args.get("grid_c")
    min_x = args.get("min_x", -1)
    max_x = args.get("max_x", -1)
    min_y = args.get("min_y", -1)
    max_y = args.get("max_y", -1)

    if grid_r is not None and grid_c is not None:
        # Grid cell score
        cell_size = 100000 / 200  # 500
        # Parse program
        prog = ctx.get_program()
        # Extract fish from CPP_CODE or input reading
        # Since we can't easily parse C++, we use ctx.read_input_sample
        # Input format: first N lines mackerels, next N lines sardines
        try:
            content = ctx.scratch_read("scratch_tmp", "")
        except:
            content = ""
        # Actually we need to read from the program's input
        # The program reads stdin, so we can't access it here
        # Use heuristic: estimate based on coords in program
        return {"error": "Use rectangle query instead for accuracy", "grid_r": grid_r, "grid_c": grid_c}
    elif min_x != -1:
        # Rectangle query on fish data from program
        # Parse program to find fish positions
        # The C++ program reads from stdin, so we need to embed fish data
        # This is complex; instead use ctx.read_input_sample
        try:
            # Try to find fish data in program
            prog = ctx.get_program()
            # This approach is unreliable for dynamic input
            return {"error": "Use direct rectangle query on input file"}
        except:
            return {"mackerels": 0, "sardines": 0, "score": 0}
    else:
        return {"error": "Invalid call"}
