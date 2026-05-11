"""
Lesson 02 — Filleting All Edges

Creates an angle iron profile, extrudes it, then applies a fillet
to every edge on the part.

Concepts:
  - Sketching with Rectangle + boolean union
  - Extrude (boss extrude)
  - edges().filter_by() to select edges
  - fillet() to round edges
"""

from build123d import *
from ocp_vscode import show

# --- Sketch & extrude -------------------------------------------------------
profile = Rectangle(3 * CM, 4 * MM, align=Align.MIN)
profile += Rectangle(4 * MM, 3 * CM, align=Align.MIN)
angle_iron = extrude(profile, 10 * CM)

# --- Fillet every edge ------------------------------------------------------
angle_iron = fillet(angle_iron.edges(), 1 * MM)

# --- Preview -----------------------------------------------------------------
show(angle_iron)
