import json


class TilesetDataParser:

    def __init__(self, json_dir):
        self.json_dir = json_dir

    def parse_tileset_data(self):
        print(">> Parsing data from JSON file")
        json_file = open(self.json_dir).read()
        data = json.loads(json_file)

        return data
