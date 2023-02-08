from .fusionize import fusionize
from dataclasses import dataclass, field
from .style import RGBA
from pysion import Tool, wrap_for_fusion


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
