from types import SimpleNamespace
from typing import Protocol
from dataclasses import dataclass


@dataclass
class RGBA:
    """Defines an RGB + Alpha color using 0 to 1 floats. Defaults to fully opaque black."""

    red: float = 0
    green: float = 0
    blue: float = 0
    alpha: float = 1


# Useful color constants
BLACK = RGBA()
WHITE = RGBA(1, 1, 1)
TRANSPARENT = RGBA(0, 0, 0, 0)
RED = RGBA(1)
GREEN = RGBA(0, 1)
BLUE = RGBA(0, 0, 1)


class Geom(Protocol):
    def render(self) -> str:
        pass


@dataclass
class GeomLine:
    x: list[int | float]
    y: list[int | float]
    thickness: float = 0.003
    color: RGBA = RGBA()


class FuPlot:
    def __init__(
        self, data: dict[str, list[int | float]], width: float = 1, height: float = 1
    ) -> None:
        self.data = SimpleNamespace(**data)
        self.width = width
        self.height = height
        self.geoms = []

    def _render_base(self) -> str:
        pass

    def _render_scale(self) -> str:
        pass

    def render(self) -> str:
        s = self._render_base()
        ...
        return s


def main():
    data = {"nums": [1, 2, 3], "letters": ["a", "b", "c"]}
    plot = FuPlot(data)

    print(plot.data.letters)


if __name__ == "__main__":
    main()
