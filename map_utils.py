import folium
import seaborn


def get_bike_point_map(bike_points):
    m = get_folium_map()
    return add_bike_points(bike_points, m)


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
    return folium.Map(location=[51.5, -0.118], zoom_start=12, tiles="cartodbpositron", prefer_canvas=True, min_zoom=8)
