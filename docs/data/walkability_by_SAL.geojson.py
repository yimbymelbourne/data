from loaders import print_parquet_file_to_stdout

name = "walkability_by_SAT"
url = 'https://tompisel.com/data/walkability_by_SAL.parquet'

print_parquet_file_to_stdout(name=name, url=url, type="geojson")