# bike-fit

A streamlit app to explore how we can encourage people to exercise using London's bike sharing scheme.

## Running the app

1. Clone the repo

2. Install requirements: `pip install -r requirements.txt` (preferably in a [virtual environment](https://virtualenvwrapper.readthedocs.io/en/latest/))

3. Run the app with `streamlit run Home.py`

## Data

I have committed the data to this repo. With more time I would have stored it separately.

MSOA boundaries are only available 
[from the ONS](https://geoportal.statistics.gov.uk/datasets/ons::msoa-dec-2011-boundaries-generalised-clipped-bgc-ew-v3/explore)
with EPSG:27700 projection (file MSOA_Dec_2011_Boundaries_Generalised_Clipped_BGC_EW_V3_2022_-6388113088635504944.geojson).
I converted them to EPSG:4326 by installing gdal (`brew install gdal`) and then using the command:
```bash
ogr2ogr -f "GeoJSON" msoa.geojson MSOA_Dec_2011_Boundaries_Generalised_Clipped_BGC_EW_V3_2022_-6388113088635504944.geojson -s_srs EPSG:27700 -t_srs EPSG:4326
```
`msoa.geojson` is the output.

Other source urls are provided in the data getting functions in `data_utils.py`

## Project structure
- `Home.py` and files in `pages/` are to make a [multi-page Streamlit app](https://docs.streamlit.io/library/get-started/multipage-apps)

## Formatting

Run linters and formatters with `make tidy`


## Tests

With more time I would have written some tests!