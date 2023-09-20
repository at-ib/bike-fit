import streamlit
from streamlit_folium import st_folium

from analysis import (
    get_number_of_docks_per_msoa,
    get_number_of_journey_starts_or_ends_per_msoa,
    get_starts_per_dock,
)
from data_utils import (
    get_bike_point_data,
    get_number_of_obese_children,
    get_population_by_msoa,
    get_prevalance_of_overwieght_year_6,
)
from map_utils import (
    add_bike_points,
    add_boundary_layer,
    add_choropleth_layer,
    get_folium_map,
    get_london_msoa_boundaries,
)
from settings import APP_NAME

LAYER_NAMES = {
    "none": "None",
    "boundaries": "MSOA boundaries",
    "obese_prev": "Obesity prevalance choropleth",
    "pop": "Population choropleth",
    "obese_num": "Number of obese children",
    "docks": "Number of BikePoint docks per MSOA",
    "starts": "Number of journeys started per week in each MSOA",
    "ends": "Number of journeys ended per week in each MSOA",
    "starts_per_dock": "Number of journeys started per week in each MSOA for each dock",
}


def page_content():
    streamlit.markdown(
        """
        # Use the map to explore BikePoint locations
        """
    )
    show_bike_points = streamlit.toggle("Show BikePoints", value=True)
    layer_to_show = streamlit.radio("Select additional layer", options=LAYER_NAMES.values(), key="layer_to_show")
    bike_points = get_bike_point_data()
    m = get_folium_map()
    boundaries = get_london_msoa_boundaries()
    m, notes = add_map_layer(bike_points, boundaries, layer_to_show, m)
    if show_bike_points:
        m = add_bike_points(bike_points, m)
    streamlit.markdown(notes)
    st_folium(m, height=700, width=900, use_container_width=False, returned_objects=[])


def add_map_layer(bike_points, boundaries, layer_to_show, m):
    # With more time I would restructure this "if, elif" ladder probably using a dictionary
    if layer_to_show == LAYER_NAMES["boundaries"]:
        m = add_boundary_layer(boundaries, m)
        notes = ""
    elif layer_to_show == LAYER_NAMES["obese_prev"]:
        df = get_prevalance_of_overwieght_year_6()
        m = add_choropleth_layer(boundaries, m, df)
        notes = """
        This obesity measure is only for year 6 children. With more time I would have looked for data for adults.

        With more time I also would have considered other measures like IMD
        """
    elif layer_to_show == LAYER_NAMES["pop"]:
        df = get_population_by_msoa()
        m = add_choropleth_layer(boundaries, m, df)
        notes = """
        With more time I would have looked at where businesses and attractions are.
        """
    elif layer_to_show == LAYER_NAMES["obese_num"]:
        df = get_number_of_obese_children()
        m = add_choropleth_layer(boundaries, m, df)
        notes = "Potential policy option: A collection of BikePoints in East London around Barking"
    elif layer_to_show == LAYER_NAMES["docks"]:
        df = get_number_of_docks_per_msoa(bike_points)
        m = add_choropleth_layer(boundaries, m, df)
        notes = "With more time I would have done the number of docks per area"
    elif layer_to_show == LAYER_NAMES["starts"]:
        df = get_number_of_journey_starts_or_ends_per_msoa(bike_points, "starts")
        m = add_choropleth_layer(boundaries, m, df)
        notes = """
        This is usage data for a week in June 2023. With more time I would have looked at the whole year.
        With more time I also would have normalised by area
        """
    elif layer_to_show == LAYER_NAMES["ends"]:
        df = get_number_of_journey_starts_or_ends_per_msoa(bike_points, "ends")
        m = add_choropleth_layer(boundaries, m, df)
        notes = """
        This is usage data for a week in June 2023. With more time I would have looked at the whole year.
        With more time I also would have normalised by area
        """
    elif layer_to_show == LAYER_NAMES["starts_per_dock"]:
        starts = get_number_of_journey_starts_or_ends_per_msoa(bike_points, "starts")
        docks = get_number_of_docks_per_msoa(bike_points)
        df = get_starts_per_dock(starts, docks)
        m = add_choropleth_layer(boundaries, m, df)
        notes = "With more time I would have looked at how this has changed over time"
    else:
        notes = ""
    return m, notes


streamlit.set_page_config(page_title=f"{APP_NAME}: Map", layout="wide")
page_content()
