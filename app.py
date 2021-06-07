from flask import Flask
import dash
import json
import h3
from flask import request
import json
import plotly.express as px
import polyfill
import pandas as pd
from geojson import Feature, Point, FeatureCollection, Polygon
from pandas.io.json import json_normalize
import dash_html_components as html
import dash_core_components as dcc




server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(server=server, external_stylesheets=external_stylesheets)

df = pd.read_csv("coordinates.csv", dtype={"id": str})
# maps = f'https://tile0.maps.2gis.com/tiles?x={lat}&y={lon}&z={z}'



def get_coordinates():
    with open("data.json", "r") as f:
        return json.load(f)


def get_geometry(df):
    raw_data = get_coordinates()
    list_features = []
    h3_ceil = []
    for rd in raw_data['features']:
        len_coord = len(rd['geometry']['coordinates'][0])
        for i in range(len_coord):
            lat = rd['geometry']['coordinates'][0][i][0]
            lng = rd['geometry']['coordinates'][0][i][1]
            ceil = h3.geo_to_h3(lat, lng, 10)
            h3_ceil.append(ceil)
            points = Polygon([h3.h3_to_geo_boundary(ceil, True)])
            feature = Feature(geometry=points,
                              id=ceil,
                              )
            list_features.append(feature)
    df['geometry'] = pd.Series(h3_ceil)
    return FeatureCollection(list_features)


def get_figure():
    geoJson = get_geometry(df)
    fig = px.choropleth_mapbox(df, geojson=geoJson, locations=df.geometry,
                               color=df.color, featureidkey='id', mapbox_style="carto-positron",
                               zoom=10, center={"lat": 54.757826, "lon":  83.097113},
                               )
    # Set templates

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    app.layout = html.Div([
        dcc.Graph(
            figure=fig
        )
    ])

    return fig.show()


if __name__ == '__main__':
    get_figure()
    app.run_server(debug=True, host='0.0.0.0', port=8080)

