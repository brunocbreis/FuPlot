def fusionize(
    values: list[int | float],
    dimensions: float = 1,
) -> list[float]:
    """Normalizes positional values for Fusion canvases"""

    min_value = min(values)
    max_value = max(values)
    range = max_value - min_value
    margin = (1 - dimensions) / 2

    return [margin + dimensions / range * (v - min_value) for v in values]
