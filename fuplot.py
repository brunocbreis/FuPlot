from types import SimpleNamespace
from typing import Protocol
from dataclasses import dataclass, field
import pandas as pd
from pathlib import Path
from jinja2 import Template
import json
import pyperclip

# CONFIG ==================================================
with open("config.json", "r") as _:
    config = json.load(_, object_hook=lambda item: SimpleNamespace(**item))


# TEMPLATES ==================================================
def template_from_file(file: Path) -> Template:
    with open(file, "r") as _:
        template = Template(_.read())
    return template


TEMPS = config.templates
TEMPS_FOLDER = Path(TEMPS.folder)

GEOM_LINE_TEMPLATE_FILE = TEMPS_FOLDER / TEMPS.geom_line
POINT_ID_TEMPLATE_FILE = TEMPS_FOLDER / TEMPS.point_id
POINT_DATA_TEMPLATE_FILE = TEMPS_FOLDER / TEMPS.point_data


GEOM_LINE_TEMPLATE = template_from_file(GEOM_LINE_TEMPLATE_FILE)
POINT_ID_TEMPLATE = template_from_file(POINT_ID_TEMPLATE_FILE)
POINT_DATA_TEMPLATE = template_from_file(POINT_DATA_TEMPLATE_FILE)


# Template rendering
def render_point_ids(no_of_points: int) -> str:
    point_ids = [f"Point{i}" for i in range(no_of_points)]

    s = ""
    for p in point_ids:
        s += POINT_ID_TEMPLATE.render(POINT_NAME=p)

    return s


def render_point_data(x: list[int | float], y: list[int | float]) -> str:
    point_ids = [f"Point{i}" for i in range(len(x))]

    s = ""
    for x_data, y_data, point_id in zip(x, y, point_ids):
        s += POINT_DATA_TEMPLATE.render(POINT_NAME=point_id, X=x_data, Y=y_data)

    return s


# FUSIONIZING ==================================================
def fusionize(
    values: list[int | float],
    dimensions: float = 1,
) -> list[float]:
    min_value = min(values)
    max_value = max(values)
    range = max_value - min_value
    margin = (1 - dimensions) / 2

    return [margin + dimensions / range * (v - min_value) for v in values]


# COLOR ==================================================
@dataclass
class RGBA:
    """Defines an RGB + Alpha color using 0 to 1 floats. Defaults to fully opaque black."""

    red: float = 0
    green: float = 0
    blue: float = 0
    alpha: float = 1


COLORS = SimpleNamespace(
    black=RGBA(),
    white=RGBA(1, 1, 1),
    transparent=RGBA(0, 0, 0, 0),
    red=RGBA(1),
    green=RGBA(0, 1),
    blue=RGBA(0, 0, 1),
)

# GEOMS ========================================
class Geom(Protocol):
    def render(self) -> str:
        pass


@dataclass
class GeomLine:
    x: list[int | float]
    y: list[int | float]
    thickness: float = 0.003
    color: RGBA = field(default_factory=RGBA)

    def render(self, width: float, height: float) -> str:
        fusionized_x = fusionize(self.x, width)
        fusionized_y = fusionize(self.y, height)

        x_y_sorted = sorted(zip(fusionized_x, fusionized_y))

        x = [x for x, _ in x_y_sorted]
        y = [y for _, y in x_y_sorted]

        alpha = self.color.alpha

        return GEOM_LINE_TEMPLATE.render(
            POINTS_ID=render_point_ids(len(x)),
            POINTS_DATA=render_point_data(x, y),
            RED=self.color.red * alpha,
            GREEN=self.color.green * alpha,
            BLUE=self.color.blue * alpha,
            ALPHA=self.color.alpha,
        )


# FUPLOT ==================================================
class FuPlot:
    def __init__(
        self,
        data: pd.DataFrame,
        width: float = 0.75,
        height: float = 0.75,
    ) -> None:
        self.data = data.to_dict(orient="list")
        self.width = width
        self.height = height
        self.geoms: list[Geom] = []

    def _render_background(self) -> str:
        return ""

    def _render_axes(self) -> str:
        return ""

    def render(self) -> str:
        s = self._render_background()
        s += self._render_axes()

        for geom in self.geoms:
            s += geom.render(self.width, self.height)

        return s

    def geom_line(
        self, x: str, y: str, thickness: float = 0.003, color: RGBA = RGBA()
    ) -> None:
        self.geoms.append(GeomLine(self.data[x], self.data[y], thickness, color))


# MAIN ==================================================
def main():
    data = pd.read_csv(Path(config.data.folder) / "IVV.csv")
    # clean dates
    data.Date = pd.to_datetime(data.Date).apply(lambda v: v.value)

    plot = FuPlot(data, width=0.8, height=0.5)
    plot.geom_line(x="Date", y="Adj Close", color=COLORS.red)

    pyperclip.copy(plot.render())


if __name__ == "__main__":
    main()
