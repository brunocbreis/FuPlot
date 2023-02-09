from .fusionize import fusionize
from dataclasses import dataclass, field
from .style import RGBA
from pysion import Tool, Macro, Output, Input
from pysion.utils import fusion_point


@dataclass
class GeomPoint:
    x: list[int | float]
    y: list[int | float]
    size: float | list[int | float] = 0.005
    fill: RGBA = field(default_factory=RGBA)
    index: int = 1

    @property
    def name(self) -> str:
        """Same name of the tool that outputs the final geom image"""

        return f"GeomPoint{self.index}"

    def render(self, width: float, height: float) -> list[Tool]:
        fu_x = fusionize(self.x, width)
        fu_y = fusionize(self.y, height)

        if type(self.size) is float:
            fu_size = [self.size for _ in fu_x]
        else:
            fu_size = fusionize(
                self.size, 0.3
            )  # Problem cause min is going to be 0? idk

        points = list(sorted(zip(fu_x, fu_y)))

        for p, s in zip(points, fu_size):
            self._add_point(p[0], p[1], s)

        bg = (
            Tool("Background", "GeomPointFill", (0, len(self.points)))
            .add_inputs(
                UseFrameFormatSettings=1,
                TopLeftRed=self.fill.red,
                TopLeftGreen=self.fill.green,
                TopLeftBlue=self.fill.blue,
                TopLeftAlpha=1,
            )
            .add_mask(self.points[-1].name)
        )

        macro = Macro(self.name, self.points + [bg])

        return [macro]

    def __post_init__(self):
        self._points: list[Tool] = []

    @property
    def points(self) -> list[Tool]:
        return self._points

    def _add_point(self, x: float, y: float, size: float):
        i = len(self.points)
        ellipse = Tool("EllipseMask", f"Point{i+1}", (0, i)).add_inputs(
            Width=size, Height=size, Center=fusion_point(x, y), Level=self.fill.alpha
        )
        if len(self.points) > 0:
            ellipse.add_mask(self.points[i - 1].name)

        self._points.append(ellipse)
