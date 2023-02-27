from .fusionize import fusionize, dim_to_scale
from pysion import Tool, Macro, RGBA
from pandas import DataFrame


class GeomLine:
    def __init__(
        self,
        data: DataFrame,
        mapping: dict[str, str],
        thickness: float | None = None,
        color: RGBA | None = None,
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
    ) -> Macro | Tool:
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
            .add_expression_input("Level", "WriteLength > 0 and 1 or 0")
            .add_published_polyline_with_expression(
                points, "(POINT - .5) * XScale + .5", "(POINT - .5) * YScale + .5"
            )
            .add_user_control(
                "X Scale", page="Controls", default=1, min_scale=0, max_scale=2
            )
            .add_user_control(
                "Y Scale", page="Controls", default=1, min_scale=0, max_scale=2
            )
        )

        background = Tool.background(
            f"PlotColor{self.index}", self.color, resolution=resolution
        ).add_mask(line)

        geom_line = (
            Macro(self.name, type="group", position=(self.index, -1))
            .add_tools(line, background)
            .add_color_input(background)
            .add_input(line, "BorderWidth", pretty_name="Thickness")
            .add_input(line, "WritePosition", "Position")
            .add_input(line, "WriteLength", "Length")
            .add_input(line, "XScale", "X Scale")
            .add_input(line, "YScale", "Y Scale")
        )

        return geom_line
