from dataclasses import dataclass
from types import SimpleNamespace

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
