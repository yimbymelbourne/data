import os
import requests
import sys
import pyarrow.feather as feather
import pyarrow.parquet as pq

# We need to convert Tom's feather file to parquet and write it to stdout:
# https://observablehq.com/framework/loaders
response = requests.get(
    "https://github.com/tpisel/walkability/raw/master/data/final/final_sal.feather", 
    allow_redirects=True)

# write in binary mode
with open('docs/data/final_sal.feather', 'wb') as file:
    file.write(response.content)

feather_table = feather.read_table('docs/data/final_sal.feather')
pq.write_table(feather_table, 'docs/data/temp_final_sal.parquet')

# read in binary mode
with open('docs/data/temp_final_sal.parquet', 'rb') as file:
    data = file.read()
    sys.stdout.buffer.write(data)

os.remove('docs/data/final_sal.feather')
os.remove('docs/data/temp_final_sal.parquet')