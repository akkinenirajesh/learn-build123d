"""Component 10: Lead Screws — three T12 drive screws with thread rings,
anti-backlash nut blocks, shaft collars, and end bearings."""

import math
from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import make_cylinder_between, hole_at


class LeadScrews(CNCComponent):
    """Three T12 lead screws (Y, X, Z) with spiral thread rings,
    anti-backlash nut blocks, shaft collars, and end bearings."""

    # Thread ring dimensions
    RING_OD = 14.0
    RING_WIDTH = 2.0
    RING_PITCH = 4.0  # spacing between rings
    RING_OFFSET = 0.5  # alternating offset for spiral appearance

    # Collar dimensions
    COLLAR_OD = 18.0
    COLLAR_WIDTH = 8.0

    # Bearing block dimensions
    BEARING_SIZE = 25.0
    BEARING_THICK = 20.0

    def build(self) -> Compound:
        c = self.config
        parts: list[Part] = []

        # Y-axis screw
        parts.extend(self._build_screw_assembly(
            (c.mid_x, c.y_screw_start_y, c.y_screw_z),
            (c.mid_x, c.y_screw_end_y, c.y_screw_z),
            (c.mid_x, c.mid_y, c.y_screw_z),
            axis='y',
        ))

        # X-axis screw
        parts.extend(self._build_screw_assembly(
            (c.x_screw_start_x, c.mid_y - c.gantry_bridge_y / 2 - 19, c.x_screw_z),
            (c.x_screw_end_x, c.mid_y - c.gantry_bridge_y / 2 - 19, c.x_screw_z),
            (c.mid_x, c.mid_y - c.gantry_bridge_y / 2 - 19, c.x_screw_z),
            axis='x',
        ))

        # Z-axis screw
        parts.extend(self._build_screw_assembly(
            (c.mid_x, c.z_screw_y, c.z_screw_bot_z),
            (c.mid_x, c.z_screw_y, c.z_screw_top_z),
            (c.mid_x, c.z_screw_y, c.bridge_z),
            axis='z',
        ))

        return Compound(children=parts)

    def _build_screw_assembly(
        self, start: tuple, end: tuple, nut_pos: tuple, axis: str,
    ) -> list[Part]:
        """Build a complete screw: core + thread rings + nut block + collars + bearings."""
        c = self.config
        parts: list[Part] = []
        r = c.lead_screw_dia / 2  # 6mm

        # --- Core shaft ---
        shaft = make_cylinder_between(start, end, r)
        parts.append(shaft)

        # --- Thread rings (alternating offset for spiral look) ---
        sx, sy, sz = start
        ex, ey, ez = end
        length = math.sqrt((ex - sx)**2 + (ey - sy)**2 + (ez - sz)**2)
        num_rings = max(1, int(length / self.RING_PITCH))
        step = length / num_rings

        dir_x = (ex - sx) / length if length > 0 else 0
        dir_y = (ey - sy) / length if length > 0 else 0
        dir_z = (ez - sz) / length if length > 0 else 1

        for i in range(num_rings):
            t = i * step + step / 2  # position along screw
            rx = sx + dir_x * t
            ry = sy + dir_y * t
            rz = sz + dir_z * t

            # Alternating offset pattern for spiral appearance
            offset_idx = i % 4
            ox = oy = oz = 0.0
            if axis == 'y':
                if offset_idx == 0:
                    ox = self.RING_OFFSET
                elif offset_idx == 1:
                    oz = self.RING_OFFSET
                elif offset_idx == 2:
                    ox = -self.RING_OFFSET
                else:
                    oz = -self.RING_OFFSET
            elif axis == 'x':
                if offset_idx == 0:
                    oy = self.RING_OFFSET
                elif offset_idx == 1:
                    oz = self.RING_OFFSET
                elif offset_idx == 2:
                    oy = -self.RING_OFFSET
                else:
                    oz = -self.RING_OFFSET
            else:  # Z
                if offset_idx == 0:
                    ox = self.RING_OFFSET
                elif offset_idx == 1:
                    oy = self.RING_OFFSET
                elif offset_idx == 2:
                    ox = -self.RING_OFFSET
                else:
                    oy = -self.RING_OFFSET

            ring_center = (rx + ox, ry + oy, rz + oz)
            ring_start = (rx + ox - dir_x * self.RING_WIDTH / 2,
                          ry + oy - dir_y * self.RING_WIDTH / 2,
                          rz + oz - dir_z * self.RING_WIDTH / 2)
            ring_end = (rx + ox + dir_x * self.RING_WIDTH / 2,
                        ry + oy + dir_y * self.RING_WIDTH / 2,
                        rz + oz + dir_z * self.RING_WIDTH / 2)
            ring = make_cylinder_between(ring_start, ring_end, self.RING_OD / 2)
            parts.append(ring)

        # --- Nut block at mid position ---
        nut = self._build_nut_block(nut_pos, (dir_x, dir_y, dir_z))
        parts.append(nut)

        # --- Shaft collars (2 at each end) ---
        for collar_p in [start, end]:
            cx_s, cy_s, cz_s = collar_p
            # Move collar 15mm inward from end
            cx_s += dir_x * 15
            cy_s += dir_y * 15
            cz_s += dir_z * 15

            collar_start = (cx_s - dir_x * self.COLLAR_WIDTH / 2,
                            cy_s - dir_y * self.COLLAR_WIDTH / 2,
                            cz_s - dir_z * self.COLLAR_WIDTH / 2)
            collar_end = (cx_s + dir_x * self.COLLAR_WIDTH / 2,
                          cy_s + dir_y * self.COLLAR_WIDTH / 2,
                          cz_s + dir_z * self.COLLAR_WIDTH / 2)
            collar = make_cylinder_between(collar_start, collar_end, self.COLLAR_OD / 2)
            parts.append(collar)

        # --- End bearings ---
        for bearing_p in [start, end]:
            bx_s, by_s, bz_s = bearing_p
            bearing = Pos(bx_s, by_s, bz_s) * Box(
                self.BEARING_SIZE, self.BEARING_SIZE, self.BEARING_THICK)
            parts.append(bearing)

        return parts

    def _build_nut_block(
        self, center: tuple, axis: tuple,
    ) -> Part:
        """Anti-backlash split nut block with spring."""
        c = self.config
        cx, cy, cz = center
        adx, ady, adz = axis
        size = c.nut_block_size  # 25

        # Main block
        block = Pos(cx, cy, cz) * Box(size, size, size)

        # Screw bore through center
        bore_r = c.lead_screw_dia / 2
        bore_length = size + 10
        if abs(adz) > 0.9:
            bore = Pos(cx, cy, cz) * Cylinder(bore_r, bore_length)
        elif abs(adx) > 0.9:
            bore = Pos(cx, cy, cz) * Rot(0, 90, 0) * Cylinder(bore_r, bore_length)
        else:
            bore = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(bore_r, bore_length)
        block -= bore

        # Split gap (1mm)
        if abs(adz) > 0.9:
            gap = Pos(cx, cy, cz) * Box(size + 10, 1, size + 10)
        elif abs(adx) > 0.9:
            gap = Pos(cx, cy, cz) * Box(1, size + 10, size + 10)
        else:
            gap = Pos(cx, cy, cz) * Box(size + 10, size + 10, 1)
        block -= gap

        # Spring pocket
        pocket_od = 10.0
        pocket_depth = 15.0
        if abs(adz) > 0.9:
            pocket = Pos(cx, cy + 8, cz) * Cylinder(pocket_od / 2, pocket_depth)
        elif abs(adx) > 0.9:
            pocket = Pos(cx, cy, cz + 8) * Cylinder(pocket_od / 2, pocket_depth)
        else:
            pocket = Pos(cx + 8, cy, cz) * Cylinder(pocket_od / 2, pocket_depth)
        block -= pocket

        # Spring inside pocket
        spring = Pos(cx + 8, cy, cz - 5) * Cylinder(4, 12)
        block += spring

        # M4 bolt holes
        for offset in (-10, 10):
            if abs(adz) > 0.9:
                bh = hole_at(cx + offset, cy, cz, 4.2, size + 10, direction=(0, 0, 1))
            elif abs(adx) > 0.9:
                bh = hole_at(cx, cy, cz + offset, 4.2, size + 10, direction=(1, 0, 0))
            else:
                bh = hole_at(cx, cy + offset, cz, 4.2, size + 10, direction=(0, 0, 1))
            block -= bh

        return block
