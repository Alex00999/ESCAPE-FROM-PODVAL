from settings import *
from mapdata import world_map
from ray_casting import surface_hit
from math import atan2, pi
import pygame


def ray_casting_npc_player(npc_x, npc_y, world_map, player_pos):
    x0, y0 = player_pos
    x_square, y_square = surface_hit(x0, y0)  # координаты угла квадрата
    delta_x, delta_y = x0 - npc_x, y0 - npc_y
    ray_angle = atan2(delta_y, delta_x)
    ray_angle += pi

    sin_a = sin(ray_angle)
    cos_a = cos(ray_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = cos_a if cos_a else 0.000001

    # алгоритм брезенхема
    x, dx = (x_square + TILE_SIZE, 1) if cos_a >= 0 else (x_square, -1)
    for i in range(0, int(abs(delta_x)) // TILE_SIZE):
        depth_v = (x - x0) / cos_a
        y_vertical = y0 + depth_v * sin_a
        tile_vertical = surface_hit(x + dx, y_vertical)
        if tile_vertical in world_map:
            return False
        x += dx * TILE_SIZE

    y, dy = (y_square + TILE_SIZE, 1) if sin_a >= 0 else (y_square, -1)
    for i in range(0, int(abs(delta_y)) // TILE_SIZE):
        depth_h = (y - y0) / sin_a
        x_horizontal = x0 + depth_h * cos_a
        tile_horizontal = surface_hit(x_horizontal, y + dy)
        if tile_horizontal in world_map:
            return False
        y += dy * TILE_SIZE
    return True


class Interaction:
    def __init__(self, player, sprites, render):
        self.player = player
        self.sprites = sprites
        self.hurt_count = 0
        self.render = render

    def interaction_objects(self):
        if self.player.shot and self.render.shot_animation_trigger:
            for obj in sorted(self.sprites.sprite_list, key=lambda obj: obj.d_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos):
                            obj.is_dead = True
                            obj.blocked = None
                            self.render.shot_animation_trigger = False
                    break

    def npc_action(self):
        for obj in self.sprites.sprite_list:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos):
                    if self.hurt_count < FPS:
                        self.hurt_count += 1
                    else:
                        self.player.player_hurt(0.1)
                        self.render.damage()
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        if abs(obj.d_sprite) > TILE_SIZE and obj.aggressive:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1

    def resurrection(self):
        for obj in self.sprites.sprite_list:
            obj.is_dead = False

    def check_win(self):
        enemies_counter = len([obj for obj in self.sprites.sprite_list if obj.flag == 'npc' and not obj.is_dead])
        self.render.showEnemies(enemies_counter)
        if not enemies_counter:
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('resources/sound/win.mp3')
            pygame.mixer.music.play()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                self.render.win()
