# !["FuPlot"](https://github.com/brunocbreis/FuPlot/blob/main/images/fuplot-logo.png)

FuPlot is a Python framework for creating animatable data visualizations from tabular data for DaVinci Resolve Fusion.
It has been __heavily__ inspired by [ggplot2](https://ggplot2.tidyverse.org) and The Grammar of Graphics. The idea is
to have a syntax so familiar to R based data scientists, that turning their existing code into a ready-for-animation
motion design project in Blackmagic Fusion should be a breeze.

## Why Fusion?

Fusion is a node based compositing / VFX software that is distributed inside of Blackmagic DaVinci Resolve. Aside from
being my motion graphics creation platform of choice, it has one huge advantage: its comps are entirely text based,
which means they can easily be generated programmatically and shared with collaborators instantaneously. Plus, DaVinci Resolve
has a free version that offers basically all of Fusion's functionality, which means it's an accessible software
for those who are not pros in animation or VFX but wish to wet their feet a little bit.

## How it works

FuPlot relies on [pandas](https://pandas.pydata.org) to process tabular data, and expects
[tidily structured](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html) data sets.

From there, you map columns to aesthetics in a very similar way you would in ggplot:

```python
from pathlib import Path
import pandas as pd
from fuplot import FuPlot, aes, RGBA


# First, we import our data. This is a month of daily prices for the IVV ETF.
data = pd.read_csv(Path("test_data") / "IVV.csv")

# FuPlot can't deal with dates yet, so we convert dates to integers:
data.Date = pd.to_datetime(data.Date).apply(lambda v: v.value)

# Then we initialize the plot by feeding it the data, some aesthetics and settings.
plot = FuPlot(data, aes(x="Date"), width=0.6, height=0.5)

# We add our geom and some extra aesthetics, plus some styling as well.
plot.geom_line(
    mapping=aes(y="Adj Close"),
    color=RGBA(0.35, 0.35, 1),
    thickness=0.002
)

# Then we render! The result is copied to the clipboard, and pasteable into Fusion.
plot.render()

```

The code above produces the following result in Fusion:

!["A line plot for IVV prices"](https://github.com/brunocbreis/FuPlot/blob/main/images/geom_line_screenshot.png)

## How to install

You can install FuPlot by running `pip install git+https://github.com/brunocbreis/FuPlot/` in your Terminal.

## Roadmap

As of right now, FuPlot is in a very early pre-release state. Some simple results can be achieved and it is
already possible to have it help kickstart some animated data viz in Fusion. For the future, I intend to
add more and more customization options, and to streamline the "animatable" part of the plots. Fusion
has a bunch of features that make animating complex node structure possible, and my goal is for FuPlot to
make use of those.

One of the advantages of working in compositing software is you have the freedom to
do whatever you want once you have your design set up in an optimal way – FuPlot will try and find the
balance between getting you to amazing plots out of the box (by box I mean VSCode or whatever), and
giving you a smartly structured, heavily customizable starting point to build up beautiful visualizations for video.
