# SVG-Coords
Converts an SVG file to coordinates, suitable for using with Bokeh patches.

In Bokeh, I wanted a choropleth map of the US states, but with Alaska and Hawaii repositioned in the way you see on most US maps. To render the states, I wanted to use the patches renderer in Bokeh. I also wanted a border (or frame) around Alaska and Hawaii to indicate they've been geographically repositioned. The problem was, there was nothing in Bokeh 'out of the box'. So I needed to create this project.

To start with, I downloaded the WikiMedia SVG map of the US (https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg). I now needed to convert the SVG map to a set of coordinates suitable for use with Bokeh, which is this project.

The Python script loads the SVG file into XXXX, and parses it. The parsing is state by state and renders each state as a list of lines. Once the states (and the AK/HI frame) have been rendered, we write the data to file and plot it to Bokeh.
