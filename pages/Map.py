import streamlit


def page_content():
    streamlit.markdown(
        """
        # Use the map to explore BikePoint locations
        """
    )


############ Script ############# # noqa
streamlit.set_page_config(page_title="Map", layout="wide")
page_content()
