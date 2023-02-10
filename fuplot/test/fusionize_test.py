import pandas as pd
from pathlib import Path
from fuplot.fusionize import fusionize

data = pd.read_csv(Path("test_data") / "IVV.csv")
data.Date = pd.to_datetime(data.Date).apply(lambda v: v.value)

print(fusionize(data["Adj Close"]))
