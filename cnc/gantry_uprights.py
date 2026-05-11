"""Component 4: Gantry Uprights — two vertical columns with gussets and top plates."""

from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import bolt_circle, hole_at


class GantryUprights(CNCComponent):
    """Two vertical columns supporting the gantry bridge, with
    reinforcing gussets at the base and bolt-on top plates."""

    def build(self) -> Compound:
        c = self.config

        parts: list[Part] = []
        for ux in (c.rail_x_left, c.rail_x_right):
            parts.extend(self._build_upright(ux))
        return Compound(children=parts)

    def _build_upright(self, ux: float) -> list[Part]:
        c = self.config
        parts: list[Part] = []
        base_z = c.upright_base_z  # top of Y-rails = 175

        # --- Main column ---
        col = Pos(ux, c.mid_y, c.upright_mid_z) * Box(
            c.upright_x, c.upright_y, c.upright_z
        )
        parts.append(col)

        # --- Base gussets (Y-direction, front and back) ---
        gus_x = c.upright_x + c.gusset_size  # 80
        gus_y = c.gusset_thick  # 10
        gus_z = c.gusset_size  # 40
        gus_z_center = base_z + gus_z / 2  # 175 + 20 = 195
        g_y_offset = c.upright_y / 2 + c.gusset_size / 4  # 30 + 10 = 40
        for gy in (c.mid_y - g_y_offset, c.mid_y + g_y_offset):
            parts.append(Pos(ux, gy, gus_z_center) * Box(gus_x, gus_y, gus_z))

        # --- Base gussets (X-direction, left and right) ---
        gus_x2 = c.gusset_thick  # 10
        gus_y2 = c.upright_y + c.gusset_size  # 100
        g_x_offset = c.upright_x / 2 + c.gusset_size / 4  # 20 + 10 = 30
        for gx in (ux - g_x_offset, ux + g_x_offset):
            parts.append(Pos(gx, c.mid_y, gus_z_center) * Box(gus_x2, gus_y2, gus_z))

        # --- Top plate ---
        plate_x = c.upright_x - 14  # 26
        plate_y = c.upright_y + c.upright_plate_overhang  # 80
        plate_z = c.upright_plate_thick  # 12
        plate_z_center = base_z + c.upright_z + plate_z / 2  # 175 + 200 + 6 = 381
        top_plate = Pos(ux, c.mid_y, plate_z_center) * Box(plate_x, plate_y, plate_z)

        # Bolt holes in top plate (4 on 30mm circle)
        bolt_positions = bolt_circle(ux, c.mid_y, c.upright_bolt_circle, count=4)
        holes: list[Part] = []
        for bx, by in bolt_positions:
            holes.append(hole_at(bx, by, plate_z_center, c.bolt_hole_dia,
                                 plate_z + 5, direction=(0, 0, -1)))
        for h in holes:
            top_plate -= h

        parts.append(top_plate)

        return parts
