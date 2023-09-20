import json

import folium
import seaborn
import streamlit

from constants import AREA_CODE_FIELD, AREA_NAME_FIELD
from data_utils import get_london_msoa_codes
from settings import DATA_DIR

MSOA_BOUNDARIES = "msoa.geojson"


def add_bike_points(bike_points, m):
    pal = get_palette(1)
    for i in bike_points.index:
        folium.CircleMarker(
            location=(bike_points.loc[i, "lat"], bike_points.loc[i, "lon"]),
            color=pal[0],
            radius=4,
            tooltip=f'{bike_points.loc[i, "NbDocks"]} docks',
        ).add_to(m)
    return m


def get_palette(n_colors):
    return seaborn.color_palette("magma", n_colors=n_colors).as_hex()


def get_folium_map():
    return folium.Map(location=[51.5, -0.118], zoom_start=10, tiles="cartodbpositron", prefer_canvas=True, min_zoom=8)


def add_boundary_layer(boundaries, m, smooth_factor=0, style=None):
    if style is None:
        style = {}
    folium.GeoJson(
        boundaries,
        name="geojson_layer",
        tooltip=folium.GeoJsonTooltip(fields=[AREA_NAME_FIELD], labels=False, sticky=True),
        smooth_factor=smooth_factor,
        style_function=lambda feature: style,
    ).add_to(m)
    return m


def add_choropleth_layer(boundaries, m, data, smooth_factor=0):
    folium.Choropleth(
        boundaries,
        name="choropleth",
        data=data,
        columns=["Area Code", "Value"],
        key_on=f"feature.properties.{AREA_CODE_FIELD}",
        fill_color="GnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Value",
        highlight=True,
        smooth_factor=smooth_factor,
        style_function=lambda feature: {"weight": 0.5},
    ).add_to(m)
    return m


@streamlit.cache_data
def get_london_msoa_boundaries():
    with open(DATA_DIR / MSOA_BOUNDARIES) as f:
        boundaries = json.load(f)
    london_msoa_codes = get_london_msoa_codes()
    boundaries["features"] = [feat for feat in boundaries["features"] if feat["properties"][AREA_CODE_FIELD] in london_msoa_codes]
    return boundaries


