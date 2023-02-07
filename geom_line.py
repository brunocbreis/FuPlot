import pandas as pd
from datetime import datetime
from jinja2 import Template
import pyperclip
from pathlib import Path

# Files
TEMPLATES_FOLDER = Path("templates")
DATA_FOLDER = Path("data")
GEOM_LINE_TEMPLATE_FILE = TEMPLATES_FOLDER / "geom_line_template.setting"


# Templates
POINT_ID_TEMPLATE = Template('\t\t\t\t\t\t\t{ PublishID = "{{ POINT_NAME }}" },\n ')
POINT_DATA_TEMPLATE = Template(
    "\t\t\t\t{{ POINT_NAME }} = Input { Value = { {{ X }}, {{ Y }} }, },\n "
)

with open(GEOM_LINE_TEMPLATE_FILE, "r") as t:
    LINEGRAPH_TEMPLATE = Template(t.read())


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


def line_graph(
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

    point_ids_string = render_point_ids(len(x))
    point_data_str = render_point_data(x, y)

    return LINEGRAPH_TEMPLATE.render(
        POINTS_ID=point_ids_string,
        POINTS_DATA=point_data_str,
        RED=color[0],
        BLUE=color[1],
        GREEN=color[2],
    )


def main():
    # Configs
    WIDTH = 0.8
    HEIGHT = 0.8

    COLOR = (0.2, 0.3, 1)

    # Data import and cleanup
    DATA_FILE = DATA_FOLDER / "IVV.csv"
    DATE_FORMAT = "%Y-%m-%d"

    X_COL_NAME = "Date"
    Y_COL_NAME = "Adj Close"

    data = pd.read_csv(DATA_FILE)

    x_raw = list(data[X_COL_NAME])
    y_raw = list(data[Y_COL_NAME])

    x_timestamp = [datetime.strptime(x, DATE_FORMAT).timestamp() for x in x_raw]

    # Render graph
    pyperclip.copy(line_graph(x_timestamp, y_raw, WIDTH, HEIGHT, COLOR))


if __name__ == "__main__":
    main()
