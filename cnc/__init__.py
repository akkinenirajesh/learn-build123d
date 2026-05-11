"""build123d CNC — a parametric gantry-style CNC router.

Components are modeled as classes inheriting from CNCComponent.
CNCConfig holds all parameters and computed constraints.

Usage:
    from cnc import CNCConfig, build_cnc
    from ocp_vscode import show

    config = CNCConfig()
    results = build_cnc(config)
    show(*results.values(), names=list(results.keys()))
"""

from cnc.config import CNCConfig
from cnc.component import CNCComponent
from cnc.main import build_cnc
from cnc.base_frame import BaseFrame
from cnc.work_bed import WorkBed
from cnc.y_rails import YRails
from cnc.gantry_uprights import GantryUprights
from cnc.gantry_bridge import GantryBridge
from cnc.x_rails import XRails
from cnc.z_assembly import ZAssembly
from cnc.spindle_mount import SpindleMount
from cnc.motor_mounts import MotorMounts
from cnc.lead_screws import LeadScrews
from cnc.drag_chains import DragChains
from cnc.safety import Safety

__all__ = [
    "CNCConfig",
    "CNCComponent",
    "build_cnc",
    "BaseFrame",
    "WorkBed",
    "YRails",
    "GantryUprights",
    "GantryBridge",
    "XRails",
    "ZAssembly",
    "SpindleMount",
    "MotorMounts",
    "LeadScrews",
    "DragChains",
    "Safety",
]
