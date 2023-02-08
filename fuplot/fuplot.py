from typing import Protocol
import pandas as pd
from pathlib import Path
import pyperclip
from .style import RGBA, COLORS
from .geom_line import GeomLine


# GEOMS ========================================
class Geom(Protocol):
    def render(self) -> str:
        pass


# FUPLOT ==================================================
class FuPlot:
    def __init__(
        self,
        data: pd.DataFrame,
        width: float = 0.75,
        height: float = 0.75,
    ) -> None:
        self.data = data.to_dict(orient="list")
        self.width = width
        self.height = height
        self.geoms: list[Geom] = []

    def _render_background(self) -> str:
        return ""

    def _render_axes(self) -> str:
        return ""

    def render(self) -> str:
        s = self._render_background()
        s += self._render_axes()

        for geom in self.geoms:
            s += geom.render(self.width, self.height)

        return s

    def geom_line(
        self, x: str, y: str, thickness: float = 0.003, color: RGBA = RGBA()
    ) -> None:
        self.geoms.append(GeomLine(self.data[x], self.data[y], thickness, color))
