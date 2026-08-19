def run(ctx, args):
    program = ctx.get_program()
    mackerels = []
    sardines = []
    for line in program.split('\n'):
        if 'mackerel' in line.lower():
            try:
                parts = line.replace('mackerel', '').replace(']', '').split(',')
                if len(parts) >= 2:
                    mackerels.append((int(parts[0].strip()), int(parts[1].strip())))
            except:
                pass
        elif 'sardine' in line.lower():
            try:
                parts = line.replace('sardine', '').replace(']', '').split(',')
                if len(parts) >= 2:
                    sardines.append((int(parts[0].strip()), int(parts[1].strip())))
            except:
                pass
    
    # Spatial hashing
    hash_size = 100
    m_hash = {}
    s_hash = {}
    for (x, y) in mackerels:
        hx, hy = x // (100000/hash_size), y // (100000/hash_size)
        key = (hx, hy)
        if key not in m_hash:
            m_hash[key] = []
        m_hash[key].append((x, y))
    
    for (x, y) in sardines:
        hx, hy = x // (100000/hash_size), y // (100000/hash_size)
        key = (hx, hy)
        if key not in s_hash:
            s_hash[key] = []
        s_hash[key].append((x, y))
    
    m_clusters = {}
    for (hx, hy), pts in m_hash.items():
        key = (hx, hy)
        m_clusters[key] = {"points": pts, "m_count": len(pts), "s_count": 0, "m_ratio": 1.0}
    
    for (hx, hy), pts in s_hash.items():
        key = (hx, hy)
        if key in m_clusters:
            m_clusters[key]["s_count"] = len(pts)
            m_clusters[key]["m_ratio"] = m_clusters[key]["m_count"] / (m_clusters[key]["m_count"] + len(pts))
        else:
            m_clusters[key] = {"points": pts, "m_count": len(pts), "s_count": 0, "m_ratio": 0.0}
    
    m_dense = [(k, v) for k, v in m_clusters.items() if v["m_ratio"] >= 0.6 and v["m_count"] >= 5]
    s_dense = [(k, v) for k, v in m_clusters.items() if v["s_count"] >= 3 and v["m_count"] >= v["s_count"]]
    
    return {
        "mackerel_dense_clusters": m_dense,
        "sardine_dense_clusters": s_dense,
        "total_mackerels": len(mackerels),
        "total_sardines": len(sardines)
    }
