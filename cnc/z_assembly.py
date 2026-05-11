"""Component 7: Z-Axis Assembly — back plate, Z rails, and Z carriage."""

from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import hole_at


class ZAssembly(CNCComponent):
    """Z-axis back plate, two vertical Z rails, and sliding Z carriage."""

    def build(self) -> Compound:
        c = self.config
        parts: list[Part] = []

        # --- Back plate ---
        plate = Pos(c.mid_x, c.z_plate_center_y, c.bridge_z) * Box(
            c.z_plate_x, c.z_plate_y, c.z_plate_z,
        )
        parts.append(plate)

        # --- Z rails (cylinders along Z, 230mm long) ---
        r_rad = c.z_rail_size / 2  # 7.5
        rail_length = c.z_plate_z - 20  # 230
        for rx in (c.mid_x - c.z_rail_space / 2, c.mid_x + c.z_rail_space / 2):
            rail = Pos(rx, c.z_rail_center_y, c.bridge_z) * Cylinder(r_rad, rail_length)
            parts.append(rail)

        # --- Z carriage ---
        carriage = self._build_carriage()
        parts.append(carriage)

        return Compound(children=parts)

    def _build_carriage(self) -> Part:
        c = self.config
        cx = c.mid_x
        cy = c.carriage_center_y  # 175
        cz = c.bridge_z  # 415

        body = Pos(cx, cy, cz) * Box(c.carriage_x, c.carriage_y, c.carriage_z)

        # Four M5 bolt holes through carriage (along Y)
        for hx, hz in [(cx - 20, cz - 15), (cx - 20, cz + 15),
                       (cx + 20, cz - 15), (cx + 20, cz + 15)]:
            h = hole_at(hx, cy, hz, c.bolt_hole_dia, 60, direction=(0, -1, 0))
            body -= h

        return body
