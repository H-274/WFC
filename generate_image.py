import random

from tile_objects.tile import SimpleTile
from tileset_data_parser import TilesetDataParser
from tile_objects.simple_tileset import SimpleTileset
from PIL import Image

from timer import Timer

print(">> Creating parser, tileset and timer objects")
parser = TilesetDataParser("tilesets/simple_sockets/tileset1_data.json")
tileset = SimpleTileset(parser.parse_tileset_data())
timer = Timer()

print(">> Making tileset image object")
tileset_image = Image.open(tileset.image_path)

print(">> Making output image object")
tile_count_width = int(input("How many tiles wide?\n> "))
tile_count_height = int(input("How many tiles high?\n> "))
output_size = (tileset.tile_width * tile_count_width, tileset.tile_height * tile_count_height)

output_image = Image.new("RGBA", output_size)
output_image.save("output.png", "PNG")

cells = {}
print(">> Generating empty tiles in the cells")
for i in range(tile_count_height * tile_count_width):
    pos_x = i % tile_count_width
    pos_y = i // tile_count_width
    cells[(pos_x, pos_y)] = SimpleTile(pos_x, pos_y)


def draw_cell(collapsed_cell):
    output_image = Image.open("output.png")

    box_left = tileset.tiles[collapsed_cell.tileset_index]["tileCoords"][0] * 30
    box_top = tileset.tiles[collapsed_cell.tileset_index]["tileCoords"][1] * 30
    box_right = tileset.tiles[collapsed_cell.tileset_index]["tileCoords"][0] * 30 + 30
    box_bottom = tileset.tiles[collapsed_cell.tileset_index]["tileCoords"][1] * 30 + 30

    tile_image = tileset_image.crop((box_left, box_top, box_right, box_bottom))

    box_left = collapsed_cell.pos_x * 30
    box_top = collapsed_cell.pos_y * 30
    box_right = collapsed_cell.pos_x * 30 + 30
    box_bottom = collapsed_cell.pos_y * 30 + 30

    output_image.paste(tile_image, (box_left, box_top, box_right, box_bottom))

    output_image.save("output.png", "PNG")


print(">> Beginning the wave collapse function")
timer.start()
for i in range(len(cells)):
    print(f"    - Calculating cell {i + 1}")
    cell_to_draw = None

    for cell in cells:
        if cells[cell].tileset_index is None:
            cell_neighbours = cells[cell].get_neighbours()

            for neighbour in cell_neighbours:  # Determines the required sockets

                try:
                    neighbour.socket_information = cells[(neighbour.pos_x, neighbour.pos_y)].socket_information
                except KeyError:
                    neighbour.socket_information = [False, False, False, False]  # Comment out the line and replace with pass to ignore border constraint

                if neighbour.pos_x < cells[cell].pos_x:  # Neighbour to the left of cell
                    cells[cell].socket_information[0] = neighbour.socket_information[2]
                elif neighbour.pos_y < cells[cell].pos_y:  # Neighbour is above cell
                    cells[cell].socket_information[1] = neighbour.socket_information[3]
                elif neighbour.pos_x > cells[cell].pos_x:  # Neighbour is to the right of cell
                    cells[cell].socket_information[2] = neighbour.socket_information[0]
                elif neighbour.pos_y > cells[cell].pos_y:  # Neighbour is under cell
                    cells[cell].socket_information[3] = neighbour.socket_information[1]

            cells[cell].entropy = tileset.determine_entropy(cells[cell])

            if cell_to_draw is None or cells[cell].entropy < cell_to_draw.entropy:
                cell_to_draw = cells[cell]

    cell_to_draw.tileset_index = random.choice(tileset.get_possible_tile_indexes(cell_to_draw))
    chosen_tile_socket_info = tileset.tiles[cell_to_draw.tileset_index]["socketInformation"]
    cell_to_draw.socket_information = [chosen_tile_socket_info["connectionLeft"],
                                       chosen_tile_socket_info["connectionUp"],
                                       chosen_tile_socket_info["connectionRight"],
                                       chosen_tile_socket_info["connectionDown"]]

    draw_cell(cell_to_draw)
timer.stop()
