import streamlit

from settings import APP_NAME

FUTURE_WORK = """
1. **Look at the average number of BikePoints within a 10 minute cycle of a BikePoint for each MSOA**.
If this number is small people may be less likely to use the bikes.

1. **Consider other metrics like IMD**. So far we have only considered obesity in year 6 children.
Adult obesity would be a better metric as children under 14
[cannot use the bikes](https://tfl.gov.uk/corporate/terms-and-conditions/santander-cycles) and adults are the primary
users.

1. **Look for demographic data on bike users** The biggest part of the analysis that's missing is whether more bikes
would lead to higher usage among people who exercise the least.
"""


def page_content():
    streamlit.markdown(FUTURE_WORK)


streamlit.set_page_config(page_title=f"{APP_NAME}: Future work")
page_content()
