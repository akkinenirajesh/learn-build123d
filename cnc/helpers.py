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


def _rotation_for_axis(dx: float, dy: float, dz: float):
    """Return a Rot that aligns Z-axis with (dx, dy, dz), or None if already Z."""
    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    if mag < 1e-9:
        return None
    nx, ny, nz = dx / mag, dy / mag, dz / mag
    if nz > 0.9999:
        return None  # Already Z-aligned
    if nz < -0.9999:
        return Rot(X=180)  # Flip Z
    if nx > 0.9999:
        return Rot(0, 90, 0)  # Z → X
    if nx < -0.9999:
        return Rot(0, -90, 0)  # Z → -X
    if ny > 0.9999:
        return Rot(-90, 0, 0)  # Z → Y
    if ny < -0.9999:
        return Rot(90, 0, 0)  # Z → -Y
    # General case: pitch + roll to align Z with (nx, ny, nz)
    pitch = math.degrees(math.atan2(nx, nz))  # rotation around Y
    roll = math.degrees(math.atan2(-ny, math.sqrt(nx*nx + nz*nz)))  # rotation around X
    return Rot(roll, pitch, 0)


def make_cylinder_between(
    start: Tuple[float, float, float],
    end: Tuple[float, float, float],
    radius: float,
) -> Part:
    """Create a cylinder spanning from start to end point."""
    sx, sy, sz = start
    ex, ey, ez = end
    dx, dy, dz = ex - sx, ey - sy, ez - sz
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    if length < 1e-9:
        return Pos(sx, sy, sz) * Sphere(radius)
    mid = ((sx + ex) / 2, (sy + ey) / 2, (sz + ez) / 2)
    rot = _rotation_for_axis(dx, dy, dz)
    cyl = Cylinder(radius, length)
    if rot is not None:
        cyl = rot * cyl
    return Pos(mid) * cyl


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
    rot = _rotation_for_axis(dx, dy, dz)
    cyl = Cylinder(r, depth)
    if rot is not None:
        cyl = rot * cyl
    return Pos(x, y, z) * cyl
