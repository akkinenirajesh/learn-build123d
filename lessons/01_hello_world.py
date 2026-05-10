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

# --- Part design -----------------------------------------------------------
# Create a 50x30x10 mm box
body = Box(50, 30, 10)
# Align: center the hole on the top face of the box
body = Pos(Z=5) * body

# Create a 6mm diameter cylinder to use as a cutting tool
hole = Cylinder(radius=3, height=10)

# Drill 4 holes through the box (one near each corner)
for x in (-18, 18):
    for y in (-10, 10):
        body -= Pos(X=x, Y=y, Z=5) * hole

# --- Export -----------------------------------------------------------------
import os
os.makedirs("output", exist_ok=True)

export_step(body, "output/01_hello_world.step")
export_stl(body, "output/01_hello_world.stl")

print("Exported: output/01_hello_world.step, output/01_hello_world.stl")

# --- Preview (requires ocp-vscode VS Code extension) ------------------------
show(body)
