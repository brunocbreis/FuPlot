from .fusionize import fusionize
from dataclasses import dataclass, field
from .style import RGBA
from pysion import Tool, Macro, Output, Input
from pysion.utils import fusion_string


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

        alpha = self.color.alpha

        line = (
            Tool("PolylineMask", "PlotLine", (0, -1))
            .add_inputs(BorderWidth=self.thickness)
            .add_inputs("Expression", Level="WriteLength > 0 and 1 or 0")
            .add_published_polyline(points)
        )

        background = (
            Tool("Background", "PlotColor")
            .add_inputs(
                TopLeftRed=self.color.red * alpha,
                TopLeftGreen=self.color.green * alpha,
                TopLeftBlue=self.color.blue * alpha,
                TopLeftAlpha=alpha,
                UseFrameFormatSettings=0,
                Width=resolution[0],
                Height=resolution[1],
            )
            .add_mask(line.name)
        )

        geom_line = (
            Macro(self.name, [line, background], (self.index, -1))
            .add_instance_output(Output(background.name))
            .add_instance_input(
                background.inputs["TopLeftRed"], ControlGroup=1, Name="Color"
            )
            .add_instance_input(background.inputs["TopLeftGreen"], ControlGroup=1)
            .add_instance_input(background.inputs["TopLeftBlue"], ControlGroup=1)
            .add_instance_input(background.inputs["TopLeftAlpha"], ControlGroup=1)
            .add_instance_input(line.inputs["BorderWidth"], Name="Thickness")
            .add_instance_input(Input(line.name, "WritePosition", 0))
            .add_instance_input(Input(line.name, "WriteLength", 1))
        )

        return geom_line
