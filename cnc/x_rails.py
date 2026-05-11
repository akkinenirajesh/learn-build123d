"""Component 6: X-Axis Rails — two rails on the gantry bridge front face."""

from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import hole_at


class XRails(CNCComponent):
    """Two X-axis linear rails (upper and lower) mounted on bridge front face."""

    def build(self) -> Compound:
        c = self.config
        parts: list[Part] = []
        for rz in (c.x_rail_lower_z, c.x_rail_upper_z):
            parts.extend(self._build_rail(rz))
        return Compound(children=parts)

    def _build_rail(self, rz: float) -> list[Part]:
        c = self.config
        r_rad = 7.5  # 15mm dia X-rail
        span = c.bridge_span_x  # 500
        x_start = c.mid_x - span / 2  # 50
        x_end = c.mid_x + span / 2  # 550
        x_mid = c.mid_x
        y_front = c.bridge_y_front  # 220

        # Main rail bar (cylinder along X)
        rail = Pos(x_mid, y_front, rz) * Rot(0, 90, 0) * Cylinder(r_rad, span)

        # Subtract bolt holes (along Y, into bridge)
        hole_depth = c.gantry_bridge_y + 10  # 70
        spacing = c.bolt_spacing_y  # 80
        x = x_start + 40
        while x <= x_end - 35:
            h = hole_at(x, y_front, rz, c.bolt_hole_dia, hole_depth,
                        direction=(0, -1, 0))
            rail -= h
            x += spacing

        # End supports
        support = Box(15, 25, 25)
        left_sup = Pos(x_start + 7.5, y_front + 12.5, rz) * support
        right_sup = Pos(x_end - 7.5, y_front + 12.5, rz) * support
        for sup, sx in [(left_sup, x_start + 7.5), (right_sup, x_end - 7.5)]:
            for sz_off in (-6, 6):
                h = hole_at(sx, y_front + 12.5, rz + sz_off,
                            c.bolt_hole_dia, 65, direction=(0, -1, 0))
                sup -= h

        # Bearing block at mid-span
        bearing = self._build_bearing_block(x_mid, rz)

        return [rail, left_sup, right_sup] + bearing

    def _build_bearing_block(self, bx: float, bz: float) -> list[Part]:
        c = self.config
        y_front = c.bridge_y_front  # 220

        # Central body
        body = Pos(bx, y_front + 12.5, bz) * Box(30, 25, 25)

        # End caps
        cap_l = Pos(bx - 17.5, y_front + 12.5, bz) * Box(5, 21, 21)
        cap_r = Pos(bx + 17.5, y_front + 12.5, bz) * Box(5, 21, 21)

        # Side wipers
        wiper_l = Pos(bx - 20.5, y_front + 12.5, bz) * Box(1, 4, 25)
        wiper_r = Pos(bx + 20.5, y_front + 12.5, bz) * Box(1, 4, 25)

        # Front mounting pad
        pad_y = y_front + 12.5 + 12.5 + 1.5  # 246.5
        pad = Pos(bx, pad_y + 1.5, bz) * Box(30, 3, 25)

        # M5 bolt holes on front pad
        for px, pz in [(bx - 10, bz - 7.5), (bx - 10, bz + 7.5),
                       (bx + 10, bz - 7.5), (bx + 10, bz + 7.5)]:
            h = hole_at(px, pad_y + 3, pz, c.bolt_hole_dia, 15,
                        direction=(0, -1, 0))
            pad -= h

        # Zerk grease fitting
        zerk = Pos(bx - 10, pad_y + 8, bz) * Rot(0, 90, 0) * Cylinder(3, 8)

        return [body, cap_l, cap_r, wiper_l, wiper_r, pad, zerk]
