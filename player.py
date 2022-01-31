from settings import *
import pygame
import math
from mapdata import collision_map


class Player:
    def __init__(self):
        self.x, self.y = PLAYER_POS
        self.hp_number = 200
        self.angle = PLAYER_ANGLE
        self.sensitivity = 0.0025
        self.side = 32
        self.rect = pygame.Rect(*PLAYER_POS, self.side, self.side)
        self.collision_list = collision_map
        self.shot = False

    @property
    def pos(self):
        return self.x, self.y

    @property
    def hp(self):
        return self.hp_number

    def player_hurt(self, hurt_points):
        self.hp_number -= hurt_points

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 20:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= pi * 2

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = PLAYER_SPEED * cos_a
            dy = PLAYER_SPEED * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -PLAYER_SPEED * cos_a
            dy = -PLAYER_SPEED * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = PLAYER_SPEED * sin_a
            dy = -PLAYER_SPEED * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -PLAYER_SPEED * sin_a
            dy = PLAYER_SPEED * cos_a
            self.detect_collision(dx, dy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True

        self.angle %= pi * 2

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            self.angle += difference * self.sensitivity
