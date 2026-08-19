def run(ctx, args):
    return {
        "templates": [
            {
                "name": "bipartite_middle",
                "code": """
                left = 0.9
                right = 1.1
                width = (right - left) / 2.0
                height = 1.0 / (2.0 * width)
                h = jnp.where((x >= left) & (x <= right), height, 0.0)
                """
            },
            {
                "name": "boundary_peak",
                "code": """
                peak_pos = 0.25
                width = 0.3
                height = 1.0 / (2.0 * width)
                h = jnp.where((x >= peak_pos) & (x <= peak_pos + width), height, 0.0)
                """
            },
            {
                "name": "dual_peaks",
                "code": """
                left = 0.4
                right = 1.6
                width = 0.25
                h1 = jnp.where((x >= left) & (x <= left + width), 4.0, 0.0)
                h2 = jnp.where((x >= right) & (x <= right + width), 4.0, 0.0)
                h = h1 + h2
                """
            },
            {
                "name": "tri_modal",
                "code": """
                peaks = [0.4, 1.0, 1.6]
                width = 0.15
                h = jnp.zeros(N)
                for p in peaks:
                    h = h + jnp.where((x >= p) & (x <= p + width), 4.0, 0.0)
                """
            },
            {
                "name": "symmetric_double",
                "code": """
                center = 1.0
                width = 0.25
                h = jnp.where(
                    (x >= center - 0.5) & (x <= center + 0.5),
                    4.0,
                    0.0
                )
                """
            },
            {
                "name": "asymmetric_taper",
                "code": """
                # Narrow peak at left, wide plateau
                peak_start = 0.1
                peak_width = 0.2
                plateau_start = 0.6
                plateau_width = 1.2
                peak_height = 8.0
                plateau_height = 1.0 / (plateau_width * 2.0)
                h = jnp.where(
                    (x >= peak_start) & (x <= peak_start + peak_width),
                    peak_height,
                    0.0
                ) + jnp.where(
                    (x >= plateau_start) & (x <= plateau_start + plateau_width),
                    plateau_height,
                    0.0
                )
                """
            },
            {
                "name": "golomb_ruler",
                "code": """
                marks = [0.0, 0.5, 1.0, 1.5]
                width = 0.12
                h = jnp.zeros(N)
                for m in marks:
                    mask = (x >= m) & (x <= m + width)
                    h = h.at[mask].set(4.0)
                """
            },
            {
                "name": "boundary_double",
                "code": """
                # Peaks at both boundaries
                left_width = 0.15
                right_width = 0.15
                left_peak = jnp.where((x >= 0.0) & (x <= left_width), 4.0, 0.0)
                right_peak = jnp.where((x >= 2.0 - right_width) & (x <= 2.0), 4.0, 0.0)
                h = left_peak + right_peak
                """
            }
        ],
        "note": "These 8 templates have different structures. Try optimizing each with different hyperparameters. Start with bipartite_middle and boundary_peak as they are simplest."
    }
