from .fusionize import fusionize, dim_to_scale, fusionize_categorical_to_position
from pysion import Tool, Macro, RGBA
from pandas import DataFrame


class GeomCol:
    def __init__(
        self,
        data: DataFrame | None = None,
        mapping: dict[str, str] | None = None,
        fill: RGBA | None = None,
        spacing: float | None = None,
        index: int = 1,
    ) -> None:
        """Accepted mappings: x (mandatory, will use sort order), y (mandatory), fill"""
        # data
        self.data = data
        self.mapping = mapping

        # styling
        self.fill = fill if fill else RGBA()
        self.spacing = spacing if spacing else 0.5

        # index
        self.index = index

        # private params
        self._cols: list[Tool] = []
        self.y_pivot: float = 0
        self.x_offset: float = 0

    @property
    def name(self) -> str:
        pass

    def render(
        self,
        width: float,
        height: float,
        mapping_scales: dict[str, tuple[int, int]],
        resolution: tuple[int, int],
    ) -> Macro:
        tools: list[Tool] = []

        base_col = self._render_base_col(width, height, resolution)
        tools.append(base_col)

        fu_x = fusionize_categorical_to_position(len(self.data), dim_to_scale(width))
        fu_y = fusionize(
            self.data[self.mapping["y"]],
            scale_data=mapping_scales["y"],
            scale_plot=dim_to_scale(height),
        )

        # temporary fill list
        fill = [self.fill for _ in fu_y]

        transforms = self._render_transforms(base_col, fu_x, fu_y, fill, width)
        transforms[-1].add_inputs(Width=resolution[0], Height=resolution[1])

        tools += transforms

        geom_col = Macro(
            f"GeomCol{self.index}", type="group", position=(self.index, -1)
        ).add_tools(*tools)

        return geom_col

    def _render_base_col(
        self, width: float, height: float, resolution: tuple[int, int]
    ) -> Tool:
        ar = resolution[0] / resolution[1]
        height /= ar
        self.y_pivot = -height / 2
        self.x_offset = -width / 2

        srect = (
            Tool("sRectangle", f"GeomColShape{self.index}")
            .add_inputs(
                Width=width,
                Height=height,
                Red=self.fill.red,
                Green=self.fill.green,
                Blue=self.fill.blue,
                Alpha=self.fill.alpha,
            )
            .add_inputs(**{'["Translate.X"]': self.x_offset})
        )

        return srect

    @staticmethod
    def _add_sbool() -> Tool:
        ...

    def _render_transforms(
        self,
        base_col: Tool,
        x_values: list[float],
        y_values: list[float],
        fill: list[RGBA],
        width: float,
    ) -> list[Tool]:
        col_width = (width / len(x_values)) * (1 - self.spacing)

        transforms: list[Tool] = []
        for i, (x, y, f) in enumerate(zip(x_values, y_values, fill)):
            transforms.append(
                Tool(
                    "sTransform",
                    f"GeomCol{self.index}Transform{i+1}",
                    (1, i - round(len(x_values) / 2)),
                )
                .add_inputs(
                    XOffset=x,
                    YSize=y,
                    XSize=col_width,
                    Red=f.red,
                    Blue=f.blue,
                    Green=f.green,
                    Alpha=f.alpha,
                    YPivot=self.y_pivot,
                    XPivot=self.x_offset,
                )
                .add_source_input("Input", base_col.name, base_col.output)
            )
        mrg = self._render_smerge(transforms)
        srender = self._render_srender(mrg)

        return transforms + [mrg, srender]

    def _render_smerge(self, transforms: list[Tool]) -> Tool:
        merge = Tool("sMerge", f"GeomColMerge{self.index}", (2, 0))
        for i, t in enumerate(transforms, start=1):
            merge.add_source_input(f"Input{i}", t.name, t.output)

        return merge

    def _render_srender(self, merge: Tool) -> Tool:
        return Tool("sRender", f"GeomColRender{self.index}", (3, 0)).add_source_input(
            "Input", merge.name, merge.output
        )
