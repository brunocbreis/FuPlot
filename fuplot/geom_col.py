from .fusionize import fusionize
from dataclasses import dataclass, field
from pysion.utils import RGBA
from pysion import Tool, Macro, Output, Input
from typing import Any


@dataclass
class GeomCol:
    mapping: dict[str, str]

    @property
    def name(self) -> str:
        pass

    def render(self, width: float, height: float, resolution: tuple[int, int]) -> Tool:
        pass
