from .fusionize import fusionize
from dataclasses import dataclass, field
from .style import RGBA
from pysion import Tool, Macro, Output, Input
from typing import Any


@dataclass
class GeomCol:
    x: list[Any]  # categorical
    y: list[int | float]
    fill: list[RGBA] = None

    @property
    def name(self) -> str:
        pass

    def render(self, width: float, height: float, resolution: tuple[int, int]) -> Tool:
        pass
