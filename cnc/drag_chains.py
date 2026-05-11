"""Component 11: Drag Chains — Y and X cable management with trays and links."""

import math
from build123d import *

from cnc.component import CNCComponent


class DragChains(CNCComponent):
    """Y-axis and X-axis cable drag chains with U-channel trays,
    articulated chain links, and cover plates."""

    # Chain link dimensions
    LINK_PITCH = 17.0
    LINK_SIDE_PLATE_THICK = 2.0
    LINK_CROSSBAR_DIA = 4.0

    def build(self) -> Compound:
        c = self.config
        parts: list[Part] = []

        # Y-axis chain tray
        parts.extend(self._build_tray_assembly(
            tray_x=c.y_tray_x,
            tray_y_start=0,
            tray_y_end=c.base_outer_y,
            tray_z=c.y_tray_z,
            orientation='y',
        ))

        # X-axis chain tray
        parts.extend(self._build_tray_assembly(
            tray_x=c.mid_x - c.gantry_bridge_y / 2 - c.chain_width - 50,
            tray_y_start=c.bridge_span_x / 2 - 200,
            tray_y_end=c.bridge_span_x / 2 + 200,
            tray_z=c.x_tray_z,
            orientation='x',
        ))

        return Compound(children=parts)

    def _build_tray_assembly(
        self, tray_x: float, tray_y_start: float, tray_y_end: float,
        tray_z: float, orientation: str,
    ) -> list[Part]:
        c = self.config
        parts: list[Part] = []

        tray_width = c.chain_tray_width  # 36
        wall_h = c.chain_wall_h  # 23
        floor_thick = 3.0
        wall_thick = 3.0
        tray_length = abs(tray_y_end - tray_y_start)

        # U-channel tray: floor + two side walls
        if orientation == 'y':
            floor = Pos(tray_x, (tray_y_start + tray_y_end) / 2, tray_z + floor_thick / 2) * Box(
                tray_width, tray_length, floor_thick)
            inner_wall = Pos(tray_x - tray_width / 2 + wall_thick / 2,
                             (tray_y_start + tray_y_end) / 2,
                             tray_z + floor_thick + wall_h / 2) * Box(
                wall_thick, tray_length, wall_h)
            outer_wall = Pos(tray_x + tray_width / 2 - wall_thick / 2,
                             (tray_y_start + tray_y_end) / 2,
                             tray_z + floor_thick + wall_h / 2) * Box(
                wall_thick, tray_length, wall_h)
            parts.extend([floor, inner_wall, outer_wall])

            # Chain links along the tray
            num_links = max(3, int(tray_length / self.LINK_PITCH))
            for i in range(num_links):
                ly = tray_y_start + i * self.LINK_PITCH + self.LINK_PITCH / 2
                link = self._build_link(tray_x, ly, tray_z + floor_thick + c.chain_height / 2, 'y')
                parts.append(link)
        else:
            floor = Pos((tray_y_start + tray_y_end) / 2, tray_x, tray_z + floor_thick / 2) * Box(
                tray_length, tray_width, floor_thick)
            inner_wall = Pos((tray_y_start + tray_y_end) / 2,
                             tray_x - tray_width / 2 + wall_thick / 2,
                             tray_z + floor_thick + wall_h / 2) * Box(
                tray_length, wall_thick, wall_h)
            outer_wall = Pos((tray_y_start + tray_y_end) / 2,
                             tray_x + tray_width / 2 - wall_thick / 2,
                             tray_z + floor_thick + wall_h / 2) * Box(
                tray_length, wall_thick, wall_h)
            parts.extend([floor, inner_wall, outer_wall])

            # Chain links
            num_links = max(3, int(tray_length / self.LINK_PITCH))
            for i in range(num_links):
                lx = tray_y_start + i * self.LINK_PITCH + self.LINK_PITCH / 2
                link = self._build_link(lx, tray_x, tray_z + floor_thick + c.chain_height / 2, 'x')
                parts.append(link)

        # Cover plates (at start and end of tray)
        cover = Box(tray_width, 5, wall_h)
        if orientation == 'y':
            parts.append(Pos(tray_x, tray_y_start + 2.5, tray_z + floor_thick + wall_h / 2) * cover)
            parts.append(Pos(tray_x, tray_y_end - 2.5, tray_z + floor_thick + wall_h / 2) * cover)
        else:
            parts.append(Pos(tray_y_start + 2.5, tray_x, tray_z + floor_thick + wall_h / 2) * Box(5, tray_width, wall_h))
            parts.append(Pos(tray_y_end - 2.5, tray_x, tray_z + floor_thick + wall_h / 2) * Box(5, tray_width, wall_h))

        # Cable gland at tray end
        gland_od = 12.0
        gland_len = 15.0
        if orientation == 'y':
            gland = Pos(tray_x, tray_y_end, tray_z + floor_thick + wall_h / 2) * Rot(0, 90, 0) * Cylinder(gland_od / 2, gland_len)
        else:
            gland = Pos(tray_y_end, tray_x, tray_z + floor_thick + wall_h / 2) * Rot(0, 90, 0) * Cylinder(gland_od / 2, gland_len)
        parts.append(gland)

        # Cable bundle placeholder (3 parallel cylinders)
        cable_dia = 4.0
        for c_off in (-4, 0, 4):
            if orientation == 'y':
                cable = Pos(tray_x + c_off, (tray_y_start + tray_y_end) / 2,
                            tray_z + floor_thick + c.chain_height / 2) * Rot(0, 90, 0) * Cylinder(cable_dia / 2, tray_length)
            else:
                cable = Pos((tray_y_start + tray_y_end) / 2, tray_x + c_off,
                            tray_z + floor_thick + c.chain_height / 2) * Rot(0, 90, 0) * Cylinder(cable_dia / 2, tray_length)
            parts.append(cable)

        return parts

    def _build_link(self, cx: float, cy: float, cz: float, orientation: str) -> Part:
        """Build a single chain link with side plates and crossbar."""
        c = self.config
        w = c.chain_width  # 30
        h = c.chain_height  # 20

        if orientation == 'y':
            # Side plates (XZ plane)
            link = Pos(cx, cy, cz) * Box(w, self.LINK_PITCH, h)
        else:
            link = Pos(cx, cy, cz) * Box(self.LINK_PITCH, w, h)

        return link
