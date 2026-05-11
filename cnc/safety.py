"""Component 12: Safety — limit switches, hard stops, and E-stop button."""

from build123d import *

from cnc.component import CNCComponent


class Safety(CNCComponent):
    """Safety components: 6 limit switches, 6 hard stop bumpers, and E-stop."""

    def build(self) -> Compound:
        c = self.config
        parts: list[Part] = []

        # Limit switch positions: 2 on Y rails, 2 on X rails, 2 on Z plate
        switch_positions = [
            # Y-axis (at ends of Y rails)
            ("y", c.rail_x_left, c.mid_y - 230, c.y_rail_z),
            ("y", c.rail_x_left, c.mid_y + 230, c.y_rail_z),
            ("y", c.rail_x_right, c.mid_y - 230, c.y_rail_z),
            ("y", c.rail_x_right, c.mid_y + 230, c.y_rail_z),
            # X-axis (at ends of X rails)
            ("x", c.mid_x - 230, c.bridge_y_front, c.x_rail_upper_z),
            ("x", c.mid_x + 230, c.bridge_y_front, c.x_rail_upper_z),
        ]

        for orient, sx, sy, sz in switch_positions:
            parts.append(self._build_limit_switch(sx, sy, sz, orient))

        # Hard stop bumpers at same positions
        for orient, sx, sy, sz in switch_positions:
            parts.append(self._build_hard_stop(sx, sy, sz, orient))

        # E-stop button (on front of base frame)
        estop_x = c.mid_x
        estop_y = c.rail_x_left - 20  # front-left corner of base
        estop_z = c.base_outer_z - 30
        parts.append(self._build_estop(estop_x, estop_y, estop_z))

        return Compound(children=parts)

    def _build_limit_switch(self, sx: float, sy: float, sz: float,
                            orient: str) -> Part:
        """Microswitch with L-bracket and roller lever."""
        # L-bracket
        bracket = Pos(sx, sy, sz) * Box(20, 25, 3)
        # Switch body
        body = Pos(sx, sy, sz - 8) * Box(12, 20, 15)
        # Roller lever
        if orient == 'y':
            roller = Pos(sx, sy - 12, sz - 8) * Rot(0, 90, 0) * Cylinder(4, 8)
        else:
            roller = Pos(sx - 12, sy, sz - 8) * Rot(0, 90, 0) * Cylinder(4, 8)
        # M3 bolt holes
        for bh_x in (-5, 5):
            hole = Pos(sx + bh_x, sy, sz) * Cylinder(1.5, 8)
            bracket -= hole

        return Compound(children=[bracket, body, roller])

    def _build_hard_stop(self, sx: float, sy: float, sz: float,
                          orient: str) -> Part:
        """Rubber bumper hard stop."""
        bumper = Pos(sx, sy, sz) * Box(15, 15, 10)
        if orient == 'y':
            bumper = Pos(sx, sy + 15, sz) * Box(15, 10, 10)
        else:
            bumper = Pos(sx + 15, sy, sz) * Box(10, 15, 10)
        return bumper

    def _build_estop(self, ex: float, ey: float, ez: float) -> Part:
        """E-stop button: mounting plate + yellow collar + red mushroom head."""
        # Mounting plate
        plate = Pos(ex, ey, ez) * Box(35, 40, 4)
        # Yellow collar
        collar = Pos(ex, ey, ez + 2 + 8) * Cylinder(22, 16)
        # Red mushroom head
        head = Pos(ex, ey, ez + 2 + 16 + 5) * Cylinder(30, 10)

        return Compound(children=[plate, collar, head])
