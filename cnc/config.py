"""
CNCConfig — all machine parameters as a frozen dataclass.
Constraints are derived positions computed on access.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CNCConfig:
    """Immutable parameter set for the CNC machine. Use replace() to modify."""

    # -- Envelope -----------------------------------------------------------
    work_area_x: float = 500
    work_area_y: float = 400
    work_area_z: float = 120
    base_outer_z: float = 150

    @property
    def base_outer_x(self) -> float:
        return self.work_area_x + 100

    @property
    def base_outer_y(self) -> float:
        return self.work_area_y + 100

    # -- Wall Thickness -----------------------------------------------------
    base_wall_thick: float = 15
    rib_thick: float = 10
    gantry_wall_thick: float = 8
    rib_spacing: float = 120

    # -- Rails --------------------------------------------------------------
    rail_width: float = 20    # Y-rail cross-section width  (used as diameter)
    rail_height: float = 25   # Y-rail cross-section height (used as diameter)
    rail_inset_x: float = 30
    bolt_hole_dia: float = 5.2   # M5 clearance
    bolt_spacing_y: float = 80

    # -- Uprights -----------------------------------------------------------
    upright_x: float = 40
    upright_y: float = 60
    upright_z: float = 200

    # -- Gantry Bridge ------------------------------------------------------
    gantry_bridge_y: float = 60
    gantry_bridge_z: float = 80

    # -- Z-Axis -------------------------------------------------------------
    z_plate_x: float = 80
    z_plate_y: float = 15
    z_plate_z: float = 250
    z_rail_space: float = 50
    z_rail_size: float = 15

    # -- Spindle ------------------------------------------------------------
    spindle_od: float = 65
    clamp_od: float = 80
    clamp_height: float = 60
    clamp_slit: float = 3

    # -- Motor Mounts -------------------------------------------------------
    nema23_width: float = 57
    nema23_bolt_circle: float = 47.14
    nema23_shaft_bore: float = 12
    mount_plate_thick: float = 8

    # -- Lead Screws --------------------------------------------------------
    lead_screw_dia: float = 12
    nut_block_size: float = 25

    # -- T-Slots ------------------------------------------------------------
    tslot_upper_w: float = 20
    tslot_lower_w: float = 10
    tslot_depth: float = 10
    tslot_spacing: float = 100

    # -- Work Bed -----------------------------------------------------------
    table_thick: float = 20

    # -- Drag Chains --------------------------------------------------------
    chain_width: float = 30
    chain_height: float = 20

    # -- Fixed constants ----------------------------------------------------
    gusset_size: float = 40
    upright_plate_thick: float = 12
    upright_plate_overhang: float = 20
    upright_bolt_circle: float = 30
    bridge_end_boss_overhang: float = 10
    bridge_rib_spacing_x: float = 80
    table_overhang: float = 40
    standoff_h: float = 15
    standoff_r: float = 4

    # -- Computed: Constraints ----------------------------------------------

    @property
    def mid_x(self) -> float:
        return self.base_outer_x / 2

    @property
    def mid_y(self) -> float:
        return self.base_outer_y / 2

    @property
    def rail_x_left(self) -> float:
        return self.rail_inset_x

    @property
    def rail_x_right(self) -> float:
        return self.base_outer_x - self.rail_inset_x

    @property
    def upright_base_z(self) -> float:
        return self.base_outer_z + self.rail_height

    @property
    def upright_top_z(self) -> float:
        return self.upright_base_z + self.upright_z

    @property
    def upright_mid_z(self) -> float:
        return self.upright_base_z + self.upright_z / 2

    @property
    def bridge_z(self) -> float:
        return self.upright_base_z + self.upright_z + self.gantry_bridge_z / 2

    @property
    def bridge_top_z(self) -> float:
        return self.upright_base_z + self.upright_z + self.gantry_bridge_z

    @property
    def bridge_bottom_z(self) -> float:
        return self.upright_base_z + self.upright_z

    @property
    def bridge_y_front(self) -> float:
        return self.mid_y - self.gantry_bridge_y / 2

    @property
    def bridge_y_back(self) -> float:
        return self.mid_y + self.gantry_bridge_y / 2

    @property
    def bridge_span_x(self) -> float:
        return self.base_outer_x - 2 * self.rail_inset_x - self.upright_x

    @property
    def table_z_center(self) -> float:
        return self.base_outer_z + self.table_thick / 2

    @property
    def table_z_top(self) -> float:
        return self.base_outer_z + self.table_thick

    @property
    def z_plate_back_y(self) -> float:
        return self.bridge_y_front - self.z_plate_y

    @property
    def z_plate_center_y(self) -> float:
        return self.bridge_y_front - self.z_plate_y / 2

    @property
    def z_plate_front_y(self) -> float:
        return self.bridge_y_front

    @property
    def z_rail_center_y(self) -> float:
        return self.z_plate_center_y - self.z_plate_y / 2 - self.z_rail_size / 2

    @property
    def carriage_x(self) -> float:
        return self.z_plate_x - 10

    @property
    def carriage_y(self) -> float:
        return 30.0

    @property
    def carriage_z(self) -> float:
        return 60.0

    @property
    def carriage_center_y(self) -> float:
        return self.z_rail_center_y - self.carriage_y / 2 - self.z_rail_size / 2

    @property
    def carriage_front_y(self) -> float:
        return self.carriage_center_y - self.carriage_y / 2

    @property
    def spindle_clamp_y(self) -> float:
        return self.carriage_front_y - 40

    @property
    def spindle_clamp_z(self) -> float:
        return self.bridge_z - self.carriage_z / 2

    @property
    def y_motor_y(self) -> float:
        return self.base_outer_y - 20

    @property
    def x_motor_x(self) -> float:
        return self.rail_inset_x + self.upright_x + 30

    @property
    def z_motor_z(self) -> float:
        return self.bridge_z + self.z_plate_z / 2 - 20

    @property
    def z_motor_y(self) -> float:
        return self.bridge_y_front - self.z_plate_y + self.nema23_width / 2

    @property
    def y_screw_start_y(self) -> float:
        return 65.0

    @property
    def y_screw_end_y(self) -> float:
        return self.base_outer_y - 65

    @property
    def y_screw_z(self) -> float:
        return self.base_outer_z + self.table_thick + 18 + 15 + 7

    @property
    def x_screw_start_x(self) -> float:
        return self.rail_inset_x + self.upright_x / 2 + 30

    @property
    def x_screw_end_x(self) -> float:
        return self.base_outer_x - self.rail_inset_x - self.upright_x / 2 - 30

    @property
    def x_screw_z(self) -> float:
        return self.bridge_z

    @property
    def z_screw_y(self) -> float:
        return self.z_plate_front_y - 28

    @property
    def z_screw_bot_z(self) -> float:
        return self.bridge_z - self.z_plate_z / 2 + 20

    @property
    def z_screw_top_z(self) -> float:
        return self.bridge_z + self.z_plate_z / 2 - 20

    @property
    def y_tray_z(self) -> float:
        return self.base_outer_z + 10

    @property
    def y_tray_x(self) -> float:
        return self.base_outer_x - self.rail_inset_x + self.rail_width + 25

    @property
    def x_tray_z(self) -> float:
        return self.bridge_top_z + 5

    @property
    def x_tray_y(self) -> float:
        return self.mid_y - self.gantry_bridge_y / 2 - self.chain_width - 50

    @property
    def chain_tray_width(self) -> float:
        return self.chain_width + 6

    @property
    def chain_wall_h(self) -> float:
        return self.chain_height + 3

    @property
    def x_rail_upper_z(self) -> float:
        return self.bridge_z + self.gantry_bridge_z / 2 - 15

    @property
    def x_rail_lower_z(self) -> float:
        return self.bridge_z - self.gantry_bridge_z / 2 + 15

    @property
    def y_rail_z(self) -> float:
        return self.base_outer_z + self.rail_height / 2

    @property
    def y_bearing_size(self) -> float:
        return 40.0

    @property
    def x_bearing_size(self) -> float:
        return 40.0

    @property
    def bridge_mid_x(self) -> float:
        return self.mid_x

    @property
    def slot_inset(self) -> float:
        return 40.0

    @property
    def slot_upper_h(self) -> float:
        return self.tslot_depth * 0.4

    @property
    def slot_lower_h(self) -> float:
        return self.tslot_depth * 0.6

    @property
    def flange_y(self) -> float:
        return 20.0

    @property
    def flange_z(self) -> float:
        return 80.0

    @property
    def clamp_boss_dia(self) -> float:
        return 14.0

    @property
    def clamp_boss_depth(self) -> float:
        return 20.0

    @property
    def gusset_thick(self) -> float:
        return 10.0

    @property
    def spoil_board_thick(self) -> float:
        return 18.0

    @property
    def max_table_x(self) -> float:
        return self.base_outer_x - 2 * self.rail_inset_x - self.upright_x - 6
