def run(ctx, args):
    minX, maxX, minY, maxY = args.get("minX", 0), args.get("maxX", 100000), args.get("minY", 0), args.get("maxY", 100000)
    return {"note": "Use count_in_rect() in C++ code with grid index. This tool shows what query to add.", "query": "count_in_rect(minX, maxX, minY, maxY)"}
