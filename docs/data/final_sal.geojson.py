import os
import requests
import sys
import geopandas as gpd

# We need to convert Tom's feather file to parquet and write it to stdout:
# https://observablehq.com/framework/loaders
response = requests.get(
    "https://github.com/tpisel/walkability/raw/master/data/final/final_sal.feather", 
    allow_redirects=True)

# write in binary mode
with open('docs/data/final_sal.feather', 'wb') as file:
    file.write(response.content)

# Use geopandas to read the feather file
gdf = gpd.read_feather('docs/data/final_sal.feather')

# Max Bo: no idea what to_crs does, Tom told me to do it.
gdf.to_crs(epsg=4326).to_file("docs/data/temp_final_sal.geojson", driver='GeoJSON')

# read in binary mode
with open('docs/data/temp_final_sal.geojson', 'rb') as file:
    data = file.read()
    sys.stdout.buffer.write(data)

os.remove('docs/data/final_sal.feather')
os.remove('docs/data/temp_final_sal.geojson')