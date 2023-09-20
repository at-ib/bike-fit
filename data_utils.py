import io

import pandas
import requests as requests
import streamlit

BIKE_POINT_URL = "https://api.tfl.gov.uk/BikePoint/"
FINGERTIPS_URL = "https://fingertips.phe.org.uk/api/all_data/csv/for_one_indicator"

LATEST_PERIOD = "2019/20 - 21/22"


def get_bike_point_data():
    response = requests.get(BIKE_POINT_URL)
    data = response.json()
    props = {
        point["id"]: {"common_name": point["commonName"], "lat": point["lat"], "lon": point["lon"]} for point in data
    }
    additional_props = {point["id"]: point["additionalProperties"] for point in data}
    additional_props = {k: process_additional_properties(v) for k, v in additional_props.items()}
    return pandas.DataFrame({k: {**props[k], **additional_props[k]} for k in props}).T


def process_additional_properties(ap):
    df = pandas.DataFrame(ap)
    return df.set_index("key")["value"].to_dict()


def get_fingertips_data_by_indicator_id(indicator_id):
    # Docs for this endpoint: https://fingertips.phe.org.uk/api#!/Data/Data_GetDataFileForOneIndicator
    url = FINGERTIPS_URL
    params = {"indicator_id": indicator_id}
    response = requests.get(url, params)
    return pandas.read_csv(io.StringIO(response.text), low_memory=False)


@streamlit.cache_data
def get_prevalance_of_overwieght_year_6():
    # ID is from https://fingertips.phe.org.uk/profile/national-child-measurement-programme/data
    # With more time I would find adult data
    indicator_id = 93108
    df = get_fingertips_data_by_indicator_id(indicator_id)
    df = df[df["Area Type"] == "MSOA"]
    df = df[df["Time period"] == LATEST_PERIOD]
    df = df[df["Area Code"].isin(get_london_msoa_codes())]
    return df[["Area Code", "Area Name",  "Value"]]


def get_london_msoa_codes():
    df = pandas.read_csv("data/london-msoa-data.csv")
    return df["Middle Super Output Area"].to_list()
