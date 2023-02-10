from pathlib import Path
import pandas as pd
from fuplot.style import RGBA
from fuplot import FuPlot, aes


# MAIN ==================================================
def main():
    data = pd.read_csv(Path("test_data") / "IVV.csv")

    # clean dates
    data.Date = pd.to_datetime(data.Date).apply(lambda v: v.value)

    plot = FuPlot(data, aes("Date"), width=0.6, height=0.5)
    plot.geom_line(mapping=aes(y="High"), color=RGBA(0.2, 1, 0.5))
    plot.geom_line(mapping=aes(y="Low"), color=RGBA(1, 0.2, 0.5))
    plot.geom_line(
        mapping=aes(y="Adj Close"), color=RGBA(0.35, 0.35, 1), thickness=0.002
    )

    plot.render()


if __name__ == "__main__":
    main()
