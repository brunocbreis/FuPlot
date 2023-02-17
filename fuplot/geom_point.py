from .fusionize import fusionize, dim_to_scale
from pysion import Tool, Macro, FuID, RGBA
from pandas import DataFrame


class GeomPoint:
    def __init__(
        self,
        data: DataFrame,
        mapping: dict[str, str],
        fill: RGBA = None,
        opacity: float = None,
        size: float = None,
        max_size: float = None,
        min_size: float = None,
        index: int = 1,
    ) -> None:
        self.data = data
        self.mapping = mapping

        # style
        self.size = size if size else 0.0075
        self.fill = fill if fill else RGBA()
        self.opacity = opacity if opacity else 1
        print("first opacity: ", self.opacity)

        # scaling
        self.max_size = max_size if max_size else 0.075
        self.min_size = min_size if min_size else 0.0075
        print(f"{self.min_size=}, {self.max_size=}")

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
                values=self.data[self.mapping["size"]],
                scale_data=mapping_scales["size"],
                scale_plot=(self.min_size, self.max_size),
            )
        else:
            fu_size = [self.size for _ in fu_x]

        points = list(sorted(zip(fu_x, fu_y)))

        for p, s in zip(points, fu_size):
            self._add_point(p[0], p[1], s)

        bg = Tool.background(
            "GeomPointFill",
            RGBA(self.fill.red, self.fill.green, self.fill.blue),
            resolution=resolution,
            position=(0, len(self.points)),
        ).add_mask(self.points[-1])

        macro = Macro(self.name, type="group", position=(self.index, -1)).add_tools(
            *(self.points + [bg])
        )

        return macro

    @property
    def points(self) -> list[Tool]:
        return self._points

    def _add_point(self, x: float, y: float, size: float):

        i = len(self.points)
        ellipse = Tool.mask(f"Point{i+1}", "Ellipse", (0, i)).add_inputs(
            Width=size, Height=size, Center=(x, y), Level=self.opacity
        )
        if len(self.points) > 0:
            ellipse.add_mask(self.points[i - 1]).add_inputs(PaintMode=FuID("Add"))

        self._points.append(ellipse)
