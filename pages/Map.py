import streamlit

from map_utils import add_folium_map


def page_content():
    streamlit.markdown(
        """
        # Use the map to explore BikePoint locations
        """
    )
    add_folium_map()


streamlit.set_page_config(page_title="Map", layout="wide")
page_content()
