#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 14:17:51 2017

@author: mikewoodward
"""

from bokeh.io import show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

import json

from svgpathtools import svg2paths2

# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':

    # Read in the the SVG data file
    paths, attributes, svg_attributes = svg2paths2('USStates.svg')

    # Unused - but shows how to get the map size
    height = int(svg_attributes['height'])
    width = int(svg_attributes['width'])

    # State data
    x_state = []
    y_state = []
    state = []  # Holds the state abbreviations

    # Frame data - the frame that separates AK, HI from the US
    x_frame = []
    y_frame = []

    # Loop through every path in the SVG file
    for i in range(len(paths)):

        # This will either be the state abbreviation or the word 'frames'
        state_id = attributes[i]['id']

        # Process the state data
        if state_id != 'frames':

            # The SVG file has DC as DC1 - correct this
            if state_id == 'DC1':
                state.append('DC')
            else:
                state.append(state_id)

            x = []
            y = []

            # If there are discontinuous paths, we want to add a 'nan'
            # but we only want to add it between paths. This variable makes
            # sure we don't add a spurious 'nan' at the end
            first_pass = True

            # Some states (like HI) consist of several discontinuous paths
            # (e.g. islands) - so loop through every continous path
            for paths_state in paths[i].continuous_subpaths():

                # Add the 'nan' seperator if there's more than one path
                if first_pass:
                    first_pass = False
                else:
                    # The 'nan' seperates discontinuous paths in Bokeh
                    x.append(float('nan'))
                    y.append(float('nan'))

                for path in paths_state:

                    # The -ve flips the y axis round. In SVG, the top left is
                    # (0,0), but in Bokeh, (0,0) is bottom left
                    x.append(path.point(0).real)
                    y.append(-path.point(0).imag)

                    x.append(path.point(1).real)
                    y.append(-path.point(1).imag)

            # Now, add the coordinates - note x and y are lists.
            x_state.append(x)
            y_state.append(y)

        # This data is the 'frames' that seperates the AK and HI outlines
        # from the rest of the US
        else:

            for paths_frame in paths[i].continuous_subpaths():

                x = []
                y = []

                for path in paths_frame:

                    x.append(path.point(0).real)
                    y.append(-path.point(0).imag)

                    x.append(path.point(1).real)
                    y.append(-path.point(1).imag)

                x_frame.append(x)
                y_frame.append(y)

    # Set up the sources
    state_source = ColumnDataSource(data=dict(x=x_state,
                                              y=y_state,
                                              name=state))

    # No name for the frame
    frame_source = ColumnDataSource(data=dict(x=x_frame,
                                              y=y_frame))

    # We have the data, now let's write it to files
    # Write the states
    state_json = state_source.to_json(state_source)
    json.dump(state_json, open("state.json", 'w'))

    # Write the frame
    frame_json = frame_source.to_json(frame_source)
    json.dump(frame_json, open("frame.json", 'w'))

    # Set up the figure - we'll add the hover later
    tools = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(title="US States",
               tools=tools,
               x_axis_location=None,
               y_axis_location=None)

    p.grid.grid_line_color = None

    # The states
    patches = p.patches('x',
                        'y',
                        source=state_source,
                        fill_color='red',
                        fill_alpha=0.7,
                        line_color="white",
                        line_width=0.5)

    # The frame that separates AK, HI from the rest of the US
    p.multi_line('x',
                 'y',
                 source=frame_source,
                 line_color="gray",
                 line_width=1.0)

    # Now set up the hover tool - only for the states
    hover = HoverTool(point_policy="follow_mouse",
                      renderers=[patches],
                      tooltips=[("Name", "@name"), ])

    p.add_tools(hover)

    show(p)
