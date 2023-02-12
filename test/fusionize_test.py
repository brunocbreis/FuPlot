import pandas as pd
from pathlib import Path
from fuplot.fusionize import fusionize, dim_to_scale, fusionize_categorical_to_position

data = pd.read_csv(Path("test_data") / "IVV.csv")
data.Date = pd.to_datetime(data.Date).apply(lambda v: v.value)

print("max:", max(data["Adj Close"]), "\nmin:", min(data["Adj Close"]))

print(fusionize(data["Adj Close"], scale_data=(200, 500), scale_plot=(0.2, 0.6)))

print(dim_to_scale(0.8 / 4, 0.25))

print(fusionize_categorical_to_position(10))
