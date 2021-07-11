# editor_mode
import pygame
import os


pygame.init()
width = 15
height = 9

class Sprite:
    width = 32
    height = 32

tiles = pygame.image.load("assets\\tiles3.png")
NUM_OF_TILES = tiles.get_size()[0] // 32
menu = pygame.image.load("assets\\menu2.png")
diamond = pygame.image.load("assets\\diamond.png")

from levels3 import *

def print_map():

    for num_room, room in enumerate(layout):
        print(f"Num. room = {num_room}")
        # room contains one room
        print(*room, sep="\n")
        print()

def room_to_list():
    # iterate the rooms
    for num_room, room in enumerate(layout):
        layout[num_room] = list(room)
    print("LAYOUT")
    print(layout)


def line_to_list():
    # iterate the rooms
    for num_room, room in enumerate(layout):
        # iterate each line of the room (room is made of 9 lines)
        for num_line, line in enumerate(room):
            # iterate the single number/letter representing a tile in a line string)
            # transform the line strings into lists
            layout[num_room][num_line] = line.split(" ")
    print(layout)


def str_to_num():
    for num_room, room in enumerate(layout):
        # iterate each line of the room (room is made of 9 lines)
        for num_line, line in enumerate(room):
            for num_item, item in enumerate(line):
                if item not in "CC":
                    if item == "__":
                        layout[num_room][num_line][num_item] = 0
                    else:
                        layout[num_room][num_line][num_item] = int(item)
    print("LAYOUT END")
    print(layout)


# layout contains the maps
def convert_map_to_list():
    print_map()
    room_to_list()
    line_to_list()
    str_to_num()


if __name__ == "__main__":
    convert_map_to_list()