"""Component 9: Motor Mounts — three NEMA 23 motors at X, Y, Z positions."""

import math
from build123d import *

from cnc.component import CNCComponent
from cnc.helpers import bolt_circle, hole_at


class MotorMounts(CNCComponent):
    """Three NEMA 23 stepper motors with mounting plates, standoffs,
    shaft bores, and motor bodies at Y, X, and Z drive positions."""

    # NEMA 23 motor body fixed dimensions
    BODY_LENGTH = 76.0
    REAR_COVER_THICK = 5.0
    CABLE_EXIT_OD = 10.0
    CABLE_EXIT_LENGTH = 15.0
    SHAFT_DIA = 6.35
    SHAFT_LENGTH = 25.0

    def build(self) -> Compound:
        c = self.config
        parts: list[Part] = []

        # Y motor — at base rear, faces +Y
        y_motor = self._build_motor(c.mid_x, c.y_motor_y, c.upright_base_z,
                                     direction=(0, 1, 0))
        parts.extend(y_motor)

        # X motor — on bridge side, faces -Y
        x_motor = self._build_motor(c.x_motor_x,
                                     c.bridge_y_front + c.nema23_width / 2 + 30,
                                     c.bridge_z,
                                     direction=(0, -1, 0))
        parts.extend(x_motor)

        # Z motor — on Z plate top, faces -Y
        z_motor = self._build_motor(c.mid_x,
                                     c.bridge_y_front - c.z_plate_y + c.nema23_width / 2,
                                     c.bridge_z + c.z_plate_z / 2 - 20,
                                     direction=(0, -1, 0))
        parts.extend(z_motor)

        return Compound(children=parts)

    def _build_motor(self, cx: float, cy: float, cz: float,
                     direction: tuple[float, float, float]) -> list[Part]:
        c = self.config
        dx, dy, dz = direction
        parts: list[Part] = []

        # --- Mounting plate ---
        w = c.nema23_width  # 57
        pt = c.mount_plate_thick  # 8
        plate = Box(w, w, pt)

        # Orient plate so its thin dimension aligns with motor direction
        if abs(dy) > 0.9:
            # Motor along Y — plate in XZ plane
            plate = Pos(cx, cy, cz) * Box(w, pt, w)
            plate_center = (cx, cy, cz)
            plate_normal = (0, dy, 0)  # normalize
        elif abs(dx) > 0.9:
            plate = Pos(cx, cy, cz) * Box(pt, w, w)
            plate_center = (cx, cy, cz)
            plate_normal = (dx, 0, 0)
        else:
            plate = Pos(cx, cy, cz) * Box(w, w, pt)
            plate_center = (cx, cy, cz)
            plate_normal = (0, 0, dz)

        # Bolt holes on plate (NEMA 23 bolt circle: 47.14mm)
        bolt_positions = bolt_circle(cx, cy, c.nema23_bolt_circle, count=4)
        for bx, by in bolt_positions:
            h = hole_at(bx, by, cz, c.bolt_hole_dia, pt + 10, direction=plate_normal)
            plate -= h

        # Center shaft bore
        shaft_hole = hole_at(cx, cy, cz, c.nema23_shaft_bore, pt + 10,
                             direction=plate_normal)
        plate -= shaft_hole

        parts.append(plate)

        # --- Standoffs (behind plate) ---
        standoff = Cylinder(c.standoff_r, c.standoff_h)
        sd = 1 if abs(dy) > 0.9 or abs(dz) > 0.9 else -1
        for bx, by in bolt_positions:
            so_z = cz - sd * (pt / 2 + c.standoff_h / 2)
            parts.append(Pos(bx, by, so_z) * standoff)

        # --- Motor body ---
        body_forward = 1 if abs(dy) > 0.9 else -1
        if abs(dy) > 0.9:
            body_sz = body_forward * (pt / 2 + self.BODY_LENGTH / 2)
            body = Pos(cx, cy + body_sz, cz) * Box(w, self.BODY_LENGTH, w)
            parts.append(body)

            # Rear cover
            cover_sz = cy + body_forward * (pt / 2 + self.BODY_LENGTH + self.REAR_COVER_THICK / 2)
            parts.append(Pos(cx, cover_sz, cz) * Rot(0, 90, 0) * Cylinder(w / 2, self.REAR_COVER_THICK))

            # Cable exit
            cable_sz = cover_sz + body_forward * (self.REAR_COVER_THICK / 2 + self.CABLE_EXIT_LENGTH / 2)
            parts.append(Pos(cx, cable_sz, cz) * Rot(0, 90, 0) * Cylinder(self.CABLE_EXIT_OD / 2, self.CABLE_EXIT_LENGTH))

            # Motor shaft (extends forward from plate)
            shaft_off = -body_forward * (pt / 2 + self.SHAFT_LENGTH / 2)
            parts.append(Pos(cx, cy + shaft_off, cz) * Rot(0, 90, 0) * Cylinder(self.SHAFT_DIA / 2, self.SHAFT_LENGTH))
        else:
            # Z-aligned motor body (default)
            body_sz = body_forward * (pt / 2 + self.BODY_LENGTH / 2)
            body = Pos(cx, cy, cz + body_sz) * Box(w, w, self.BODY_LENGTH)
            parts.append(body)

            # Rear cover
            cover_sz = cz + body_forward * (pt / 2 + self.BODY_LENGTH + self.REAR_COVER_THICK / 2)
            parts.append(Pos(cx, cy, cover_sz) * Cylinder(w / 2, self.REAR_COVER_THICK))

            # Cable exit
            cable_sz = cover_sz + body_forward * (self.REAR_COVER_THICK / 2 + self.CABLE_EXIT_LENGTH / 2)
            parts.append(Pos(cx, cy, cable_sz) * Cylinder(self.CABLE_EXIT_OD / 2, self.CABLE_EXIT_LENGTH))

            # Motor shaft
            shaft_off = -body_forward * (pt / 2 + self.SHAFT_LENGTH / 2)
            parts.append(Pos(cx, cy, cz + shaft_off) * Cylinder(self.SHAFT_DIA / 2, self.SHAFT_LENGTH))

        return parts
