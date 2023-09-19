import pandas
import requests as requests

BIKE_POINT_URL = "https://api.tfl.gov.uk/BikePoint/"


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
