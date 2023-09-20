import streamlit
from geopandas import GeoDataFrame

from constants import AREA_CODE_FIELD
from data_utils import get_bike_point_data
from map_utils import get_london_msoa_boundaries

from shapely.geometry import Point


# @streamlit.cache_data
def get_number_of_docks_per_msoa():
    bike_points = get_bike_point_data()
    geometry = bike_points.apply(lambda x: Point(x["lon"], x["lat"]), axis=1)
    # To assign BikePoints to MSOAs we need to uses geopandas.sjoin, which means converting to GeoDataFrame
    bike_points = GeoDataFrame(bike_points.assign(geometry=geometry))
    boundaries = GeoDataFrame.from_features(get_london_msoa_boundaries())
    bike_points = bike_points.sjoin(boundaries)
    docks = bike_points[["NbDocks", AREA_CODE_FIELD]].astype({"NbDocks": int, AREA_CODE_FIELD: str}).groupby(AREA_CODE_FIELD, as_index=False).sum()
    return docks.rename(columns={"MSOA11CD": "Area Code", "NbDocks": "Value"})
