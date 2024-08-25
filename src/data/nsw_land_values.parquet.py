import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import zipfile
import sys

zip_path = 'src/data/LV_20240801.zip'

data_frames = []


with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for csv_filename in zip_ref.namelist():
        if not csv_filename.endswith('.csv'):
            continue

        with zip_ref.open(csv_filename, 'r') as csvfile:
            try:
                df = pd.read_csv(csvfile, usecols=[
                    'DISTRICT CODE', 'DISTRICT NAME', 'PROPERTY ID', 'PROPERTY TYPE',
                    'SUBURB NAME', 'POSTCODE', 'ZONE CODE',
                    'AREA', 'AREA TYPE', 'BASE DATE 1', 'LAND VALUE 1',
                    'AUTHORITY 1', 'BASIS 1'
                ], dtype={
                    'PROPERTY ID': str
                })
            except:
                continue

            data_frames.append(df)



# Concatenate all DataFrames into one
final_df = pd.concat(data_frames, ignore_index=True)

# downgrade LAND VALUE 1 to a standard number instead of a BigInt
final_df['LAND VALUE 1'] = final_df['LAND VALUE 1'].astype('float64')

# Write DataFrame to a temporary file-like object
buf = pa.BufferOutputStream()
table = pa.Table.from_pandas(final_df)
pq.write_table(table, buf, compression="snappy")

# Get the buffer as a bytes object
buf_bytes = buf.getvalue().to_pybytes()

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)