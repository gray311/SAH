def run(ctx, args):
    try:
        # Use ctx methods that exist
        result = {}
        result["vertices_count"] = ctx.scratch_read("__poly_vertices__") or "N/A"
        result["perimeter"] = ctx.scratch_read("__poly_perimeter__") or "N/A"
        result["bounding_box"] = ctx.scratch_read("__poly_bbox__") or "N/A"
        return result
    except:
        return {"note": "use edit_solution then probe to check metrics"}
