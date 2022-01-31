from settings import *
import pygame

MAP = []

with open(f'maps/map.txt', 'r') as f:
    for line in f:
        MAP.append(list(line))

map_width = len(max(MAP, key=len)) - 1
map_height = len(MAP)


world_map = {}
minimap_map = set()
collision_map = []
for i, row in enumerate(MAP):
    for j, block in enumerate(row):
        if block != ' ' and block != '\n':
            minimap_map.add((j * MAP_TILE, i * MAP_TILE))
            collision_map.append(pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            world_map[(j * TILE_SIZE, i * TILE_SIZE)] = block
