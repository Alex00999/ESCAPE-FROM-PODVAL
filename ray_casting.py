import pygame
from settings import *
from mapdata import world_map, map_width, map_height
from math import sin, cos


def surface_hit(x, y):
    return (x // TILE_SIZE) * TILE_SIZE, (y // TILE_SIZE) * TILE_SIZE


def ray_casting(player, textures):
    walls = []
    x0, y0 = player.pos
    texture_v, texture_h = 1, 1
    x_square, y_square = surface_hit(x0, y0)  # координаты угла квадрата
    ray_angle = player.angle - HALF_FOV
    for ray in range(RAYS_NUMBER):
        sin_a = sin(ray_angle)
        cos_a = cos(ray_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # алгоритм брезенхема
        x, dx = (x_square + TILE_SIZE, 1) if cos_a >= 0 else (x_square, -1)
        for i in range(0, TILE_SIZE * map_width, TILE_SIZE):
            depth_v = (x - x0) / cos_a
            y_vertical = y0 + depth_v * sin_a
            tile_vertical = surface_hit(x + dx, y_vertical)
            if tile_vertical in world_map:
                texture_v = world_map[tile_vertical]
                break
            x += dx * TILE_SIZE

        y, dy = (y_square + TILE_SIZE, 1) if sin_a >= 0 else (y_square, -1)
        for i in range(0, TILE_SIZE * map_height, TILE_SIZE):
            depth_h = (y - y0) / sin_a
            x_horizontal = x0 + depth_h * cos_a
            tile_horizontal = surface_hit(x_horizontal, y + dy)
            if tile_horizontal in world_map:
                texture_h = world_map[tile_horizontal]
                break
            y += dy * TILE_SIZE

        depth, offset, texture = (depth_v, y_vertical, texture_v) if depth_v < depth_h else (
            depth_h, x_horizontal, texture_h)

        offset = int(offset) % TILE_SIZE
        depth *= cos(player.angle - ray_angle)
        depth = max(depth, 0.00001)
        projection_height = int(SCALE_COEFFICIENT / depth)
        if projection_height > HEIGHT:
            co = projection_height / HEIGHT
            texture_height = TEXTURE_HEIGHT / co
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE,
                                                       HALF_TEXTURE_HEIGHT - texture_height // 2,
                                                       TEXTURE_SCALE, texture_height)
            wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
            walls_position = (ray * SCALE, 0)
        else:
            try:
                wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
                wall_column = pygame.transform.scale(wall_column, (SCALE, projection_height))
                walls_position = (ray * SCALE, HALF_HEIGHT - projection_height // 2)
            except KeyError:
                wall_column = textures['*'].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
                wall_column = pygame.transform.scale(wall_column, (SCALE, projection_height))
                walls_position = (ray * SCALE, HALF_HEIGHT - projection_height // 2)

        walls.append((depth, wall_column, walls_position))
        ray_angle += DELTA_ANGLE
    return walls
