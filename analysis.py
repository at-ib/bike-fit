import pandas
import streamlit
from geopandas import GeoDataFrame

from constants import AREA_CODE_FIELD
from data_utils import get_bike_point_data
from map_utils import get_london_msoa_boundaries

from shapely.geometry import Point

from settings import DATA_DIR

USAGE_FILE = "374JourneyDataExtract12Jun2023-18Jun2023.csv"


@streamlit.cache_data
def get_number_of_docks_per_msoa(bike_points):
    bike_points = add_msoa_data(bike_points)
    docks = bike_points[["NbDocks", AREA_CODE_FIELD]].astype({"NbDocks": int, AREA_CODE_FIELD: str}).groupby(AREA_CODE_FIELD, as_index=False).sum()
    return docks.rename(columns={"MSOA11CD": "Area Code", "NbDocks": "Value"})


def add_msoa_data(bike_points):
    geometry = bike_points.apply(lambda x: Point(x["lon"], x["lat"]), axis=1)
    # To assign BikePoints to MSOAs we need to uses geopandas.sjoin, which means converting to GeoDataFrame
    bike_points = GeoDataFrame(bike_points.assign(geometry=geometry))
    boundaries = GeoDataFrame.from_features(get_london_msoa_boundaries())
    bike_points = bike_points.sjoin(boundaries)
    return bike_points


def get_usage_by_msoa(bike_points):
    usage = get_usage_by_bike_point()
    # Zero pad station numbers to match bike_points
    usage = usage.assign(station_number=usage["station_number"].map("{:06d}".format))
    bike_points = bike_points.merge(usage, left_on="TerminalName", right_on="station_number")
    bike_points = add_msoa_data(bike_points)
    #  TODO generalise this with get_number_of_docks_per_msoa
    return bike_points[["starts", "ends", AREA_CODE_FIELD]].groupby(AREA_CODE_FIELD, as_index=False).sum()


@streamlit.cache_data
def get_number_of_journey_starts_or_ends_per_msoa(bike_points, starts_or_ends):
    df = get_usage_by_msoa(bike_points)
    return df[[AREA_CODE_FIELD, starts_or_ends]].rename(columns={AREA_CODE_FIELD: "Area Code", starts_or_ends: "Value"})


def get_usage_by_bike_point():
    df = pandas.read_csv(DATA_DIR / USAGE_FILE)
    # With more time I would look at journey duration and data for a longer time period
    df = pandas.concat([count_vals(df["Start station number"], "starts"), count_vals(df["End station number"], "ends")], axis=1)
    return df.reset_index(names="station_number")


def count_vals(ser, name):
    # There's probably a more elegant way to do this
    return pandas.DataFrame(ser.value_counts()).rename(columns={"count": name})


def get_starts_per_dock(docks, starts):
    df = pandas.merge(docks, starts, on="Area Code", suffixes=("Starts", "Docks"))
    df = df.assign(Value=df["ValueStarts"]/df["ValueDocks"])
    return df[["Area Code", "Value"]]
