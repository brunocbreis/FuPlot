from .fusionize import fusionize, dim_to_scale
from pysion import Tool, Macro
from pysion.utils import fusion_point, RGBA, fu_id
from pandas import DataFrame


class GeomPoint:
    def __init__(
        self,
        data: DataFrame,
        mapping: dict[str, str],
        size: float = None,
        fill: RGBA = None,
        opacity: float = None,
        index: int = 1,
    ) -> None:
        self.data = data
        self.mapping = mapping

        # style
        self.size = size if size else 0.0075
        self.fill = fill if fill else RGBA()
        self.opacity = opacity if opacity else 1

        # index
        self.index = index

        self._points: list[Tool] = []

        if self.fill.alpha < 1:
            print(
                "Warning: setting fill alpha to less than 1 will darken points' color."
                'Use "opacity" as an argument instead.'
            )

    @property
    def name(self) -> str:
        """Same name of the tool that outputs the final geom image"""

        return f"GeomPoint{self.index}"

    def render(
        self,
        width: float,
        height: float,
        mapping_scales: dict[str, tuple[int, int]],
        resolution: tuple[int, int],
    ) -> Tool:
        fu_x = fusionize(
            self.data[self.mapping["x"]],
            mapping_scales["x"],
            dim_to_scale(width),
        )
        fu_y = fusionize(
            self.data[self.mapping["y"]],
            mapping_scales["y"],
            dim_to_scale(height),
        )

        if "size" in self.mapping:
            fu_size = fusionize(
                self.data[self.mapping["size"]],
                mapping_scales["size"],
                dim_to_scale(width / 4, 0.25),
            )
        else:
            fu_size = [self.size for _ in fu_x]

        points = list(sorted(zip(fu_x, fu_y)))

        for p, s in zip(points, fu_size):
            self._add_point(p[0], p[1], s)

        bg = Tool.bg(
            "GeomPointFill",
            RGBA(self.fill.red, self.fill.green, self.fill.blue),
            resolution,
            (0, len(self.points)),
        ).add_mask(self.points[-1].name)

        macro = Macro(self.name, self.points + [bg], (self.index, -1))

        return macro

    @property
    def points(self) -> list[Tool]:
        return self._points

    def _add_point(self, x: float, y: float, size: float):
        i = len(self.points)
        ellipse = Tool.mask(f"Point{i+1}", "Ellipse", (0, i)).add_inputs(
            Width=size, Height=size, Center=fusion_point(x, y), Level=self.opacity
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
