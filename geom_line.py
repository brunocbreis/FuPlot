from jinja2 import Template
import pandas as pd
import pyperclip

from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import json


# LOAD CONFIG
with open("config.json", "r") as _:
    config = json.load(_, object_hook=lambda item: SimpleNamespace(**item))

# LOAD DATA
DATA_FOLDER = Path(config.data.folder)


# LOAD TEMPLATES
# Helper func
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


# Template rendering funcs
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


# Fusion rendering funcs
def fusionize(
    values: list[int | float],
    dimensions: float = 1,
) -> list[float]:
    min_value = min(values)
    max_value = max(values)
    range = max_value - min_value
    margin = (1 - dimensions) / 2

    return [margin + dimensions / range * (v - min_value) for v in values]


def line_plot(
    x: list[int | float],
    y: list[int | float],
    width: float = 1,
    height: float = 1,
    color: tuple[float, float, float] = (0, 0, 0),
) -> str:
    fusionized_x = fusionize(x, width)
    fusionized_y = fusionize(y, height)

    x_y_sorted = sorted(zip(fusionized_x, fusionized_y))

    x = [x for x, _ in x_y_sorted]
    y = [y for _, y in x_y_sorted]

    return GEOM_LINE_TEMPLATE.render(
        POINTS_ID=render_point_ids(len(x)),
        POINTS_DATA=render_point_data(x, y),
        RED=color[0],
        BLUE=color[1],
        GREEN=color[2],
    )


def main():
    # configs
    WIDTH = 0.8
    HEIGHT = 0.8

    COLOR = (0.5, 0.3, 1)

    # Data import and cleanup
    DATA_FILE = DATA_FOLDER / "IVV.csv"
    DATE_FORMAT = "%Y-%m-%d"

    X_COL_NAME = "Date"
    Y_COL_NAME = "Adj Close"

    data = pd.read_csv(DATA_FILE)

    x_raw = list(data[X_COL_NAME])
    y_raw = list(data[Y_COL_NAME])

    x_timestamp = [datetime.strptime(x, DATE_FORMAT).timestamp() for x in x_raw]

    # Render plot
    pyperclip.copy(line_plot(x_timestamp, y_raw, WIDTH, HEIGHT, COLOR))


if __name__ == "__main__":
    main()
