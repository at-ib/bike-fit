import streamlit
from streamlit_folium import st_folium

from data_utils import get_bike_point_data
from map_utils import get_bike_point_map


def page_content():
    streamlit.markdown(
        """
        # Use the map to explore BikePoint locations
        """
    )
    streamlit.toggle("Show year 6 obesity by MSOA", value=False, key="show_obesity", label_visibility="visible")
    bike_points = get_bike_point_data()
    m = get_bike_point_map(bike_points)
    st_folium(m, height=700, width=900, use_container_width=False, returned_objects=["last_object_clicked_tooltip"])


streamlit.set_page_config(page_title="Map", layout="wide")
page_content()
