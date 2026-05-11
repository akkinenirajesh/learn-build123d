"""
Utility helpers for CNC component construction.
"""

import math
from typing import List, Tuple

from build123d import *


def bolt_circle(
    center_x: float, center_y: float, diameter: float, count: int = 4,
    start_angle: float = 45,
) -> List[Tuple[float, float]]:
    """Generate (x, y) positions on a bolt circle in the XY plane.

    Args:
        center_x, center_y: Circle center coordinates.
        diameter: Bolt circle diameter.
        count: Number of bolt positions.
        start_angle: Angle in degrees of first bolt (default 45°).
    """
    radius = diameter / 2
    positions = []
    for i in range(count):
        angle = math.radians(start_angle + i * 360 / count)
        positions.append((center_x + radius * math.cos(angle),
                          center_y + radius * math.sin(angle)))
    return positions


def bolt_holes_along_line(
    start: float, end: float, spacing: float,
    *,
    y: float = 0, z: float = 0,
    hole_dia: float = 5.2, hole_depth: float = 30,
) -> List[Tuple[float, float, float]]:
    """Generate hole center positions along a line (X axis by default).

    Returns list of (x, y, z) positions.
    """
    length = end - start
    if length <= 0:
        return []
    count = max(1, int(length / spacing))
    step = length / count
    first = start + spacing / 2
    positions = []
    for i in range(count):
        x = first + i * step
        if x > end - spacing / 4:
            break
        positions.append((x, y, z))
    return positions


def make_cylinder_between(
    start: Tuple[float, float, float],
    end: Tuple[float, float, float],
    radius: float,
) -> Part:
    """Create a cylinder spanning from start to end point.

    In build123d, Cylinder is Z-axis by default. We position it at the
    midpoint and rotate to align with the start-end vector.
    """
    sx, sy, sz = start
    ex, ey, ez = end
    dx, dy, dz = ex - sx, ey - sy, ez - sz
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    if length < 1e-9:
        # Degenerate — return a sphere at the point
        return Pos(sx, sy, sz) * Sphere(radius)
    mid = ((sx + ex) / 2, (sy + ey) / 2, (sz + ez) / 2)
    c = Pos(mid) * Cylinder(radius, length, direction=(dx, dy, dz))
    return c


def hole_at(
    x: float, y: float, z: float,
    dia: float, depth: float, direction: Tuple[float, float, float] = (0, 0, 1),
) -> Part:
    """Create a cylinder for subtraction (a hole).

    Args:
        x, y, z: Hole center.
        dia: Hole diameter.
        depth: Hole depth (cylinder height).
        direction: Hole axis direction (default +Z).
    """
    r = dia / 2
    dx, dy, dz = direction
    return Pos(x, y, z) * Cylinder(r, depth, direction=(dx, dy, dz))
