from .fusionize import fusionize, dim_to_scale
from pysion.utils import RGBA
from pysion import Tool, Macro, Input
from pandas import DataFrame


class GeomLine:
    def __init__(
        self,
        data: DataFrame,
        mapping: dict[str, str],
        thickness: float = None,
        color: RGBA = None,
        index: int = 1,
    ) -> None:
        self.data = data
        self.mapping = mapping

        # style
        self.thickness = thickness if thickness else 0.003
        self.color = color if color else RGBA()

        # index
        self.index = index

    @property
    def name(self) -> str:
        """Same name of the tool that outputs the final geom image"""

        return f"GeomLine{self.index}"

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

        points = list(sorted(zip(fu_x, fu_y)))

        line = (
            Tool.mask(f"PlotLine{self.index}", "Polyline", (0, -1))
            .add_inputs(BorderWidth=self.thickness)
            .add_inputs("Expression", Level="WriteLength > 0 and 1 or 0")
            .add_published_polyline(points)
        )

        background = Tool.bg(f"PlotColor{self.index}", self.color, resolution).add_mask(
            line.name
        )

        geom_line = (
            Macro(self.name, [line, background], (self.index, -1))
            .add_color_input(background)
            .add_instance_input(line.inputs["BorderWidth"], Name="Thickness")
            .add_instance_input(Input(line.name, "WritePosition", 0))
            .add_instance_input(Input(line.name, "WriteLength", 1))
        )

        return geom_line
