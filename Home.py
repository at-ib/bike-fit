import streamlit

from settings import APP_NAME


def page_content():
    streamlit.markdown(
        f"""
        # {APP_NAME}

        Welcome to the Bike fit minimum viable product.
        The Bike fit app is a tool for exploring ways to encourage people to exercise using London's
        [cycle hire scheme](https://tfl.gov.uk/modes/cycling/santander-cycles).
        """
    )


############ Script ############# # noqa
streamlit.set_page_config(page_title=f"{APP_NAME}: home", layout="wide")
page_content()
