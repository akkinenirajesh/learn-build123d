"""CNC Machine — main entry point. Builds all 12 components, previews, exports."""

import os
from build123d import export_step, export_stl
from ocp_vscode import show

from cnc.config import CNCConfig
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


def build_cnc(config: CNCConfig | None = None):
    """Build all 12 CNC components and return them as a dict of name -> Compound."""
    if config is None:
        config = CNCConfig()

    components = {
        "BaseFrame": BaseFrame(config),
        "WorkBed": WorkBed(config),
        "YRails": YRails(config),
        "GantryUprights": GantryUprights(config),
        "GantryBridge": GantryBridge(config),
        "XRails": XRails(config),
        "ZAssembly": ZAssembly(config),
        "SpindleMount": SpindleMount(config),
        "MotorMounts": MotorMounts(config),
        "LeadScrews": LeadScrews(config),
        "DragChains": DragChains(config),
        "Safety": Safety(config),
    }

    results = {}
    for name, comp in components.items():
        print(f"Building {name}...")
        results[name] = comp.build()

    return results


def main():
    """Build the complete CNC machine, preview in viewer, and export."""
    config = CNCConfig()
    print(f"CNC Machine: {config.work_area_x}x{config.work_area_y}x{config.work_area_z}mm work area")
    print(f"  Base: {config.base_outer_x}x{config.base_outer_y}x{config.base_outer_z}mm")

    results = build_cnc(config)

    print("\nAll 12 components built. Starting viewer...")
    show(*results.values(), names=list(results.keys()))

    # Export
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    for name, shape in results.items():
        step_path = os.path.join(out_dir, f"{name}.step")
        stl_path = os.path.join(out_dir, f"{name}.stl")
        export_step(shape, step_path)
        export_stl(shape, stl_path)
        print(f"  Exported: {step_path}, {stl_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
