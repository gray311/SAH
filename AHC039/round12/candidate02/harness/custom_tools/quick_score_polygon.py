def run(ctx, args):
    polygon = args.get("polygon")
    if not polygon or len(polygon) < 4:
        return {"error": "invalid polygon"}
    
    # Extract fish positions from program
    program_text = ctx.get_program()
    mackerels = []
    sardines = []
    
    for line in program_text.split('\n'):
        line = line.strip()
        if 'mackerel' in line.lower() and '[' in line:
            try:
                idx = line.find('[') + 1
                end = line.find(']', idx)
                if idx < end:
                    coords = line[idx:end].split(',')
                    if len(coords) >= 2:
                        x, y = int(coords[0].strip()), int(coords[1].strip())
                        mackerels.append((x, y))
            except:
                pass
        elif 'sardine' in line.lower() and '[' in line:
            try:
                idx = line.find('[') + 1
                end = line.find(']', idx)
                if idx < end:
                    coords = line[idx:end].split(',')
                    if len(coords) >= 2:
                        x, y = int(coords[0].strip()), int(coords[1].strip())
                        sardines.append((x, y))
            except:
                pass
    
    # For rectangle-based polygon, use bounding box scoring
    # This is still faster than full polygon scan
    if len(polygon) >= 4:
        min_x = min(p['x'] for p in polygon)
        max_x = max(p['x'] for p in polygon)
        min_y = min(p['y'] for p in polygon)
        max_y = max(p['y'] for p in polygon)
        
        # Count fish in bounding box
        m_count = sum(1 for mx, my in mackerels if min_x <= mx <= max_x and min_y <= my <= max_y)
        s_count = sum(1 for sx, sy in sardines if min_x <= sx <= max_x and min_y <= sy <= max_y)
        
        score = max(0, m_count - s_count + 1)
        return {"score": score, "mackerels": m_count, "sardines": s_count}
    return {"error": "too few vertices"}
