# SV-Coords
Converts an SVG file to coordinates, suitable for using with Bokeh patches.

In Bokeh, I wanted a choropleth map of the US states, but with Alaska and Hawaii repositioned in the way you see on most US maps. To render the states, I wanted to use the patches renderer in Bokeh. I also wanted a border around Alaska and Hawaii to indicate they've been geographically repositioned.

The problem was, there was nothing in Bokeh 'out of the box'. So I needed to create this project.

To start with, I downloaded the WikiMedia SVG map of the US (). I now needed to convert the SVG map to a set of coordinates suitable for use with Bokeh, which is this project.


