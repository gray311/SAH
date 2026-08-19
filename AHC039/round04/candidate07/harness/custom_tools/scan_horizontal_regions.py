def run(ctx, args):
    # Access the fish data - check for common patterns
    all_fish = getattr(ctx, 'all_fish', getattr(ctx, '_all_fish', None))
    if all_fish is None:
        # Try accessing via a different pattern
        try:
            scratch_data = ctx.scratch_read('scan_data')
            if scratch_data:
                all_fish = json.loads(scratch_data)
            else:
                all_fish = []
        except:
            return {"note": "No fish data accessible, skip scan", "bands": []}
    
    if len(all_fish) < 10:
        return {"note": "Too few fish", "bands": []}
    
    # Build y-coordinate -> fish count mapping
    y_to_mackerels = {}
    y_to_sardines = {}
    
    max_y = 100000
    for fish in all_fish[:2000]:  # Limit scan to 2000 fish for speed
        y = fish['y'] if isinstance(fish, dict) else fish.y
        fish_type = fish.get('type', 1) if isinstance(fish, dict) else (1 if fish.type == 1 else -1)
        if y not in y_to_mackerels:
            y_to_mackerels[y] = 0
            y_to_sardines[y] = 0
        if fish_type == 1:  # mackerel
            y_to_mackerels[y] += 1
        else:  # sardine
            y_to_sardines[y] += 1
        
        if len(y_to_mackerels) >= 200:
            break
    
    # Return y-coordinates with high mackerel ratios
    results = []
    for y in sorted(y_to_mackerels.keys()):
        m = y_to_mackerels[y]
        s = y_to_sardines[y]
        total = m + s
        ratio = m / max(1, total)
        results.append({
            "y": y,
            "mackerel_count": m,
            "sardine_count": s,
            "ratio": ratio
        })
    
    # Sort by ratio descending
    results.sort(key=lambda x: x['ratio'], reverse=True)
    return {"bands": results[:30], "total_unique_y": len(results)}