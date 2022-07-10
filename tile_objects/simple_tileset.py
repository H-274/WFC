class SimpleTileset:

    def __init__(self, tileset_data):
        self.name = tileset_data["tilesetName"]
        self.image_path = tileset_data["tilesetImagePath"]
        self.tiles = tileset_data["tiles"]
        self.expected_tile_count = tileset_data["tileCount"]
        self.tileset_rows = tileset_data["tilesetRows"]
        self.tileset_columns = tileset_data["tilesetColumns"]
        self.tile_width = tileset_data["singleTileWidth"]
        self.tile_height = tileset_data["singleTileHeight"]

    def determine_entropy(self, cell):
        return len(self.get_possible_tile_indexes(cell))

    def get_possible_tile_indexes(self, cell):
        possible_indexes = []
        cell_sockets = cell.socket_information

        for tile in self.tiles:
            tile_sockets = tile["socketInformation"]

            if ((cell_sockets[0] is None) or (tile_sockets["connectionLeft"] == cell_sockets[0])) and \
                    ((cell_sockets[1] is None) or (tile_sockets["connectionUp"] == cell_sockets[1])) and \
                    ((cell_sockets[2] is None) or (tile_sockets["connectionRight"] == cell_sockets[2])) and \
                    ((cell_sockets[3] is None) or (tile_sockets["connectionDown"] == cell_sockets[3])):
                possible_indexes.append(self.tiles.index(tile))

        return possible_indexes
