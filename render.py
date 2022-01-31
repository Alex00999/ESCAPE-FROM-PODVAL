import pygame
from mapdata import minimap_map
from player import Player
from settings import *
from collections import deque
import sys

player = Player()


def play_theme():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load('resources/sound/theme.mp3')
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(10)


def main_menu(screen, clock):
    x = 12
    menu_picture = pygame.image.load('resources/bg.jpg').convert()
    menu_trigger = True
    pygame.mixer.music.load('resources/sound/mainmenu.mp3')
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(10)
    button_font = pygame.font.Font('resources/font.ttf', 72)
    start = button_font.render('START', True, pygame.Color((68, 164, 104)))
    button_start = pygame.Rect(0, 0, 400, 150)
    button_start.center = HALF_WIDTH, HALF_HEIGHT
    exit = button_font.render('EXIT', True, pygame.Color((68, 164, 104)))
    button_exit = pygame.Rect(0, 0, 400, 150)
    button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

    while menu_trigger:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(menu_picture, (0, 0), (x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
        x += 1

        pygame.draw.rect(screen, (68, 164, 104), button_start, width=10)
        screen.blit(start, (button_start.centerx - 130, button_start.centery - 35))

        pygame.draw.rect(screen, (68, 164, 104), button_exit, width=10)
        screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 35))

        label = pygame.image.load('resources/label.png').convert_alpha()
        screen.blit(label, (HALF_WIDTH - 1019 / 2, 100))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if button_start.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 102, 24), button_start)
            screen.blit(start, (button_start.centerx - 130, button_start.centery - 35))
            if mouse_click[0]:
                menu_trigger = False
        elif button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 102, 24), button_exit)
            screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 35))
            if mouse_click[0]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(20)


class Rendering:
    def __init__(self, screen, minimap, player, clock):
        self.screen = screen
        self.clock = clock
        self.font_win = pygame.font.Font('resources/font.ttf', 72)
        self.minimap = minimap
        self.player = player
        self.font = pygame.font.Font('resources/font.ttf', 40)
        self.font2 = pygame.font.Font('resources/font.ttf', 25)
        self.textures = {'B': pygame.image.load('resources/walls/brick.png').convert(),
                         'C': pygame.image.load('resources/walls/cage.png').convert(),
                         'S': pygame.image.load('resources/walls/computer.png').convert(),
                         'D': pygame.image.load('resources/walls/darkbrick.png').convert(),
                         'c': pygame.image.load('resources/walls/darkbrick_caged.png').convert(),
                         'd': pygame.image.load('resources/walls/darkstone.png').convert(),
                         'O': pygame.image.load('resources/walls/door.png').convert(),
                         '*': pygame.image.load('resources/walls/freedom.png').convert(),
                         'I': pygame.image.load('resources/walls/iron.png').convert(),
                         'G': pygame.image.load('resources/walls/greybrick.png').convert(),
                         'P': pygame.image.load('resources/walls/plate.png').convert()

                         }
        # параматеры оружия
        self.weapon_base = pygame.image.load('resources/gun/gun0.png').convert_alpha()
        self.weapon_animation = deque([pygame.image.load(f'resources/gun/gun{i}.png').convert_alpha()
                                       for i in range(1, 6)])
        self.weapon_rect = self.weapon_base.get_rect()
        self.weapon_position = (HALF_WIDTH - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_animation)
        self.shot_length_count = 0
        self.shot_sound_length_count = 0
        self.shot_animation_speed = 7
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound('resources/sound/shotgun.mp3')
        self.shot_sound.set_volume(0.5)

    def win(self):
        button_font = pygame.font.Font('resources/font.ttf', 72)
        render = self.font_win.render('You have won !!!', True, (68, 164, 104))
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, BLACK, rect)
        exit = button_font.render('EXIT', True, pygame.Color((68, 164, 104)))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200
        pygame.draw.rect(self.screen, (68, 164, 104), button_exit, width=10)
        self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 35))
        self.screen.blit(render, (HALF_WIDTH - 300, HALF_HEIGHT - 150))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (200, 102, 24), button_exit)
            self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 35))
            if mouse_click[0]:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        self.clock.tick(15)

    def lose(self):
        button_font = pygame.font.Font('resources/font.ttf', 72)
        render = self.font_win.render('You have lost ...', True, (68, 164, 104))
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, BLACK, rect)
        exit = button_font.render('EXIT', True, pygame.Color((68, 164, 104)))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200
        pygame.draw.rect(self.screen, (68, 164, 104), button_exit, width=10)
        self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 35))
        self.screen.blit(render, (HALF_WIDTH - 300, HALF_HEIGHT - 150))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (200, 102, 24), button_exit)
            self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 35))
            if mouse_click[0]:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        self.clock.tick(15)

    def showFps(self, clock):
        fps_counter = str(int(clock.get_fps()))
        text_render = self.font.render(fps_counter, False, YELLOW)
        self.screen.blit(text_render, FPS_POS)

    def showHP(self, player_hp):
        display_text = '> ' + str(int(player_hp)) + ' <'
        text_render = self.font.render(display_text, False, RED)
        self.screen.blit(text_render, HP_POS)

    def showEnemies(self, enemies):
        display_text = 'ENEMIES: ' + str(int(enemies))
        text_render = self.font2.render(display_text, False, WHITE)
        self.screen.blit(text_render, ENEMIES_POS)

    def damage(self):
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(15)
        s.fill((255, 0, 0))
        self.screen.blit(s, (0, 0))

    def background(self, player_pos):
        x = player_pos[0] / TILE_SIZE
        y = player_pos[1] / TILE_SIZE
        if y > 44 and x < 42:
            pygame.draw.rect(self.screen, SKY, (0, 0, WIDTH, HALF_HEIGHT))  # небо
            pygame.draw.rect(self.screen, FLOOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))  # пол
        else:
            pygame.draw.rect(self.screen, SKY2, (0, 0, WIDTH, HALF_HEIGHT))  # небо
            pygame.draw.rect(self.screen, FLOOR2, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))  # пол

    def vision(self, objects):
        for obj in sorted(objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)

    def mini_map(self):
        self.minimap.fill(GRAY)
        for tile_x, tile_y in minimap_map:
            pygame.draw.rect(self.minimap, GREEN, (tile_x, tile_y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.minimap, MAP_POS)

    def weapon(self):
        if self.player.shot:
            if not self.shot_sound_length_count:
                self.shot_sound.play()
            shot_sprite = self.weapon_animation[0]
            self.screen.blit(shot_sprite, self.weapon_position)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_sound_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_animation_count == 1:
                self.shot_sound_length_count += 1
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.shot_sound_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.screen.blit(self.weapon_base, self.weapon_position)

    def crosshair(self):
        pygame.draw.circle(self.screen, LIGHT_GREEN, (HALF_WIDTH, HALF_HEIGHT), 2)
