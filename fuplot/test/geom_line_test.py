from pathlib import Path
import pandas as pd
from fuplot.style import RGBA
from fuplot import FuPlot, aes


# MAIN ==================================================
def main():
    data = pd.read_csv(Path("test_data") / "IVV.csv")

    # clean dates
    data.Date = pd.to_datetime(data.Date).apply(lambda v: v.value)

    plot = FuPlot(data, aes("Date", "High"), width=0.8, height=0.5)
    plot.geom_line(color=RGBA(0.5, 0.2, 1))
    plot.geom_line(mapping=aes(y="Low"), color=RGBA(0.2, 0.5, 1))

    plot.render()


if __name__ == "__main__":
    main()
