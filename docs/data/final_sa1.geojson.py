from loaders import print_feather_file_to_stdout

name = "final_sa1"
url = f"https://github.com/tpisel/walkability/raw/master/data/final/{name}.feather" 

print_feather_file_to_stdout(name=name, url=url, type="geojson")