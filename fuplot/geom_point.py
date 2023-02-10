from .fusionize import fusionize
from dataclasses import dataclass, field
from pysion import Tool, Macro
from pysion.utils import fusion_point, RGBA, fu_id


@dataclass
class GeomPoint:
    x: list[int | float]
    y: list[int | float]
    size: float | list[int | float] = 0.0075
    fill: RGBA = field(default_factory=RGBA)
    index: int = 1

    @property
    def name(self) -> str:
        """Same name of the tool that outputs the final geom image"""

        return f"GeomPoint{self.index}"

    def render(self, width: float, height: float, resolution: tuple[int, int]) -> Tool:
        fu_x = fusionize(self.x, width)
        fu_y = fusionize(self.y, height)

        if type(self.size) is float:
            fu_size = [self.size for _ in fu_x]
        else:
            fu_size = self.fusionize_size(self.size, 0.1, 0.001, width)

        points = list(sorted(zip(fu_x, fu_y)))

        for p, s in zip(points, fu_size):
            self._add_point(p[0], p[1], s)

        bg = Tool.bg(
            "GeomPointFill", self.fill, resolution, (0, len(self.points))
        ).add_mask(self.points[-1].name)

        macro = Macro(self.name, self.points + [bg], (self.index, -1))

        return macro

    def __post_init__(self):
        self._points: list[Tool] = []

    @property
    def points(self) -> list[Tool]:
        return self._points

    def _add_point(self, x: float, y: float, size: float):
        i = len(self.points)
        ellipse = Tool.mask(f"Point{i+1}", "Ellipse", (0, i)).add_inputs(
            Width=size, Height=size, Center=fusion_point(x, y), Level=self.fill.alpha
        )
        if len(self.points) > 0:
            ellipse.add_mask(self.points[i - 1].name).add_inputs(PaintMode=fu_id("Add"))

        self._points.append(ellipse)

    @staticmethod
    def fusionize_size(
        values: list[int | float], max_size: float, min_size: float, scale: float
    ) -> list[float]:
        """Normalizes size values for Fusion, considering the plot's scale and a min and max sizes"""

        min_value = min(values)
        max_value = max(values)
        origin_range = max_value - min_value
        dest_range = max_size - min_size

        return [
            min_size + (scale / origin_range) * dest_range * (v - min_value)
            for v in values
        ]
