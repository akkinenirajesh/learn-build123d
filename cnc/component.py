"""CNCComponent — abstract base class for all CNC machine components."""

from abc import ABC, abstractmethod
import os

from build123d import Compound, export_step, export_stl

from cnc.config import CNCConfig


class CNCComponent(ABC):
    """Base class for a parametric CNC machine component."""

    def __init__(self, config: CNCConfig | None = None):
        self.config = config or CNCConfig()

    @abstractmethod
    def build(self) -> Compound:
        """Return the full geometry for this component."""
        ...

    def export(self, dir_path: str = "output") -> str:
        """Export component as STEP and STL to dir_path. Returns base filename."""
        name = self.__class__.__name__
        os.makedirs(dir_path, exist_ok=True)
        shape = self.build()
        step_path = os.path.join(dir_path, f"{name}.step")
        stl_path = os.path.join(dir_path, f"{name}.stl")
        export_step(shape, step_path)
        export_stl(shape, stl_path)
        return name
