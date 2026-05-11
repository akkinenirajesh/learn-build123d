"""Component 3: Y-Axis Rails — two parallel linear rails with bearing blocks."""

from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import hole_at


class YRails(CNCComponent):
    """Two Y-axis linear rails with bolt holes, end supports, and bearing blocks."""

    def build(self) -> Compound:
        c = self.config
        parts: list[Part] = []
        for rail_x in (c.rail_x_left, c.rail_x_right):
            parts.extend(self._build_rail(rail_x))
        return Compound(children=parts)

    def _build_rail(self, rx: float) -> list[Part]:
        c = self.config
        r_rad = c.rail_width / 2  # 10mm
        rz = c.y_rail_z  # 162.5
        ry_mid = c.mid_y
        outer_y = c.base_outer_y

        # Main rail bar (cylinder along Y)
        rail = Pos(rx, ry_mid, rz) * Rot(X=90) * Cylinder(r_rad, outer_y)

        # Subtract bolt holes (vertical, M5 clearance)
        hole_depth = c.rail_height + 10  # 35
        y_start = 40.0
        y_end = outer_y - 40.0
        y = y_start
        while y <= y_end + 0.01:
            hole = hole_at(rx, y, rz, c.bolt_hole_dia, hole_depth, direction=(0, 0, -1))
            rail -= hole
            y += c.bolt_spacing_y

        # End supports (boxes with bolt holes)
        support = Box(30, 15, 30)
        left_sup = Pos(rx, 7.5, rz) * support
        right_sup = Pos(rx, outer_y - 7.5, rz) * support
        for sup, sy in [(left_sup, 7.5), (right_sup, outer_y - 7.5)]:
            for sx_off in (-6, 6):
                h = hole_at(rx + sx_off, sy, rz, c.bolt_hole_dia, 40, direction=(0, 0, -1))
                sup -= h

        # Bearing block at mid-span
        bearing = self._build_bearing_block(rx, ry_mid, rz)

        return [rail, left_sup, right_sup] + bearing

    def _build_bearing_block(self, rx: float, ry: float, rz: float) -> list[Part]:
        c = self.config
        body_x = c.rail_width + 10  # 30
        body_z = c.rail_height + 15  # 40

        # Central body
        body = Pos(rx, ry, rz + 7.5) * Box(body_x, 30, body_z)

        # End caps
        cap_x = c.rail_width + 6  # 26
        cap_z = c.rail_height + 11  # 36
        cap_front = Pos(rx, ry - 17.5, rz + 7.5) * Box(cap_x, 5, cap_z)
        cap_back = Pos(rx, ry + 17.5, rz + 7.5) * Box(cap_x, 5, cap_z)

        # Side wipers
        wiper_front = Pos(rx, ry - 20.5, rz + 7.5) * Box(24, 1, 40)
        wiper_back = Pos(rx, ry + 20.5, rz + 7.5) * Box(24, 1, 40)

        # Top mounting pad
        pad_z = rz + 20 + 1.5  # 184
        pad = Pos(rx, ry, pad_z + 1.5) * Box(30, 30, 3)

        # Subtract M5 bolt holes from pad
        for bx, by in [(rx - 7.5, ry - 10), (rx - 7.5, ry + 10),
                       (rx + 7.5, ry - 10), (rx + 7.5, ry + 10)]:
            h = hole_at(bx, by, pad_z + 3, c.bolt_hole_dia, 15, direction=(0, 0, -1))
            pad -= h

        # Zerk grease fitting
        zerk = Pos(rx - 7.5, ry, rz + 31.5) * Cylinder(3, 8)

        return [body, cap_front, cap_back, wiper_front, wiper_back, pad, zerk]
