import streamlit
from streamlit_folium import st_folium

from data_utils import get_bike_point_data, get_prevalance_of_overwieght_year_6
from map_utils import add_boundary_layer, get_london_msoa_boundaries, add_choropleth_layer, \
    get_folium_map, add_bike_points


def page_content():
    streamlit.markdown(
        """
        # Use the map to explore BikePoint locations
        """
    )
    layer_to_show = streamlit.radio("Select additional layer", options=["None", "MSOA boundaries", "Obesity choropleth"], key="layer_to_show")
    bike_points = get_bike_point_data()
    m = get_folium_map()
    boundaries = get_london_msoa_boundaries()
    if layer_to_show == "MSOA boundaries":
        m = add_boundary_layer(boundaries, m)
    elif layer_to_show == "Obesity choropleth":
        df = get_prevalance_of_overwieght_year_6()
        m = add_choropleth_layer(boundaries, m, df)
    m = add_bike_points(bike_points, m)
    st_folium(m, height=700, width=900, use_container_width=False, returned_objects=[])


streamlit.set_page_config(page_title="Map", layout="wide")
page_content()
