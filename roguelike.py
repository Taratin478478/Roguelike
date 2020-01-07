import os
from pprint import pprint

import pygame
from random import shuffle, randint

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60
level_names = ['room1', 'room2', 'room3', 'room4', 'room5', 'room6', 'room7', 'room8', 'room9',
               'room10']
player = None


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


class Hole(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, hole_group)
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


def reset_groups():
    global tiles_group, player_group, walls_group, all_sprites, hole_group
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    hole_group = pygame.sprite.Group()


floor = 0
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
hole_group = pygame.sprite.Group()
in_game = False
tile_images = {'wall': load_image('images\\wall.png'),
               'empty': load_image('images\\floor.png'),
               'hole': load_image('images\\hole.png')}
tile_width = 64
tile_height = 64
mw = 15
mh = 15


def load_level(level):
    with open('data/levels/' + level, 'r') as mapFile:
        level_map = [list(line.strip()) for line in mapFile]
    return list(level_map)


def draw_room(level, i, j, t):
    global player
    if t == 'room':
        ax = 0
        ay = 0
    elif t == 'hor':
        ax = 15
        ay = 5
    else:
        ax = 5
        ay = 15
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[x][y] == '.':
                Tile('empty', x + j * 20 + ax, y + i * 20 + ay)
            elif level[x][y] == '#':
                Wall('wall', x + j * 20 + ax, y + i * 20 + ay)
            elif level[x][y] == '@':
                Tile('empty', x + j * 20, y + i * 20)
                player = Player(x + j * 20, y + i * 20)
            elif level[x][y] == '$':
                Hole('hole', x + j * 20, y + i * 20)



def draw_level():
    names = level_names
    shuffle(names)
    k = randint(3, 7) + 1
    names = names[:k]
    level_map = []
    for i in range(9):
        level_map.append([''] * 9)
    level_map[3][3] = 'start'
    names.append('end')
    n = 0
    while n <= k:
        x, y = randint(1, 7), randint(1, 7)
        if (level_map[y + 1][x] != '' or level_map[y - 1][x] != '' or level_map[y][x + 1] != '' or
            level_map[y][x - 1] != '') and level_map[y][x] == '':
            level_map[y][x] = names[n]
            n += 1
    for i in range(len(level_map)):
        for j in range(len(level_map[0])):
            if level_map[i][j] != '':
                level_map[i][j] = load_level(level_map[i][j] + '.txt')
    hor = load_level('hor_corridor.txt')
    vert = load_level('vert_corridor.txt')
    for i in range(len(level_map)):
        for j in range(len(level_map[0])):
            if level_map[i][j] != '':
                level = level_map[i][j]
                if level_map[i + 1][j] != '':
                    level[6][14] = '.'
                    level[7][14] = '.'
                    level[8][14] = '.'
                    draw_room(hor, i, j, 'vert')
                if level_map[i - 1][j] != '':
                    level[6][0] = '.'
                    level[7][0] = '.'
                    level[8][0] = '.'
                if level_map[i][j + 1] != '':
                    level[14][6] = '.'
                    level[14][7] = '.'
                    level[14][8] = '.'
                    draw_room(vert, i, j, 'hor')
                if level_map[i][j - 1] != '':
                    level[0][6] = '.'
                    level[0][7] = '.'
                    level[0][8] = '.'
                draw_room(level, i, j, 'room')
    pprint(level_map)


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


def generate_map():
    global floor
    reset_groups()
    draw_level()
    floor += 1

def run_game():
    global screen, in_game
    camera = Camera()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    generate_map()
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
                if pygame.sprite.spritecollideany(player, hole_group):
                    generate_map()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        font = pygame.font.Font(None, 55)
        clock.tick(fps)
        screen.fill(pygame.Color('black'))
        tiles_group.draw(screen)
        screen.blit(font.render("Этаж " + str(floor), 1, pygame.Color('red')),
                    (1730, 20))
        player_group.draw(screen)
        pygame.display.flip()


menu = Menu()
while in_game or menu.in_menu:
    if in_game:
        run_game()
    if menu.in_menu:
        menu.run_menu()
