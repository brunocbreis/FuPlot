from pathlib import Path
import pandas as pd
import pyperclip
from fuplot.style import COLORS
from fuplot import FuPlot


# MAIN ==================================================
def main():
    data = pd.read_csv(Path("test_data") / "IVV.csv")
    # clean dates
    data.Date = pd.to_datetime(data.Date).apply(lambda v: v.value)

    plot = FuPlot(data, width=0.8, height=0.5)
    plot.geom_line(x="Date", y="Adj Close", color=COLORS.red)

    pyperclip.copy(plot.render())


if __name__ == "__main__":
    main()
