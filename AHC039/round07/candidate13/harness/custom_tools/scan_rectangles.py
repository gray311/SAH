def run(ctx, args):
    count = args.get("count", 50)
    k = args.get("k", 10)
    
    import random
    rects = []
    for _ in range(count):
        x1 = random.randint(0, 50000)
        y1 = random.randint(0, 50000)
        x2 = random.randint(x1 + 1, 100000)
        y2 = random.randint(y1 + 1, 100000)
        rects.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2})
    
    scored = []
    for r in rects:
        score = random.randint(0, 1000)  # Placeholder for actual scoring
        scored.append({"rect": r, "score": score})
    
    scored.sort(key=lambda x: x["score"], reverse=True)
    return {"top_rects": scored[:k], "total_scored": len(scored)}
