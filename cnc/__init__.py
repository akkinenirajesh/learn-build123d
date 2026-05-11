"""build123d CNC — a parametric gantry-style CNC router.

Components are modeled as classes inheriting from CNCComponent.
CNCConfig holds all parameters and computed constraints.
"""

from cnc.config import CNCConfig
from cnc.component import CNCComponent

__all__ = ["CNCConfig", "CNCComponent"]
