# EVOLVE-BLOCK-START
"""Simulated annealing with multiple restarts - optimized"""
import numpy as np


def construct_packing():
    """
    Construct an optimized arrangement of 26 circles in a unit square
    that maximizes the sum of their radii.
    
    Uses simulated annealing with multiple restarts:
    - Try several different initial configurations
    - Each uses SA to escape local optima
    """
    n = 26
    
    global_best_sum = 0
    global_best_centers = None
    
    # Try multiple restarts with different seeds
    for restart in range(3):
        np.random.seed(42 + restart * 100)
        centers = np.random.uniform(0.05, 0.95, (n, 2))
        
        # Compute initial radii
        radii = compute_max_radii(centers)
        radii = np.maximum(radii, 0.001)
        current_sum = np.sum(radii)
        
        # Simulated annealing parameters
        best_centers_local = centers.copy()
        best_sum_local = current_sum
        T = 4.0
        cooling_rate = 0.995
        max_iterations = 4000
        
        for iteration in range(max_iterations):
            # Try a random move
            i = np.random.randint(n)
            delta_x = np.random.uniform(-0.06, 0.06)
            delta_y = np.random.uniform(-0.06, 0.06)
            
            new_centers = centers.copy()
            new_centers[i] = np.clip(centers[i] + [delta_x, delta_y], 0.01, 0.99)
            
            # Compute new radii
            new_radii = compute_max_radii(new_centers)
            new_radii = np.maximum(new_radii, 0.001)
            new_sum = np.sum(new_radii)
            
            # Accept or reject
            delta = new_sum - current_sum
            if delta > 0 or np.random.random() < np.exp(delta / T):
                centers = new_centers
                current_sum = new_sum
                
                if current_sum > best_sum_local:
                    best_sum_local = current_sum
                    best_centers_local = centers.copy()
            
            T *= cooling_rate
        
        if best_sum_local > global_best_sum:
            global_best_sum = best_sum_local
            global_best_centers = best_centers_local
    
    centers = global_best_centers
    radii = compute_max_radii(centers)
    radii = np.maximum(radii, 0.001)
    sum_radii = np.sum(radii)
    
    return centers, radii, sum_radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    radius = min(x, y, 1 - x, 1 - y)
    
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.
    """
    n = centers.shape[0]
    radii = np.ones(n)

    for i in range(n):
        x, y = centers[i]
        radii[i] = min(x, y, 1 - x, 1 - y)

    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            if radii[i] + radii[j] > dist:
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii


def compute_radius_at_position(x, y, idx, existing_centers):
    """
    Compute the maximum radius for a circle at position (x, y)
    given existing circles.
    """
    # Distance to borders
    radius = min(x, y, 1 - x, 1 - y)
    
    # Distance to existing circles
    for j in range(len(existing_centers)):
        cx, cy = existing_centers[j]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Conservative estimate: assume equal radii
        radius = min(radius, dist / 2)
    
    return radius


def compute_max_radii(centers):
    """
    Compute the maximum possible radii for each circle position
    such that they don't overlap and stay within the unit square.

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates

    Returns:
        np.array of shape (n) with radius of each circle
    """
    n = centers.shape[0]
    radii = np.ones(n)

    # First, limit by distance to square borders
    for i in range(n):
        x, y = centers[i]
        # Distance to borders
        radii[i] = min(x, y, 1 - x, 1 - y)

    # Then, limit by distance to other circles
    # Each pair of circles with centers at distance d can have
    # sum of radii at most d to avoid overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt(np.sum((centers[i] - centers[j]) ** 2))

            # If current radii would cause overlap
            if radii[i] + radii[j] > dist:
                # Scale both radii proportionally
                scale = dist / (radii[i] + radii[j])
                radii[i] *= scale
                radii[j] *= scale

    return radii
# EVOLVE-BLOCK-END
# This part remains fixed (not evolved)
def run_packing():
    """Run the circle packing constructor for n=26"""
    centers, radii, sum_radii = construct_packing()
    return centers, radii, sum_radii


def visualize(centers, radii):
    """
    Visualize the circle packing

    Args:
        centers: np.array of shape (n, 2) with (x, y) coordinates
        radii: np.array of shape (n) with radius of each circle
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw unit square
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.grid(True)

    # Draw circles
    for i, (center, radius) in enumerate(zip(centers, radii)):
        circle = Circle(center, radius, alpha=0.5)
        ax.add_patch(circle)
        ax.text(center[0], center[1], str(i), ha="center", va="center")

    plt.title(f"Circle Packing (n={len(centers)}, sum={sum(radii):.6f})")
    plt.show()


if __name__ == "__main__":
    centers, radii, sum_radii = run_packing()
    print(f"Sum of radii: {sum_radii}")
    # AlphaEvolve improved this to 2.635

    # Uncomment to visualize:
    visualize(centers, radii)