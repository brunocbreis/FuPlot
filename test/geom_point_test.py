from pathlib import Path
import pandas as pd
from fuplot import FuPlot, RGBA, aes


def main() -> None:
    data = pd.read_csv(Path("test_data") / "pop_co2.csv")

    plot = FuPlot(data, width=0.5)
    plot.geom_point(
        mapping=aes(x="pop_urb_pct", y="co2_transport"),
        fill=RGBA(1, 0.2, 0.4),
        opacity=0.25,
    )

    plot.render()


def main2() -> None:
    data = pd.read_csv(Path("test_data") / "planets.csv")
    data = data.dropna()

    plot = FuPlot(data, width=0.6)
    plot.geom_point(
        mapping=aes("distance", "orbital_period", size="mass"),
        fill=RGBA(0.2, 1, 0.4),
        opacity=0.1,
    )
    plot.render()


if __name__ == "__main__":
    main2()
