"""Component 5: Gantry Bridge — hollow box beam with diagonal lattice ribs."""

from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import make_cylinder_between


class GantryBridge(CNCComponent):
    """Hollow gantry bridge beam spanning X between uprights,
    with internal diagonal cross-braced lattice ribs."""

    def build(self) -> Compound:
        c = self.config
        span_x = c.bridge_span_x  # 500
        by_dim = c.gantry_bridge_y  # 60
        bz_dim = c.gantry_bridge_z  # 80
        t = c.gantry_wall_thick  # 8
        cx = c.mid_x
        cy = c.mid_y
        bz = c.bridge_z  # 415

        # --- Hollow beam ---
        outer = Pos(cx, cy, bz) * Box(span_x, by_dim, bz_dim)
        inner = Pos(cx, cy, bz) * Box(
            span_x - 2 * t, by_dim - 2 * t, bz_dim - 2 * t,
        )
        beam = outer - inner

        # --- Diagonal lattice ribs ---
        ribs: list[Part] = []
        rr = c.rib_thick / 2  # 5mm
        x_min = cx - span_x / 2 + t  # 58
        x_max = cx + span_x / 2 - t  # 542
        y_front = cy - by_dim / 2 + t  # 228
        y_back = cy + by_dim / 2 - t  # 272
        z_bot = bz - bz_dim / 2 + t  # 383
        z_top = bz + bz_dim / 2 - t  # 447

        x = x_min
        while x < x_max - c.bridge_rib_spacing_x / 2:
            x_next = min(x + c.bridge_rib_spacing_x, x_max)

            for y_face in (y_front, y_back):
                # Forward diagonal
                ribs.append(make_cylinder_between(
                    (x, y_face, z_bot), (x_next, y_face, z_top), rr))
                # Backward diagonal
                ribs.append(make_cylinder_between(
                    (x, y_face, z_top), (x_next, y_face, z_bot), rr))
                # Vertical strut
                ribs.append(make_cylinder_between(
                    (x, y_face, z_bot), (x, y_face, z_top), rr))

            x += c.bridge_rib_spacing_x

        # --- End mounting bosses ---
        boss_over = c.bridge_end_boss_overhang  # 10
        boss = Box(c.upright_x + boss_over, by_dim + boss_over, bz_dim + boss_over)
        left_boss = Pos(c.rail_x_left, cy, bz) * boss
        right_boss = Pos(c.rail_x_right, cy, bz) * boss

        # --- Compose ---
        result = beam
        for rib in ribs:
            result += rib
        result += left_boss
        result += right_boss

        return result
