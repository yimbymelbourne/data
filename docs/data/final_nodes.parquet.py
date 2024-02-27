from loaders import print_feather_file_to_stdout

name = "final_nodes"
url = 'https://s3.ap-southeast-2.amazonaws.com/tompisel.com/collection/final_nodes.feather'

print_feather_file_to_stdout(name=name, url=url, type="parquet", sample=10000)