# FuPlot

FuPlot is a ggplot2 (heavily) inspired framework for creating animatable data visualizations from tabular data for DaVinci Resolve Fusion.

## TODO

- wrap stuff into a group for cleaner node output
- customizable scale
- ability to better configure margin and dimensional properties
- geom_col for bar plots
- GUI for use within Fusion in a plugin-like interface
- turn into pip installable package
- make it work as a script in fusion rather than generating text
- figure out how it works in fusion when points are not published
- text for labs
- text for axes
- text for titles and stuff
- create canvas for graph so scale can make it go outside the displayed area (use a mask)
- test exporting some values as dynamically controllable in fusion for easier animation
  - add expressions to inputs that connect them to animatable sliders
  - or add modifiers to each input... don't know which is heavier on the cpu
