from pathlib import Path
import pandas as pd
from fuplot import FuPlot, RGBA, aes


def main() -> None:
    # data = pd.read_csv(Path("test_data") / "pop_co2.csv")

    # plot = FuPlot(data, width=0.5)
    # plot.geom_point(x="pop_urb_pct", y="co2_transport", fill=RGBA(1, 0.2, 0.4, 0.5))

    # pyperclip.copy(plot.render())

    data = pd.read_csv(Path("test_data") / "planets.csv")
    data = data.dropna()

    plot = FuPlot(data, width=0.6)
    plot.geom_point(
        mapping=aes("distance", "orbital_period", size="mass"),
        fill=RGBA(0.2, 1, 0.4, 0.25, premultiply=False),
    )
    plot.render()


if __name__ == "__main__":
    main()
