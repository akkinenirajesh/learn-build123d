"""Component 2: Work Bed — table slab with T-slots, spoil board, fence, and clamps."""

from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import hole_at


class WorkBed(CNCComponent):
    """Work bed: table with T-slot grooves, MDF spoil board,
    alignment fence, and hold-down step clamps."""

    SPOIL_BOARD_THICK = 18.0

    def build(self) -> Compound:
        c = self.config
        table_x = min(c.work_area_x + 40, c.max_table_x)  # 494
        table_y = min(c.work_area_y + 40, c.base_outer_y)  # 440
        table_z = c.table_thick  # 20
        table_cx = c.mid_x
        table_cy = c.mid_y
        table_cz = c.table_z_center  # 160
        parts: list[Part] = []

        # --- Table slab ---
        table = Pos(table_cx, table_cy, table_cz) * Box(table_x, table_y, table_z)

        # --- T-slot grooves (subtracted from table) ---
        slot_start_x = table_cx - table_x / 2 + c.slot_inset  # ~93
        slot_end_x = table_cx + table_x / 2 - c.slot_inset  # ~507
        slot_y = table_y + 20  # extend past table edges
        slot_upper_h = c.slot_upper_h  # 4
        slot_lower_h = c.slot_lower_h  # 6
        slot_top_z = c.table_z_top  # 170

        x = slot_start_x
        while x <= slot_end_x + 0.01:
            # Upper (wide) slot
            upper = Pos(x, table_cy, slot_top_z - slot_upper_h / 2) * Box(
                c.tslot_upper_w, slot_y, slot_upper_h)
            # Lower (narrow) slot
            lower = Pos(x, table_cy, slot_top_z - slot_upper_h - slot_lower_h / 2) * Box(
                c.tslot_lower_w, slot_y, slot_lower_h)
            table -= upper
            table -= lower
            x += c.tslot_spacing

        parts.append(table)

        # --- Spoil board (MDF, 18mm) ---
        spoil_z = c.table_z_top + self.SPOIL_BOARD_THICK / 2  # 179
        spoil = Pos(table_cx, table_cy, spoil_z) * Box(table_x, table_y, self.SPOIL_BOARD_THICK)

        # M8 counterbored mounting holes (4 corners)
        cb_dia = 16.0
        cb_depth = 5.0
        m8_dia = 8.5
        inset = 50.0
        for sx in (table_cx - table_x / 2 + inset, table_cx + table_x / 2 - inset):
            for sy in (table_cy - table_y / 2 + inset, table_cy + table_y / 2 - inset):
                # Counterbore
                cb = Pos(sx, sy, spoil_z + self.SPOIL_BOARD_THICK / 2 - cb_depth / 2) * Cylinder(cb_dia / 2, cb_depth + 0.1)
                spoil -= cb
                # Through hole
                th = Pos(sx, sy, spoil_z) * Cylinder(m8_dia / 2, self.SPOIL_BOARD_THICK + 10)
                spoil -= th

        parts.append(spoil)

        # --- Alignment fence (along back edge) ---
        fence_y = table_cy + table_y / 2 - 7.5  # back edge - half fence Y
        fence_z = spoil_z + self.SPOIL_BOARD_THICK / 2 + 12.5  # on top of spoil board
        fence = Pos(table_cx, fence_y, fence_z) * Box(table_x, 15, 25)
        parts.append(fence)

        # --- Hold-down clamps (2 units) ---
        for cx in (c.mid_x - c.base_outer_x / 4, c.mid_x + c.base_outer_x / 4):
            clamp = self._build_step_clamp(cx, fence_y - 40, spoil_z + self.SPOIL_BOARD_THICK / 2)
            parts.append(clamp)

        return Compound(children=parts)

    def _build_step_clamp(self, cx: float, cy: float, sz: float) -> Part:
        """Build a single step clamp (heel/toe body + stud + nut)."""
        # Clamp body: heel (12mm tall at rear) + toe (6mm tall at front)
        body = Pos(cx, cy, sz + 9) * Box(80, 20, 18)  # simplified as uniform block
        # Through slot
        slot = Pos(cx, cy, sz + 9) * Box(30, 10, 20)
        body -= slot

        # Stud (M8 threaded rod)
        stud = Pos(cx, cy, sz - 10 + 30) * Cylinder(4, 60)

        # Hex nut
        nut = Pos(cx, cy, sz + 18 + 6) * Cylinder(6, 8)

        return Compound(children=[body, stud, nut])
