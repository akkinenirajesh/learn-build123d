"""Component 1: Base Frame — hollow box with internal lattice ribs and corner feet."""

from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import make_cylinder_between


class BaseFrame(CNCComponent):
    """Hollow rectangular base with internal rib structure and corner feet."""

    def build(self) -> Compound:
        c = self.config
        outer_x, outer_y, outer_z = c.base_outer_x, c.base_outer_y, c.base_outer_z
        t = c.base_wall_thick
        cx, cy = c.mid_x, c.mid_y

        # --- Hollow shell (walls on all 6 sides) ---
        outer = Pos(cx, cy, outer_z / 2) * Box(outer_x, outer_y, outer_z)
        inner = Pos(cx, cy, outer_z / 2) * Box(
            outer_x - 2 * t, outer_y - 2 * t, outer_z - 2 * t
        )
        hollow = outer - inner

        # --- Y-direction ribs (rectangular frames at Y intervals) ---
        ribs_y: list[Part] = []
        inner_x_min = t
        inner_x_max = outer_x - t
        inner_z_bot = t
        inner_z_top = outer_z - t
        rr = c.rib_thick / 2  # 5mm

        y = c.rib_spacing
        while y < outer_y - c.rib_spacing / 2:
            beams: list[Part] = []
            # Bottom beam along X
            beams.append(make_cylinder_between(
                (inner_x_min, y, inner_z_bot),
                (inner_x_max, y, inner_z_bot), rr))
            # Top beam along X
            beams.append(make_cylinder_between(
                (inner_x_min, y, inner_z_top),
                (inner_x_max, y, inner_z_top), rr))
            # Left vertical
            beams.append(make_cylinder_between(
                (inner_x_min, y, inner_z_bot),
                (inner_x_min, y, inner_z_top), rr))
            # Right vertical
            beams.append(make_cylinder_between(
                (inner_x_max, y, inner_z_bot),
                (inner_x_max, y, inner_z_top), rr))
            # Center vertical
            beams.append(make_cylinder_between(
                (cx, y, inner_z_bot),
                (cx, y, inner_z_top), rr))
            for b in beams:
                ribs_y.append(b)
            y += c.rib_spacing

        # --- X-direction ribs ---
        ribs_x: list[Part] = []
        inner_y_min = t
        inner_y_max = outer_y - t

        x = c.rib_spacing
        while x < outer_x - c.rib_spacing / 2:
            beams: list[Part] = []
            # Bottom beam along Y
            beams.append(make_cylinder_between(
                (x, inner_y_min, inner_z_bot),
                (x, inner_y_max, inner_z_bot), rr))
            # Top beam along Y
            beams.append(make_cylinder_between(
                (x, inner_y_min, inner_z_top),
                (x, inner_y_max, inner_z_top), rr))
            # Left vertical (at Y=inner_y_min)
            beams.append(make_cylinder_between(
                (x, inner_y_min, inner_z_bot),
                (x, inner_y_min, inner_z_top), rr))
            # Right vertical (at Y=inner_y_max)
            beams.append(make_cylinder_between(
                (x, inner_y_max, inner_z_bot),
                (x, inner_y_max, inner_z_top), rr))
            # Center vertical
            beams.append(make_cylinder_between(
                (x, cy, inner_z_bot),
                (x, cy, inner_z_top), rr))
            for b in beams:
                ribs_x.append(b)
            x += c.rib_spacing

        # --- Corner feet ---
        foot_size = 40.0
        foot_h = 20.0
        foot = Box(foot_size, foot_size, foot_h)
        corners = [
            (foot_size / 2, foot_size / 2),
            (outer_x - foot_size / 2, foot_size / 2),
            (foot_size / 2, outer_y - foot_size / 2),
            (outer_x - foot_size / 2, outer_y - foot_size / 2),
        ]
        feet = [Pos(fx, fy, foot_h / 2) * foot for fx, fy in corners]

        # --- Compose ---
        result = hollow
        for rib in ribs_y:
            result += rib
        for rib in ribs_x:
            result += rib
        for f in feet:
            result += f

        return result
