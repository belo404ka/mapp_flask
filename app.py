from flask import Flask
import dash
import json
import h3
from flask import request
import json
import requests
import plotly.express as px
import polyfill
from geojson import Polygon
from pandas.io.json import json_normalize
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import pandas as pd
import numpy


server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(server=server, external_stylesheets=external_stylesheets)

H3_res = 10
lat = numpy.uint32(54.748079)
lon = numpy.uint32(83.104486)
z = numpy.uint32(12.79)
# df = pd.read_csv("coordinates.csv",
#                    dtype={"fips": str})


maps = f'https://tile0.maps.2gis.com/tiles?x={lat}&y={lon}&z={z}'

def get_maps():
    r_json = requests.get(maps).json()
    df = json_normalize(r_json)
    return df


def get_coordinates():
    with open("data.json", "r") as f:
        return json.load(f)


def get_polylines():
    raw_data = get_coordinates()
    hexagons = []
    for rd in raw_data:
        geoJson = dict(type="Polygon", coordinates=[rd])
        hexagons.extend(h3.polyfill(geoJson, 10))
    polylines = []
    for hex in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        polylines.append(polyline)
    return Polygon(polylines)



def get_figure():
    fig = go.Choroplethmapbox(get_maps(), geojson=get_polylines(), locations='fips', center={"lat": lat, "lon": lon}
                               )
    # Set templates

    app.layout = html.Div([
        dcc.Graph(
            figure=fig
        )
    ])

    fig.show()



if __name__ == '__main__':
    get_figure()
    app.run_server(debug=True, host='127.0.0.1', port=8080)

