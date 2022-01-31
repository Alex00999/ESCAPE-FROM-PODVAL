from mapdata import map_width, map_height
from sprites import *
from ray_casting import ray_casting
from render import Rendering, play_theme, main_menu
from interactions import Interaction

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption('ESCAPE FROM PODVAL')
minimap = pygame.Surface((MAP_TILE * map_width, MAP_TILE * map_height))

sprites = Sprites()
clock = pygame.time.Clock()
player = Player()
render = Rendering(screen, minimap, player, clock)
main_menu(screen, clock)
pygame.mouse.set_visible(False)
interaction = Interaction(player, sprites, render)

play_theme()


while True:
    if player.hp < 1:
        pygame.mouse.set_visible(True)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resources/sound/loss.mp3')
        pygame.mixer.music.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            render.lose()
    player.movement()
    render.background(player.pos)
    walls = ray_casting(player, render.textures)
    render.vision(walls + [obj.sprite_locate(player, walls) for obj in sprites.sprite_list])
    render.weapon()
    interaction.interaction_objects()
    interaction.npc_action()
    render.mini_map()
    # print(player.pos[0] / 64, player.pos[1] / 64)
    render.showFps(clock)
    render.showHP(player.hp)
    render.crosshair()
    interaction.check_win()

    pygame.display.flip()
    clock.tick(FPS)
