import streamlit


def page_content():
    streamlit.markdown(
        """
        # Bike fit

        Welcome to the Bike fit minimum viable product.
        The Bike fit app is a tool for exploring ways to encourage people to exercise using London's
        [cycle hire scheme](https://tfl.gov.uk/modes/cycling/santander-cycles).
        """
    )


############ Script ############# # noqa
streamlit.set_page_config(page_title="Home", layout="wide")
page_content()
