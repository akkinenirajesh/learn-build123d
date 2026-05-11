"""Component 8: Spindle Mount — clamp ring, motor body, collet, tool, cooling."""

from build123d import *

from cnc.component import CNCComponent


class SpindleMount(CNCComponent):
    """Spindle assembly: clamp ring, motor body, ER20 collet, tool,
    water-cooling jacket, top cap, and cable exit."""

    # Fixed dimensions (from picocnc)
    BODY_HEIGHT = 180.0
    COLLET_OD = 40.0
    COLLET_HEIGHT = 25.0
    TOOL_DIA = 6.0
    TOOL_LENGTH = 30.0
    JACKET_GAP = 10.0  # extra OD on spindle for cooling jacket wall
    JACKET_HEIGHT = 120.0
    BARB_OD = 8.0
    BARB_LENGTH = 20.0
    TOP_CAP_THICK = 10.0
    CABLE_OD = 12.0
    CABLE_HEIGHT = 15.0

    def build(self) -> Compound:
        c = self.config
        cx = c.mid_x
        cy = c.spindle_clamp_y  # 120
        cz = c.spindle_clamp_z  # 385
        sp_od = c.spindle_od  # 65
        sp_rad = sp_od / 2
        clamp_h = c.clamp_height  # 60

        parts: list[Part] = []

        # --- Clamp ring (annular) ---
        clamp_outer = Pos(cx, cy, cz) * Cylinder(c.clamp_od / 2, clamp_h)
        clamp_inner = Pos(cx, cy, cz) * Cylinder(sp_rad, clamp_h + 20)
        clamp_ring = clamp_outer - clamp_inner

        # Clamp slit
        slit = Pos(cx, cy, cz) * Box(c.clamp_slit, 90, clamp_h + 10)
        clamp_ring -= slit

        # Bolt bosses (4 total, 2 per slit side, Y-axis cylinders)
        boss = Cylinder(c.clamp_boss_dia / 2, c.clamp_boss_depth)
        for sx in (-37, 37):  # X offset from center
            for sz in (-20, 20):  # Z offset from clamp center
                clamp_ring += Pos(cx + sx, cy, cz + sz) * Rot(0, 90, 0) * boss

        parts.append(clamp_ring)

        # --- Mounting flange (connects clamp to Z carriage) ---
        flange_y = cy + clamp_h / 2 + c.flange_y / 2  # 120 + 30 + 10 = 160
        flange = Pos(cx, flange_y, cz) * Box(c.z_plate_x, c.flange_y, c.flange_z)
        parts.append(flange)

        # --- Spindle motor body ---
        motor_bot_z = cz - self.BODY_HEIGHT / 2  # 385 - 90 = 295
        motor_top_z = cz + self.BODY_HEIGHT / 2  # 385 + 90 = 475
        motor = Pos(cx, cy, cz) * Cylinder(sp_rad, self.BODY_HEIGHT)
        parts.append(motor)

        # --- ER20 Collet nut ---
        collet_z = motor_bot_z - self.COLLET_HEIGHT / 2  # 295 - 12.5 = 282.5
        collet = Pos(cx, cy, collet_z) * Cylinder(self.COLLET_OD / 2, self.COLLET_HEIGHT)
        parts.append(collet)

        # --- Tool placeholder (6mm end mill) ---
        tool_z = collet_z - self.COLLET_HEIGHT / 2 - self.TOOL_LENGTH / 2  # 255
        tool = Pos(cx, cy, tool_z) * Cylinder(self.TOOL_DIA / 2, self.TOOL_LENGTH)
        parts.append(tool)

        # --- Cooling jacket (hollow cylinder around upper spindle) ---
        jacket_od = sp_od + self.JACKET_GAP  # 75
        jacket_z = motor_top_z - self.JACKET_HEIGHT / 2  # 475 - 60 = 415
        jacket_outer = Pos(cx, cy, jacket_z) * Cylinder(jacket_od / 2, self.JACKET_HEIGHT)
        jacket_inner = Pos(cx, cy, jacket_z) * Cylinder(sp_rad, self.JACKET_HEIGHT + 10)
        jacket = jacket_outer - jacket_inner
        parts.append(jacket)

        # --- Inlet/outlet barbs (X-axis cylinders through jacket wall) ---
        barb_r = self.BARB_OD / 2
        barb_in_z = jacket_z - self.JACKET_HEIGHT / 4  # 385
        barb_out_z = jacket_z + self.JACKET_HEIGHT / 4  # 445
        jacket_rad = jacket_od / 2  # 37.5
        barb_inlet = Pos(cx + jacket_rad, cy, barb_in_z) * Rot(0, 90, 0) * Cylinder(barb_r, self.BARB_LENGTH)
        barb_outlet = Pos(cx - jacket_rad, cy, barb_out_z) * Rot(0, 90, 0) * Cylinder(barb_r, self.BARB_LENGTH)
        parts.extend([barb_inlet, barb_outlet])

        # --- Top cap ---
        cap_z = motor_top_z + self.TOP_CAP_THICK / 2  # 480
        cap = Pos(cx, cy, cap_z) * Cylinder(sp_rad, self.TOP_CAP_THICK)
        parts.append(cap)

        # --- Cable exit ---
        cable_z = cap_z + self.TOP_CAP_THICK / 2 + self.CABLE_HEIGHT / 2  # 492.5
        cable = Pos(cx, cy, cable_z) * Cylinder(self.CABLE_OD / 2, self.CABLE_HEIGHT)
        parts.append(cable)

        return Compound(children=parts)
