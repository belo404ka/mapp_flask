from flask import Flask
import dash
import json
import h3
from flask import request
import json
import plotly.express as px
import polyfill
import pandas as pd
from geojson import Feature, Point, FeatureCollection
from pandas.io.json import json_normalize
import dash_html_components as html
import dash_core_components as dcc



server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(server=server, external_stylesheets=external_stylesheets)

H3_res = 10
lat = 54.748079
lon = 83.104486
z = 12.79


df = pd.read_csv("coordinates.csv",
                   dtype={"id": str})
# maps = f'https://tile0.maps.2gis.com/tiles?x={lat}&y={lon}&z={z}'



def get_coordinates():
    with open("data.json", "r") as f:
        return json.load(f)


def get_polylines():
    raw_data = get_coordinates()
    hexagons = []
    lat = []
    lng = []
    for rd in raw_data['features']:
        geoJson = dict(type="Polygon", coordinates=rd['geometry']['coordinates'])
        hexagons = list((h3.polyfill(geoJson, 10)))
    polylines = []
    for hex in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        lat.extend(map(lambda v: v[0], polyline))
        lng.extend(map(lambda v: v[1], polyline))
        polylines.append(Feature(polyline))
    return FeatureCollection(polylines)


def get_figure():
    fig = px.choropleth_mapbox(df, geojson=get_polylines(), locations=df.id,
                               color=df.color, mapbox_style="carto-positron",
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

