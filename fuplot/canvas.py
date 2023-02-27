from pysion import Tool, RGBA, Composition, Macro
from pysion.modifiers import Modifier
from pysion.values import ToolID
from typing import Literal
from types import SimpleNamespace


class NamesAndPositions(SimpleNamespace):
    canvas = "pcPlotCanvas", (0, 0)
    expand = "pcExpand", (1, 0)
    outline = "pcOutline", (2.5, 2)
    outline_color = "pcOutlineClr", (2.5, 3)

    remove_top_transform = "rtbTransform", (0, 0)
    remove_top_boolean = "rtbBool", (0, 1)
    remove_top_group = "pcRmTopBorder", (2.5, 5)

    grid_boolean = "pcGridBool", (2.5, -2)
    grid_h_line = "pcGridHline", (1.5, -5)
    grid_h = "pcGridH", (1.5, -4)
    grid_v_line = "pcGridVline", (3.5, -5)
    grid_v = "pcGridV", (3.5, -4)
    grid_merge = "pcGridMrg", (2.5, -4)

    tick_h = "pcTickH", (5, -5)
    tick_v = "pcTickV", (5, -4)
    tick_grid_h = "pcTickGridH", (6, -5)
    tick_grid_v = "pcTickGridV", (6, -4)

    merge = "pcMerge", (5, 0)
    render = "pcRender", (7, 0)


class Canvas:
    def __init__(
        self,
        resolution: tuple[int, int] = (1920, 1080),
        width: float = 0.5,
        height: float = 0.5,
        margin: float = 0.2,
        border_type: Literal["all", "axes", "none"] = "all",
        border_thickness: float = 0.1,
        border_color: RGBA = RGBA(),
        grid_h: int = 5,
        grid_v: int = 5,
        grid_thickness: float = 0.05,
        grid_color: RGBA = RGBA(0.8, 0.8, 0.8),
        ticks: bool = True,
        tick_thickness: float = 0.1,
        tick_length: float = 0.5,
        background_color: RGBA = RGBA(0.95, 0.95, 0.95),
    ) -> None:
        self.resolution = resolution
        self.width = width
        self._height = height

        self._margin = margin

        self.border_type = border_type
        self._border_thickness = border_thickness

        self.border_color = border_color

        self.grid_h = grid_h
        self.grid_v = grid_v

        self._grid_thickness = grid_thickness

        self.grid_color = grid_color

        self.ticks = ticks
        self._tick_thickness = tick_thickness
        self._tick_length = tick_length

        self.background_color = background_color

        self.comp = Composition()
        self._create_tools()

        return None

    @property
    def aspect_ratio(self):
        return self.resolution[0] / self.resolution[1]

    # Getters and setters! ==============================
    @property
    def height(self) -> float:
        return self._height / self.aspect_ratio

    @height.setter
    def height(self, value: float):
        self._height = value

    @property
    def margin(self) -> float:
        return self._margin / 10

    @margin.setter
    def margin(self, value: float):
        self._margin = value

    @property
    def border_thickness(self) -> float:
        return self._border_thickness / 100

    @border_thickness.setter
    def border_thickness(self, value):
        self._border_thickness = value

    @property
    def grid_thickness(self) -> float:
        return self._grid_thickness / 100

    @grid_thickness.setter
    def grid_thickness(self, value):
        self._grid_thickness = value

    @property
    def tick_thickness(self) -> float:
        return self._tick_thickness / 100

    @tick_thickness.setter
    def tick_thickness(self, value):
        self._tick_thickness = value

    @property
    def tick_length(self) -> float:
        return self._tick_length / 100

    @tick_length.setter
    def tick_length(self, value):
        self._tick_length = value

    # end getters and setters ==============================

    def render(self) -> Macro:
        self._set_tool_inputs()

        # return self.comp.copy()

        return self._create_macro()

    def _create_macro(self) -> Macro:
        macro = self.comp.to_macro("PlotCanvas", type="group")
        macro.position = (0, -1)
        macro.add_output(self.comp[NamesAndPositions.render[0]])
        ...
        # add macro inputs
        ...
        return macro

    def _create_tools(self) -> None:
        comp = self.comp

        canvas_output = self.__create_canvas_tools(comp)

        grid_output = self.__create_grid_tools(comp, canvas_output)

        outline_ouput = self.__create_outline_tools(comp, canvas_output)

        ticks_outputs = self.__create_ticks_tools(
            comp, comp[NamesAndPositions.grid_h[0]], comp[NamesAndPositions.grid_v[0]]
        )

        merge_output = self.__create_merge(
            comp,
            canvas_output,
            grid_output,
            outline_ouput,
            *ticks_outputs,
        )

        self.__create_render_tool(comp, merge_output)

    def __create_canvas_tools(self, comp: Composition) -> Tool:
        canvas = comp.add_tool(ToolID.s_rectangle, *NamesAndPositions.canvas)
        expand = comp.add_tool("sExpand", *NamesAndPositions.expand)
        comp.connect(canvas, expand)

        return expand

    def __create_outline_tools(self, comp: Composition, last_output: Tool) -> Tool:
        outline = comp.add_tool(ToolID.s_outline, *NamesAndPositions.outline)
        comp.connect(last_output, outline)

        outline_color = comp.add_tool(
            ToolID.s_boolean, *NamesAndPositions.outline_color
        )
        comp.connect(outline, outline_color, source_in="Input1")
        comp.connect(outline, outline_color, source_in="Input2")

        return outline_color

    def __create_grid_tools(self, comp: Composition, last_output: Tool) -> Tool:
        grid_h_line = comp.add_tool(ToolID.s_rectangle, *NamesAndPositions.grid_h_line)
        grid_h = comp.add_tool("sGrid", *NamesAndPositions.grid_h)
        comp.connect(grid_h_line, grid_h)

        grid_v_line = comp.add_tool(ToolID.s_rectangle, *NamesAndPositions.grid_v_line)
        grid_v = comp.add_tool("sGrid", *NamesAndPositions.grid_v)
        comp.connect(grid_v_line, grid_v)

        merge = comp.add_tool(ToolID.s_merge, *NamesAndPositions.grid_merge)
        comp.connect(grid_h, merge, source_in="Input1")
        comp.connect(grid_v, merge, source_in="Input2")

        boolean = comp.add_tool(ToolID.s_boolean, *NamesAndPositions.grid_boolean)
        comp.connect(last_output, boolean, source_in="Input1")
        comp.connect(merge, boolean, source_in="Input2")

        return boolean

    def __create_ticks_tools(
        self, comp: Composition, grid_h: Tool, grid_v: Tool
    ) -> tuple[Tool, Tool]:
        tick_h = comp.add_tool(ToolID.s_rectangle, *NamesAndPositions.tick_h)
        tick_v = comp.add_tool(ToolID.s_rectangle, *NamesAndPositions.tick_v)

        tick_h_grid = comp.add_instance(grid_h, *NamesAndPositions.tick_grid_h)
        tick_v_grid = comp.add_instance(grid_v, *NamesAndPositions.tick_grid_v)

        comp.connect(tick_h, tick_h_grid)
        comp.connect(tick_v, tick_v_grid)

        return tick_h_grid, tick_v_grid

    def __create_merge(self, comp: Composition, *inputs: Tool) -> Tool:
        merge = comp.add_tool(ToolID.s_merge, *NamesAndPositions.merge)

        for i, tool in enumerate(inputs, start=1):
            comp.connect(tool, merge, source_in=f"Input{i}")

        return merge

    def __create_render_tool(self, comp: Composition, last_output: Tool) -> None:
        canvas_render = comp.add_tool(ToolID.s_render, *NamesAndPositions.render)

        comp.connect(last_output, canvas_render)

    # INPUT SETTERS =================================
    def _set_tool_inputs(self, dynamic: bool = False):
        self.__set_canvas_inputs(dynamic)
        self.__set_outline_inputs(dynamic)
        self.__set_grid_inputs(dynamic)
        self.__set_ticks_inputs(dynamic)
        self.__set_render_inputs(dynamic)

    def __set_canvas_inputs(self, dynamic: bool):
        canvas: Tool = self.comp[NamesAndPositions.canvas[0]]
        expand: Tool = self.comp[NamesAndPositions.expand[0]]

        canvas.add_inputs(Width=self.width).add_color_input(self.background_color)

        calculation = Modifier("Calculation", "HeightCalc")
        calculation.add_inputs(
            Operator=3,
            SecondOperand=self.aspect_ratio,
            FirstOperand=self.height * self.aspect_ratio,
        ).add_user_control("Plot Height", page="Controls")

        self.comp._add_modifier(calculation)

        self.comp.connect(calculation, canvas, source_in="Height", source_out="Result")

        expand.add_inputs(Amount=self.margin, JoinStyle=2)

    def __set_outline_inputs(self, dynamic: bool):
        outline: Tool = self.comp[NamesAndPositions.outline[0]]
        color: Tool = self.comp[NamesAndPositions.outline_color[0]]

        outline.add_inputs(Thickness=self.border_thickness, JoinStyle=2)
        color.add_color_input(self.border_color)

    def __set_grid_inputs(self, dynamic: bool):
        grid_h_line: Tool = self.comp[NamesAndPositions.grid_h_line[0]]
        grid_h: Tool = self.comp[NamesAndPositions.grid_h[0]]
        grid_v_line: Tool = self.comp[NamesAndPositions.grid_v_line[0]]
        grid_v: Tool = self.comp[NamesAndPositions.grid_v[0]]

        boolean: Tool = self.comp[NamesAndPositions.grid_boolean[0]]

        thickness = self.comp.publish(grid_h_line, "Height", self.grid_thickness)
        # thickness.name = "GridlineThickness"
        self.comp.connect_to_published_value(thickness, grid_v_line, "Width")

        grid_h_line.add_inputs(Width=1)
        grid_v_line.add_inputs(Height=1)

        boolean.add_color_input(self.grid_color)

        grid_h.add_inputs(
            CellsY=max(1, self.grid_h),
            CellsX=1,
            YOffset=0 if self.grid_h <= 1 else (self.height) / (self.grid_h - 1),
        )
        grid_v.add_inputs(
            CellsX=max(1, self.grid_v),
            CellsY=1,
            XOffset=0 if self.grid_v <= 1 else self.width / (self.grid_v - 1),
        )

        if not self.grid_h:
            grid_h_line.pass_through = True
            grid_h.pass_through = True
        if not self.grid_v:
            grid_v_line.pass_through = True
            grid_v.pass_through = True

    def __set_ticks_inputs(self, dynamic: bool):
        tick_h: Tool = self.comp[NamesAndPositions.tick_h[0]]
        tick_v: Tool = self.comp[NamesAndPositions.tick_v[0]]

        tick_h.add_color_input(self.border_color).add_inputs(
            Width=self.tick_length,
            Height=self.border_thickness,
        ).add_inputs(
            **{
                '["Translate.X"]': -(self.width + self.margin + self.tick_length) / 2
                - self.border_thickness / self.aspect_ratio
            }
        )
        tick_v.add_color_input(self.border_color).add_inputs(
            Width=self.border_thickness,
            Height=self.tick_length,
        ).add_inputs(
            **{
                '["Translate.Y"]': -(self.height + self.margin + self.tick_length) / 2
                - self.border_thickness / self.aspect_ratio
            }
        )

        if not self.grid_h:
            tick_h.pass_through = True
        if not self.grid_v:
            tick_v.pass_through = True

    def __set_render_inputs(self, dynamic: bool):
        render: Tool = self.comp[NamesAndPositions.render[0]]

        render.add_inputs(Width=self.resolution[0], Height=self.resolution[1])
