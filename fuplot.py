from types import SimpleNamespace
from typing import Protocol
from dataclasses import dataclass, field
import pandas as pd
from pathlib import Path
import pyperclip
from pysion import Tool, wrap_for_fusion


# FUSIONIZING ==================================================
def fusionize(
    values: list[int | float],
    dimensions: float = 1,
) -> list[float]:
    """Normalizes positional values for Fusion canvases"""

    min_value = min(values)
    max_value = max(values)
    range = max_value - min_value
    margin = (1 - dimensions) / 2

    return [margin + dimensions / range * (v - min_value) for v in values]


# COLOR ==================================================
@dataclass
class RGBA:
    """Defines an RGB + Alpha color using 0 to 1 floats. Defaults to fully opaque black."""

    red: float = 0
    green: float = 0
    blue: float = 0
    alpha: float = 1


COLORS = SimpleNamespace(
    black=RGBA(),
    white=RGBA(1, 1, 1),
    transparent=RGBA(0, 0, 0, 0),
    red=RGBA(1),
    green=RGBA(0, 1),
    blue=RGBA(0, 0, 1),
)

# GEOMS ========================================
class Geom(Protocol):
    def render(self) -> str:
        pass


@dataclass
class GeomLine:
    x: list[int | float]
    y: list[int | float]
    thickness: float = 0.003
    color: RGBA = field(default_factory=RGBA)

    def render(self, width: float, height: float) -> str:
        fu_x = fusionize(self.x, width)
        fu_y = fusionize(self.y, height)

        points = list(sorted(zip(fu_x, fu_y)))

        alpha = self.color.alpha

        line = (
            Tool("PolylineMask", "Plot", (0, -1))
            .add_inputs(BorderWidth=self.thickness)
            .add_published_polyline(points)
        )

        background = (
            Tool("Background", "PlotColor")
            .add_inputs(
                TopLeftRed=self.color.red * alpha,
                TopLeftGreen=self.color.green * alpha,
                TopLeftBlue=self.color.blue * alpha,
                TopLeftAlpha=alpha,
                UseFrameFormatSettings=1,
            )
            .add_mask(line.name)
        )

        return wrap_for_fusion([background, line])


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


# MAIN ==================================================
def main():
    data = pd.read_csv(Path("test_data") / "IVV.csv")
    # clean dates
    data.Date = pd.to_datetime(data.Date).apply(lambda v: v.value)

    plot = FuPlot(data, width=0.8, height=0.5)
    plot.geom_line(x="Date", y="Adj Close", color=COLORS.red)

    pyperclip.copy(plot.render())


if __name__ == "__main__":
    main()
