import pandas as pd
from fuplot import FuPlot, aes, RGBA
from pathlib import Path

data = pd.read_csv(Path("test_data") / "planets.csv")
data = data.groupby("method").sum().sort_values("orbital_period", ascending=False)


plot = FuPlot(data, aes("number", "orbital_period"))
plot.geom_col(fill=RGBA(0.5, 0.5, 1), spacing=0.01)
plot.render()
