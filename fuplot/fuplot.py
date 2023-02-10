from typing import Protocol
import pandas as pd
from .style import COLORS
from .geom_line import GeomLine
from .geom_point import GeomPoint
from pysion import Tool, wrap_for_fusion, Macro
from pysion.utils import fusion_point, RGBA
from dataclasses import dataclass
import pyperclip


# GEOMS ========================================
class Geom(Protocol):
    @property
    def mapping(self) -> dict[str, str]:
        pass

    @property
    def name(self) -> str:
        pass

    def render(self, width: float, height: float, resolution: tuple[int, int]) -> Tool:
        pass


def aes(x: str = None, y: str = None, **kwargs: dict[str | str]) -> dict[str, str]:
    return dict(x=x, y=y, **kwargs)


# FUPLOT ==================================================
@dataclass
class FuPlot:
    data: pd.DataFrame
    mapping: dict[str, str] = None
    width: float = 0.75
    height: float = 0.75
    resolution: tuple[int, int] = (1920, 1080)

    def __post_init__(self) -> None:
        self.data = self.data.to_dict(orient="list")
        self.geoms: list[Geom] = []

        self._set_defaults()

    def _set_defaults(self):
        self.background_color = COLORS.white
        self.padding = 0.05
        self.axis_thickness = 0.001
        self.axis_color = RGBA(0.6, 0.6, 0.6, 1)

    def _render_background(self) -> Tool:
        return Tool.bg("PlotBG", self.background_color, self.resolution, (-1, 0))

    def _render_axes(self) -> Tool:
        ar = self.aspect_ratio
        pd = self.padding

        height = self.height + pd * ar
        width = self.width + pd

        x_pos = 0.5 - 0.5 * (self.width + pd)
        y_pos = 0.5 - 0.5 * (self.height + pd * ar)

        x_axis = Tool.mask("XAxis").add_inputs(
            Height=self.axis_thickness * ar,
            Width=width,
            Center=fusion_point(0.5, y_pos),
        )
        y_axis = (
            Tool.mask("YAxis")
            .add_inputs(
                Height=height,
                Width=self.axis_thickness,
                Center=fusion_point(x_pos, 0.5),
            )
            .add_mask(x_axis.name)
        )

        fill = Tool.bg("AxisFill", self.axis_color, self.resolution).add_mask(
            y_axis.name
        )

        return Macro("Axes", [x_axis, y_axis, fill], (0, -1))

    def _render_geoms(self) -> list[Tool]:
        g: list[Tool] = []
        for geom in self.geoms:
            g.append(geom.render(self.width, self.height, self.resolution))

        return g

    @property
    def aspect_ratio(self) -> float:
        return self.resolution[0] / self.resolution[1]

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

        s = wrap_for_fusion(t + merges)
        pyperclip.copy(s)

        print("Rendered node tree successfully copied to the clipboard.")

        return s

    def pass_to_geom(
        self, data: pd.DataFrame, mapping: dict[str, str]
    ) -> tuple[pd.DataFrame, dict[str, str]]:
        """Generalizes the passing of data and mapping to any geom."""

        if data is None:
            data = self.data
        if mapping is None:
            new_mapping = self.mapping
        else:
            new_mapping = {k: v for k, v in self.mapping.items()}
            for k, v in mapping.items():
                if v is None:
                    continue
                new_mapping[k] = v

        print(new_mapping)
        return data, new_mapping

    def geom_line(
        self,
        data: pd.DataFrame = None,
        mapping: dict[str, str] = None,
        thickness: float = None,
        color: RGBA = None,
    ):
        data, mapping = self.pass_to_geom(data, mapping)

        index = len(self.geoms) + 1
        self.geoms.append(GeomLine(data, mapping, thickness, color, index))

        return self

    def geom_point(self, x: str, y: str, size: str, fill: RGBA = COLORS.black) -> None:
        idx = len(self.geoms) + 1
        self.geoms.append(
            GeomPoint(
                self.data[x], self.data[y], size=self.data[size], fill=fill, index=idx
            )
        )

        return self

    def theme(self, background_color: RGBA = None, **kwargs):
        if background_color:
            self.background_color = background_color

        return self
