class SimpleTile:

    def __init__(self, pos_x, pos_y, tileset_index=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tileset_index = tileset_index
        self.entropy = None
        self.socket_information = [None, None, None, None]

    def get_neighbours(self):
        return (SimpleTile(self.pos_x - 1, self.pos_y),
                SimpleTile(self.pos_x, self.pos_y - 1),
                SimpleTile(self.pos_x + 1, self.pos_y),
                SimpleTile(self.pos_x, self.pos_y + 1))

    def __eq__(self, tile):
        return (self.pos_x == tile.pos_x) and (self.pos_y == tile.pos_y)
