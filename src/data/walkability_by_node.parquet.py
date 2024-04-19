from loaders import print_parquet_file_to_stdout

name = "walkability_by_node"
url = 'https://tompisel.com/data/walkability_by_node.parquet'

print_parquet_file_to_stdout(name=name, url=url, sample=10000, type="parquet")