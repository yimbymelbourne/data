import os
import requests
import sys
import geopandas as gpd
from typing import Literal


def print_walkability_file_to_stdout(name, type: Literal["parquet", "geojson"]):
    response = requests.get(
        f"https://github.com/tpisel/walkability/raw/master/data/final/{name}.feather", 
        allow_redirects=True)

    # write in binary mode
    with open(f'temp/{name}.feather', 'wb') as file:
        file.write(response.content)

    # Use geopandas to read the feather file
    gdf = gpd.read_feather(f'temp/{name}.feather')

    # write the GeoDataFrame to parquet file
    if type == "parquet":
        gdf.to_parquet(f'temp/{name}.parquet')

        with open(f'temp/{name}.parquet', 'rb') as file:
            data = file.read()
            sys.stdout.buffer.write(data)

    if type == "geojson":
        # Max Bo: no idea what to_crs does, Tom told me to do it.
        gdf.to_crs(epsg=4326).to_file(f"temp/{name}.geojson", driver='GeoJSON')

        # read in binary mode
        with open(f'temp/{name}.geojson', 'rb') as file:
            data = file.read()
            sys.stdout.buffer.write(data)
