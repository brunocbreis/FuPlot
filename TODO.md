# TODO

## Features and Fixes

## General improvements

- [X] wrap stuff into a group for cleaner node output
- [ ] customizable scale
- [ ] ability to better configure margin and dimensional properties
- [ ] turn into pip installable package
- [ ] create canvas for graph so scale can make it go outside the displayed area (use a mask)
- [ ] test exporting some values as dynamically controllable in fusion for easier animation
  - [ ] add expressions to inputs that connect them to animatable sliders
  - [ ] or add modifiers to each input... don't know which is heavier on the cpu
- [ ] themes
- [ ] color palettes / scales

### text stuff

- [ ] text for labs
- [ ] text for axes
- [ ] text for titles and stuff

### geom_point

- [ ] use sNodes instead of masks (one sNode per shape, one sTransform per data point)
- [ ] different shapes as aes() options or style options

### geom_col

- [ ] fix spacing and scale
- [ ] figure out how it works in fusion when points are not published

## Maybe in the future

- [ ] make it work as a script in fusion rather than generating text
- [ ] GUI for use within Fusion in a plugin-like interface
