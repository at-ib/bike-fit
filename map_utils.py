import folium
from streamlit_folium import st_folium


def add_folium_map():
    m = get_folium_map()
    st_folium(m, height=700, width=900, use_container_width=False, returned_objects=["last_object_clicked_tooltip"])


def get_folium_map():
    return folium.Map(location=[51.5, -0.118], zoom_start=10, tiles="cartodbpositron", prefer_canvas=True, min_zoom=8)