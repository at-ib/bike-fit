# bike-fit

A project to explore how we can encourage people to exercise using London's bike sharing scheme

## Running the app

`streamlit run Home.py`

## Preparing the data

I have committed the data to this repo.
MSOA boundaries are only available 
[from the ONS](https://geoportal.statistics.gov.uk/datasets/ons::msoa-dec-2011-boundaries-generalised-clipped-bgc-ew-v3/explore)
with EPSG:27700 projection (file MSOA_Dec_2011_Boundaries_Generalised_Clipped_BGC_EW_V3_2022_-6388113088635504944.geojson).
I converted them to EPSG:4326 by installing gdal (`brew install gdal`) and then using the command
`ogr2ogr -f "GeoJSON" msoa.geojson MSOA_Dec_2011_Boundaries_Generalised_Clipped_BGC_EW_V3_2022_-6388113088635504944.geojson -s_srs EPSG:27700 -t_srs EPSG:4326`.
`msoa.geojson` is the output.

## Formatting

Run linters and formatters with `make tidy`