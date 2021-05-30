from h3 import h3
import dash

import numpy as np
import json
import polyfill
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import pandas as pd
import data
from PIL import Image


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#
# df = pd.read_csv('mapp.csv')

H3_res = 10

pyLogo = Image.open("Screenshot_1.png")

geoJson = {'type': 'Polygon',
 'coordinates': [data.data_a]}

geoJson_2 = {'type': 'Polygon',
 'coordinates': [data.data_b]}

geoJson_3 = {'type': 'Polygon',
 'coordinates': [data.data_c]}

hexagons = list(h3.polyfill(geoJson, H3_res))
polylines = []
for hex in hexagons:
    polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
    outlines = [loop for polygon in polygons for loop in polygon]
    polyline = [outline + [outline[0]] for outline in outlines][0]
    polylines.append(polyline)
fig = go.Figure()
for polyline in polylines:
            fig.add_trace(
                go.Scatter(
                    x=[i[0] for i in polyline],
                    y=[i[1] for i in polyline],
                    line=dict(color="red"),
                ),
            )

hexagons2 = list(h3.polyfill(geoJson_2, H3_res))
polylines2 = []
for hex in hexagons2:
    polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
    outlines = [loop for polygon in polygons for loop in polygon]
    polyline = [outline + [outline[0]] for outline in outlines][0]
    polylines2.append(polyline)
for polyline in polylines2:
            fig.add_trace(
                go.Scatter(
                    x=[i[0] for i in polyline],
                    y=[i[1] for i in polyline],
                    line=dict(color="red"),
                ),
            )

hexagons3 = list(h3.polyfill(geoJson_3, H3_res))
polylines3 = []
for hex in hexagons3:
    polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
    outlines = [loop for polygon in polygons for loop in polygon]
    polyline = [outline + [outline[0]] for outline in outlines][0]
    polylines3.append(polyline)
for polyline in polylines3:
            fig.add_trace(
                go.Scatter(
                    x=[i[0] for i in polyline],
                    y=[i[1] for i in polyline],
                    line=dict(color="red"),
                ),
            )

fig.add_layout_image(
        dict(
            source=pyLogo,
            xref="paper",
            yref="paper",
            x=0,
            y=1,
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.5,
            layer="below")
)

# Set templates
fig.update_layout(template="plotly_white")

app.layout = html.Div([
    dcc.Graph(
        figure=fig
    )
])

fig.show()

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')

