from flask import Flask
import dash
import json
import h3
import json
import plotly.express as px
import pandas as pd
from geojson import Feature, Point, FeatureCollection, Polygon
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


def get_geometry():
    raw_data = get_coordinates()
    list_features = []
    hexagons = []
    for rd in raw_data['features']:
        poll = dict(type="Polygon", coordinates=rd['geometry']['coordinates'])
        polyfill = h3.polyfill(poll, 10)
        hexagons.extend(polyfill)
        for hex in hexagons:
            points = h3.h3_set_to_multi_polygon([hex], True)
            geometry = dict(type="Polygon", coordinates=points[0])
            feature = Feature(geometry=geometry,
                              id=hex,
                              )
            list_features.append(feature)
    df['geometry'] = pd.Series(hexagons)
    return FeatureCollection(list_features)


def get_figure():
    geoJson = get_geometry()
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
