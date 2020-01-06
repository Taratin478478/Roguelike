import os
import pygame
from PIL import Image

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60


def mirror():
    i = Image.open('data\\images\\player.png')
    i.transpose(Image.FLIP_LEFT_RIGHT).save('data\\images\\player.png')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, walls_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x = obj.rect.x + self.dx
        obj.rect.y = obj.rect.y + self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 1920 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 1080 // 2)


in_game = False
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tile_images = {'wall': load_image('images\\wall.png'),
               'empty': load_image('images\\floor.png')}
tile_width = 64
tile_height = 64
mw = 15
mh = 15


def load_level():
    with open('data/levels/basic.txt', 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def draw_level():
    global player
    level = load_level()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Wall('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y, )
                player = Player(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        pygame.key.set_repeat(10, 1)
        self.image = load_image('images\\player.png', -1)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.hor_direction = 'right'
        self.vert_direction = 'down'
        self.walk_cycle = 0

    def move(self, dir, n):
        self.rect[dir] += 5 * n


class Menu:
    def __init__(self):
        self.in_menu = True
        self.draw_menu()
        self.run_menu()

    def draw_menu(self):
        screen.fill(pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color('red'),
                         (width // 4, height // 3, width // 2, height // 12), 1)
        pygame.draw.rect(screen, pygame.Color('red'),
                         (width // 4, height // 24 * 11, width // 2,
                          height // 12),
                         1)
        pygame.draw.rect(screen, pygame.Color('red'),
                         (width // 4, height // 12 * 7, width // 2,
                          height // 12),
                         1)
        pygame.draw.rect(screen, pygame.Color('red'),
                         (width // 4, height // 24 * 17, width // 2,
                          height // 12),
                         1)
        font = pygame.font.Font(None, 113)
        screen.blit(font.render("Something", 1, pygame.Color('red')),
                    (width // 4, 100))
        font = pygame.font.Font(None, 55)
        screen.blit(font.render("Играть", 1, pygame.Color('red')),
                    (width // 3 + 70, height // 3 + 5))
        screen.blit(font.render("Магазин", 1, pygame.Color('red')),
                    (width // 3 + 57, height // 24 * 11 + 5))
        screen.blit(font.render("Достижения", 1, pygame.Color('red')),
                    (width // 3 + 20, height // 12 * 7 + 5))
        screen.blit(font.render("Выход", 1, pygame.Color('red')),
                    (width // 3 + 70, height // 24 * 17 + 5))

    def run_menu(self):
        global in_game
        while self.in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.in_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] in range(width // 4, width // 4 * 3):
                        if event.pos[1] in range(height // 24 * 17,
                                                 height // 24 * 19):
                            self.in_menu = False
                        elif event.pos[1] in range(height // 3,
                                                   height // 12 * 5):
                            self.in_menu = False
                            in_game = True
            clock.tick(fps)
            pygame.display.flip()


def run_game():
    global screen, in_game
    camera = Camera()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    load_level()
    draw_level()
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move(0, 1)
                    if pygame.sprite.spritecollideany(player, walls_group):
                        player.move(0, -1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player.png', -1)
                    else:
                        player.image = load_image('images\\player_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.hor_direction = 'right'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move(0, -1)
                    if pygame.sprite.spritecollideany(player, walls_group):
                        player.move(0, 1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_left.png', -1)
                    else:
                        player.image = load_image('images\\player_left_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.hor_direction = 'left'
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.move(1, -1)
                    if pygame.sprite.spritecollideany(player, walls_group):
                        player.move(1, 1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_back.png', -1)
                    else:
                        player.image = load_image('images\\player_back_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.vert_direction = 'up'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.move(1, 1)
                    if pygame.sprite.spritecollideany(player, walls_group):
                        player.move(1, -1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_front.png', -1)
                    else:
                        player.image = load_image('images\\player_front_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.vert_direction = 'down'
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        clock.tick(fps)
        screen.fill(pygame.Color('black'))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()


menu = Menu()
while in_game or menu.in_menu:
    if in_game:
        run_game()
    if menu.in_menu:
        menu.run_menu()
