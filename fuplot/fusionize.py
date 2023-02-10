from pandas import Series


def fusionize(
    values: list[int | float] | Series,
    scale_data: tuple[int | float, int | float] = None,
    scale_plot: tuple[float, float] = (0, 1),
) -> list[float]:
    """Normalizes positional values for Fusion canvases"""
    if not scale_data:
        min_data = min(values)
        max_data = max(values)
    else:
        min_data = min(scale_data)
        max_data = max(scale_data)

    range_data = max_data - min_data

    min_plot = min(scale_plot)
    max_plot = max(scale_plot)
    range_plot = max_plot - min_plot

    return [range_plot * (v - min_data) / range_data + min_plot for v in values]


def dim_to_scale(dim: float, center: float = 0.5) -> tuple[float, float]:
    max_value = center + dim / 2
    min_value = max_value - dim
    return min_value, max_value


def scale_to_dim(scale: tuple[float, float]) -> float:
    return scale[1] - scale[0]
