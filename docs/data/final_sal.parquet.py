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

# Write the GeoDataFrame to parquet file
gdf.to_parquet('docs/data/temp_final_sal.parquet')

# read in binary mode
with open('docs/data/temp_final_sal.parquet', 'rb') as file:
    data = file.read()
    sys.stdout.buffer.write(data)

os.remove('docs/data/final_sal.feather')
os.remove('docs/data/temp_final_sal.parquet')