import streamlit
from streamlit_folium import st_folium

from data_utils import get_bike_point_data
from map_utils import get_bike_point_map, add_folium_layer, get_london_msoa_boundaries


def page_content():
    streamlit.markdown(
        """
        # Use the map to explore BikePoint locations
        """
    )
    show_obesity = streamlit.toggle("Show year 6 obesity by MSOA", value=False, key="show_obesity", label_visibility="visible")
    bike_points = get_bike_point_data()
    m = get_bike_point_map(bike_points)
    if show_obesity:
        boundaries = get_london_msoa_boundaries()
        m = add_folium_layer(boundaries, m)
    st_folium(m, height=700, width=900, use_container_width=False, returned_objects=[])


streamlit.set_page_config(page_title="Map", layout="wide")
page_content()
