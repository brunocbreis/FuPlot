from .fusionize import fusionize
from dataclasses import dataclass, field
from pysion.utils import RGBA
from pysion import Tool, Macro, Input


@dataclass
class GeomLine:
    x: list[int | float]
    y: list[int | float]
    thickness: float = 0.003
    color: RGBA = field(default_factory=RGBA)
    index: int = 1

    @property
    def name(self) -> str:
        """Same name of the tool that outputs the final geom image"""

        return f"GeomLine{self.index}"

    def render(self, width: float, height: float, resolution: tuple[int, int]) -> Tool:
        fu_x = fusionize(self.x, width)
        fu_y = fusionize(self.y, height)

        points = list(sorted(zip(fu_x, fu_y)))

        line = (
            Tool.mask("PlotLine", "Polyline", (0, -1))
            .add_inputs(BorderWidth=self.thickness)
            .add_inputs("Expression", Level="WriteLength > 0 and 1 or 0")
            .add_published_polyline(points)
        )

        background = Tool.bg("PlotColor", self.color, resolution).add_mask(line.name)

        geom_line = (
            Macro(self.name, [line, background], (self.index, -1))
            .add_color_input(background)
            .add_instance_input(line.inputs["BorderWidth"], Name="Thickness")
            .add_instance_input(Input(line.name, "WritePosition", 0))
            .add_instance_input(Input(line.name, "WriteLength", 1))
        )

        return geom_line
