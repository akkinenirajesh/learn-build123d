"""
Lesson 01 — Hello World: Your First build123d Part

Creates a simple box with a hole, renders it, and exports as STEP/STL.

Concepts:
  - Box primitive
  - Cylinder primitive (as cutting tool)
  - Boolean cut (-) operation
  - Export to STEP and STL
"""

from build123d import *
from ocp_vscode import show

profile = Rectangle(3 * CM, 4 * MM, align=Align.MIN)
profile += Rectangle(4 * MM, 3 * CM, align=Align.MIN)
angle_iron = extrude(profile, 10 * CM)


angle_iron = chamfer(
    angle_iron.edges().filter_by(lambda e: not e.is_interior), 0.5 * MM
)
# --- Preview (requires ocp-vscode VS Code extension) ------------------------
show(angle_iron)
