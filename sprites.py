import pygame
from settings import *
from math import sqrt, atan2, cos, degrees
from collections import deque
from player import Player

player = Player()


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'enemy': {
                'sprite': pygame.image.load('resources/enemy/enemy.png').convert_alpha(),
                'shift': 0,
                'scale': 1,
                'side': 50,
                'animation': [],
                'death_anim': deque(
                    [pygame.image.load(f'resources/enemy_dead/death{i}.png').convert_alpha() for i in range(5)]),
                'is_dead': None,
                'dead_shift': 0.5,
                'animation_dist': 800,
                'animation_speed': 40,
                'flag': 'npc',
                'blocked': True,
                'obj_action': deque(
                    [pygame.image.load(f'resources/enemy/enemy{i}.png').convert_alpha() for i in range(4)]),
            }
        }
        self.sprite_list = [
            Sprite(self.sprite_parameters['enemy'], (8.5, 75.5), False),
            Sprite(self.sprite_parameters['enemy'], (18.5, 75.5), False),
            Sprite(self.sprite_parameters['enemy'], (13.5, 60.5), True),
            Sprite(self.sprite_parameters['enemy'], (9.5, 50.5), True),
            Sprite(self.sprite_parameters['enemy'], (4.5, 46.5), True),
            Sprite(self.sprite_parameters['enemy'], (24.5, 48.5), False),
            Sprite(self.sprite_parameters['enemy'], (24.5, 50.5), False),
            Sprite(self.sprite_parameters['enemy'], (37.5, 45.5), False),
            Sprite(self.sprite_parameters['enemy'], (37.5, 51.5), True),
            Sprite(self.sprite_parameters['enemy'], (43.5, 23.5), False),
            Sprite(self.sprite_parameters['enemy'], (37.5, 16.5), True),
            Sprite(self.sprite_parameters['enemy'], (27.5, 7.5), True),
            Sprite(self.sprite_parameters['enemy'], (59.5, 13.5), True),
            Sprite(self.sprite_parameters['enemy'], (57.5, 22.5), False),
            Sprite(self.sprite_parameters['enemy'], (62.5, 13.5), False),
            Sprite(self.sprite_parameters['enemy'], (63.5, 10.5), True),
            Sprite(self.sprite_parameters['enemy'], (45.5, 11.5), True),
            Sprite(self.sprite_parameters['enemy'], (46.5, 38.5), False),
            Sprite(self.sprite_parameters['enemy'], (38.5, 33.5), True),
            Sprite(self.sprite_parameters['enemy'], (37.5, 18.5), False),
            Sprite(self.sprite_parameters['enemy'], (49.5, 18.5), False),

            Sprite(self.sprite_parameters['enemy'], (28.5, 4.5), True),
            Sprite(self.sprite_parameters['enemy'], (28.5, 3.5), True),
            Sprite(self.sprite_parameters['enemy'], (30.5, 4), False),
            Sprite(self.sprite_parameters['enemy'], (23.5, 22.5), False),
            Sprite(self.sprite_parameters['enemy'], (43.5, 46.5), False),
            Sprite(self.sprite_parameters['enemy'], (52.5, 7.5), True),
            Sprite(self.sprite_parameters['enemy'], (58.5, 29.5), True),

        ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.sprite_list], default=(float('inf'), 0))


class Sprite:
    def __init__(self, parameters, pos, aggressive):
        self.type = parameters['sprite']
        self.side = parameters['side']
        self.obj_action = parameters['obj_action'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        self.death_animation = parameters['death_anim'].copy()
        self.dead_animation_count = 0
        self.dead_animation_speed = 16
        self.aggressive = aggressive
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.hurt_frame = 0
        self.x, self.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.flag = parameters['flag']
        self.delete = False,
        self.npc_action_trigger = False,
        self.blocked = parameters['blocked']
        self.projection_height = 0

    @property
    def is_on_fire(self):
        if CENTER_RAY - self.side // 2 < self.ray < CENTER_RAY + self.side // 2 and self.blocked:
            return self.d_sprite, self.projection_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def sprite_locate(self, player_d, walls):
        dx, dy = self.x - player_d.x, self.y - player_d.y
        self.d_sprite = sqrt(dx ** 2 + dy ** 2)

        self.theta = atan2(dy, dx)
        gamma = self.theta - player_d.angle
        if dx > 0 and 180 <= degrees(player_d.angle) <= 360 or dx < 0 and dy < 0:
            gamma += pi * 2
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.ray = CENTER_RAY + delta_rays
        self.d_sprite *= cos(HALF_FOV - self.ray * DELTA_ANGLE)

        if 0 <= self.ray <= RAYS_NUMBER - 1 and self.d_sprite < walls[self.ray][0]:
            self.projection_height = min(int(SCALE_COEFFICIENT / self.d_sprite),
                                         DOUBLE_HEIGHT if self.flag not in {'door_h', 'door_v'} else HEIGHT)
            # half_projection_height = self.projection_height // 2
            sprite_width = int(self.projection_height * self.scale)
            sprite_height = int(self.projection_height * self.scale)
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            # logic for doors, npc, decor
            if self.is_dead and self.is_dead != 'immortal':
                sprite_object = self.dead_animation()
                shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1.3)
            elif self.npc_action_trigger:
                sprite_object = self.npc_in_action()
            else:
                # choose sprite for angle
                self.type = self.visible_sprite()
                # sprite animation
                sprite_object = self.sprite_animation()

            sprite_pos = (self.ray * SCALE - half_sprite_width, HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return self.d_sprite, sprite, sprite_pos
        else:
            return False,

    def sprite_animation(self):
        if self.animation and self.d_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.type

    def visible_sprite(self):
        return self.type

    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += self.dead_animation_speed
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 4
        else:
            self.obj_action.rotate()
        return sprite_object
