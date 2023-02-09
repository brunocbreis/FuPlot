from typing import Protocol
import pandas as pd
from .style import RGBA, COLORS
from .geom_line import GeomLine
from .geom_point import GeomPoint
from pysion import Tool, wrap_for_fusion, Macro, Output
from pysion.utils import fusion_point
from dataclasses import dataclass


# GEOMS ========================================
class Geom(Protocol):
    @property
    def name(self) -> str:
        pass

    def render(self, width: float, height: float, resolution: tuple[int, int]) -> Tool:
        pass


# FUPLOT ==================================================
@dataclass
class FuPlot:
    data: pd.DataFrame
    width: float = 0.75
    height: float = 0.75
    resolution: tuple[int, int] = (1920, 1080)

    def __post_init__(self) -> None:
        self.data = self.data.to_dict(orient="list")
        self.geoms: list[Geom] = []

        self._set_defaults()

    def _set_defaults(self):
        self.background_color = COLORS.white
        self.padding = 0.1
        self.axis_thickness = 0.001
        self.axis_color = RGBA(0.6, 0.6, 0.6, 1)

    def _render_background(self) -> Tool:
        alpha = self.background_color.alpha

        bg = Tool("Background", "PlotBG", (-1, 0)).add_inputs(
            UseFrameFormatSettings=0,
            Width=self.resolution[0],
            Height=self.resolution[1],
            TopLeftRed=self.background_color.red * alpha,
            TopLeftGreen=self.background_color.green * alpha,
            TopLeftBlue=self.background_color.blue * alpha,
            TopLeftAlpha=alpha,
        )

        return bg

    def _render_axes(self) -> Tool:
        ar = self.aspect_ratio
        pd = self.padding

        height = self.height + pd * ar
        width = self.width + pd

        x_pos = 0.5 - 0.5 * (self.width + pd * 0.75)
        y_pos = 0.5 - 0.5 * (self.height + pd * 0.75 * ar)

        x_axis = Tool("RectangleMask", "XAxis").add_inputs(
            Height=self.axis_thickness * ar,
            Width=width,
            Center=fusion_point(0.5, y_pos),
        )
        y_axis = (
            Tool("RectangleMask", "YAxis")
            .add_inputs(
                Height=height,
                Width=self.axis_thickness,
                Center=fusion_point(x_pos, 0.5),
            )
            .add_mask(x_axis.name)
        )
        fill = (
            Tool("Background", "AxisFill")
            .add_mask(y_axis.name)
            .add_inputs(
                UseFrameFormatSettings=0,
                Width=self.resolution[0],
                Height=self.resolution[1],
                TopLeftRed=self.axis_color.red * self.axis_color.alpha,
                TopLeftGreen=self.axis_color.green * self.axis_color.alpha,
                TopLeftBlue=self.axis_color.blue * self.axis_color.alpha,
                TopLeftAlpha=self.axis_color.alpha,
            )
        )

        macro = Macro("Axes", [x_axis, y_axis, fill], (0, -1)).add_instance_output(
            Output(fill.name)
        )

        return macro

    def _render_geoms(self) -> list[Tool]:
        g: list[Tool] = []
        for geom in self.geoms:
            g.append(geom.render(self.width, self.height, self.resolution))

        return g

    @property
    def aspect_ratio(self) -> float:
        return self.resolution[0] / self.resolution[1]

    # def render(self) -> str:
    #     t: list[Tool] = []

    #     t += self._render_geoms()

    #     t.append(self._render_axes())

    #     for tool in self._render_background():
    #         t.append(tool)

    #     return wrap_for_fusion(t)

    def render(self) -> str:
        t: list[Tool] = []
        merges: list[Tool] = []
        geoms = self._render_geoms()

        bg = self._render_background()
        axes = self._render_axes()

        t += [bg, axes]
        t += geoms

        for i, tool in enumerate(t):
            if i == 0:
                continue
            if i == 1:
                merges.append(Tool.merge(f"Merge{i}", t[i - 1], tool, (i - 1, 0)))
                continue
            merges.append(Tool.merge(f"Merge{i}", merges[i - 2], tool, (i - 1, 0)))

        return wrap_for_fusion(t + merges)

    def geom_line(
        self, x: str, y: str, thickness: float = 0.003, color: RGBA = COLORS.black
    ) -> None:
        idx = len(self.geoms) + 1
        self.geoms.append(GeomLine(self.data[x], self.data[y], thickness, color, idx))

        return self

    def geom_point(self, x: str, y: str, fill: RGBA = COLORS.black) -> None:
        idx = len(self.geoms) + 1
        self.geoms.append(GeomPoint(self.data[x], self.data[y], fill=fill, index=idx))

        return self

    def theme(self, background_color: RGBA = None, **kwargs):
        if background_color:
            self.background_color = background_color

        return self
