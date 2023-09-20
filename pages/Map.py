import streamlit
from streamlit_folium import st_folium

from data_utils import get_bike_point_data, get_prevalance_of_overwieght_year_6, get_population_by_msoa, \
    get_number_of_obese_children
from map_utils import add_boundary_layer, get_london_msoa_boundaries, add_choropleth_layer, \
    get_folium_map, add_bike_points


NONE = "None"
BOUNDARIES = "MSOA boundaries"
OBESE_PREVALANCE = "Obesity prevalance choropleth"
POPULATION = "Population choropleth"
OBESE_NUMBER = "Number of obese children"

def page_content():
    streamlit.markdown(
        """
        # Use the map to explore BikePoint locations
        """
    )
    layer_to_show = streamlit.radio("Select additional layer", options=[NONE, BOUNDARIES, OBESE_PREVALANCE, POPULATION, OBESE_NUMBER], key="layer_to_show")
    bike_points = get_bike_point_data()
    m = get_folium_map()
    boundaries = get_london_msoa_boundaries()
    notes = ""
    # With more time I would restructure this "if, elif" ladder probably using a dictionary
    if layer_to_show == BOUNDARIES:
        m = add_boundary_layer(boundaries, m)
    elif layer_to_show == OBESE_PREVALANCE:
        df = get_prevalance_of_overwieght_year_6()
        m = add_choropleth_layer(boundaries, m, df)
        notes = """
        This obesity measure is only for year 6 children. With more time I would have looked for data for adults.
        
        With more time I also would have considered other measures like IMD
        """
    elif layer_to_show == POPULATION:
        df = get_population_by_msoa()
        m = add_choropleth_layer(boundaries, m, df)
        notes = """
        With more time I would have looked at where businesses and attractions are.
        """
    elif layer_to_show == OBESE_NUMBER:
        df = get_number_of_obese_children()
        m = add_choropleth_layer(boundaries, m, df)
        notes = "Potential policy option: A collection of BikePoints in East London around Barking"
    m = add_bike_points(bike_points, m)
    streamlit.markdown(notes)
    st_folium(m, height=700, width=900, use_container_width=False, returned_objects=[])


streamlit.set_page_config(page_title="Map", layout="wide")
page_content()
