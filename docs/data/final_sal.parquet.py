import os
import requests
import sys
import pyarrow.feather as feather
import pyarrow.parquet as pq

response = requests.get(
    "https://github.com/tpisel/walkability/raw/master/data/final/final_sal.feather", 
    allow_redirects=True)

# Open the file in write mode 
with open('docs/data/final_sal.feather', 'wb') as file:
    # Write the contents of the response to the file
    file.write(response.content)

feather_table = feather.read_table('docs/data/final_sal.feather')
pq.write_table(feather_table, 'docs/data/temp_final_sal.parquet')

# read in binary mode
with open('docs/data/temp_final_sal.parquet', 'rb') as file:
    # read the file
    data = file.read()
    # write bytes to stdout
    sys.stdout.buffer.write(data)

os.remove('docs/data/final_sal.feather')
os.remove('docs/data/temp_final_sal.parquet')