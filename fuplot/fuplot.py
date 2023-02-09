from typing import Protocol
import pandas as pd
from .style import RGBA, COLORS
from .geom_line import GeomLine
from pysion import Tool, wrap_for_fusion


# GEOMS ========================================
class Geom(Protocol):
    @property
    def name(self) -> str:
        pass

    def render(self) -> list[Tool]:
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

        self._set_defaults()

    def _set_defaults(self):
        self.background_color = COLORS.white

    def _render_background(self) -> list[Tool]:
        alpha = self.background_color.alpha

        bg = Tool("Background", "PlotBG", (-1, 1)).add_inputs(
            UseFrameFormatSettings=1,
            TopLeftRed=self.background_color.red * alpha,
            TopLeftGreen=self.background_color.green * alpha,
            TopLeftBlue=self.background_color.blue * alpha,
            TopLeftAlpha=alpha,
        )
        mg = (
            Tool("Merge", "MrgPlot", (0, 1))
            .add_source_input("Background", bg.name, "Output")
            .add_source_input("Foreground", self.geoms[-1].name, "Output")
        )
        return [bg, mg]

    def _render_axes(self) -> str:
        return ""

    def render(self) -> str:
        t = self._render_background()
        # s += self._render_axes()

        for geom in self.geoms:
            for tool in geom.render(self.width, self.height):
                t.append(tool)

        return wrap_for_fusion(t)

    def geom_line(
        self, x: str, y: str, thickness: float = 0.003, color: RGBA = COLORS.black
    ) -> None:
        idx = len(self.geoms) + 1
        self.geoms.append(GeomLine(self.data[x], self.data[y], thickness, color, idx))

    def theme(self, background_color: RGBA = None, **kwargs):
        if background_color:
            self.background_color = background_color
