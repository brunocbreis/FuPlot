from pysion import RGBA
from types import SimpleNamespace


COLORS = SimpleNamespace(
    black=RGBA(),
    white=RGBA(1, 1, 1),
    transparent=RGBA(0, 0, 0, 0),
    red=RGBA(1),
    green=RGBA(0, 1),
    blue=RGBA(0, 0, 1),
)
