import math
import os
import pygame
from random import shuffle, randint, uniform
from PIL import Image

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
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, walls_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class BulletStopper(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, bullet_stopper_group)
        self.rect = pygame.Rect(tile_width * pos_x, tile_height * pos_y, 64, 64)


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
        if type(obj) in [Enemy, Bullet]:
            obj.sx += self.dx
            obj.sy += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 1920 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 1080 // 2)


def reset_groups():
    global tiles_group, player_group, walls_group, all_sprites, hole_group, gun_group, bullet_group,\
        enemy_group, dead_group, bullet_stopper_group
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    hole_group = pygame.sprite.Group()
    gun_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    dead_group = pygame.sprite.Group()
    bullet_stopper_group = pygame.sprite.Group()


floor = 0
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
hole_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
dead_group = pygame.sprite.Group()
bullet_stopper_group = pygame.sprite.Group()
in_game = False
tile_images = {'wall': load_image('images\\wall.png'),
               'empty': load_image('images\\floor.png'),
               'hole': load_image('images\\hole.png')}
tile_width = 64
tile_height = 64
mw = 15
mh = 15
arrow = load_image('images\\scope.png', -1)


def load_level(level):
    with open('data/levels/' + level, 'r') as mapFile:
        level_map = [list(line.strip()) for line in mapFile]
    return list(level_map)


def draw_room(level, i, j, t):
    global player, gun
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
                gun = Pistol(x + j * 20, y + i * 20)
            elif level[x][y] == '$':
                Hole('hole', x + j * 20, y + i * 20)
            elif level[x][y] == '%':
                Tile('empty', x + j * 20, y + i * 20)
                Enemy(x + j * 20, y + i * 20)
            elif level[x][y] == ':':
                BulletStopper(x + j * 20, y + i * 20)
                Tile('empty', x + j * 20, y + i * 20)



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
    hor = load_level('hor_corridor.txt')
    vert = load_level('vert_corridor.txt')
    for i in range(len(level_map)):
        for j in range(len(level_map[0])):
            if level_map[i][j] != '':
                ea = level_map[i][j] not in ['start', 'end']
                level = load_level(level_map[i][j] + '.txt')
                ne = randint(2, 6)
                while ne > 0 and ea:
                    x = randint(1, 13)
                    y = randint(1, 13)
                    if level[x][y] == '.':
                        level[x][y] = '%'
                        ne -= 1
                symb = ':' if ea else '.'
                if level_map[i + 1][j] != '':
                    level[6][14] = symb
                    level[7][14] = symb
                    level[8][14] = symb
                    draw_room(hor, i, j, 'vert')
                if level_map[i - 1][j] != '':
                    level[6][0] = symb
                    level[7][0] = symb
                    level[8][0] = symb
                if level_map[i][j + 1] != '':
                    level[14][6] = symb
                    level[14][7] = symb
                    level[14][8] = symb
                    draw_room(vert, i, j, 'hor')
                if level_map[i][j - 1] != '':
                    level[0][6] = symb
                    level[0][7] = symb
                    level[0][8] = symb
                draw_room(level, i, j, 'room')


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = load_image('images\\slime.png', -1)
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)
        self.direction = 'right'
        self.walk_cycle = 0
        self.v = 2
        self.sx, self.sy = self.rect.center
        self.hp = 20 + 2 * (floor - 1)
        self.room = [pos_x // 20, pos_y // 20]
        self.a = 256

    def update(self):
        if self.hp > 0:
            if self.room == player.room and not player.in_corridor:
                x, y = player.rect.center
                g = ((x - self.sx) ** 2 + (self.sy - y) ** 2) ** 0.5
                if g != 0:
                    vx = (x - self.sx) / g * self.v
                    vy = (y - self.sy) / g * self.v
                else:
                    vx, vy = 0, 0
                self.sx, self.sy = self.sx + vx, self.sy + vy
                self.rect.center = (self.sx, self.sy)
                if pygame.sprite.spritecollideany(self, walls_group):
                    self.sx = self.sx - vx
                    self.rect.center = (self.sx, self.sy)
                    if pygame.sprite.spritecollideany(self, walls_group):
                        self.sx, self.sy = self.sx + vx, self.sy - vy
                        self.rect.center = (self.sx, self.sy)
                        if pygame.sprite.spritecollideany(self, walls_group):
                            self.sx = self.sx - vx
                            self.rect.center = (self.sx, self.sy)
        else:
            if self.a == 256:
                enemy_group.remove(self)
                dead_group.add(self)
            if self.a > 0:
                self.a -= 5
                self.image.set_alpha(self.a)
            else:
                self.kill()


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(x + 23, y + 6, 57, 75)
        self.left = x + 23
        self.top = y + 6
        self.right = self.left + 57
        self.bottom = self.top + 75


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        pygame.key.set_repeat(10, 1)
        self.image = load_image('images\\player.png', -1)
        self.x = tile_width * pos_x
        self.y = tile_height * pos_y
        self.direction = 'right'
        self.room = [self.x // 1280, self.y // 1280]
        self.in_corridor = False
        self.walk_cycle = 0
        self.hp = 3
        self.hitbox = Hitbox(self.x, self.y)
        self.rect = self.image.get_rect().move(self.x, self.y)

    def move(self, dir, n):
        self.rect[dir] += 5 * n
        self.hitbox.rect[dir] += 5 * n
        if dir == 0:
            self.x += 5 * n
            self.hitbox.left += 5 * n
            self.hitbox.right += 5 * n
        else:
            self.y += 5 * n
            self.hitbox.top += 5 * n
            self.hitbox.bottom += 5 * n

        self.room = [self.x // 1280, self.y // 1280]
        self.in_corridor = self.hitbox.left % 1280 > 895 or self.hitbox.top % 1280 > 895 \
                           or self.hitbox.right % 1280 < 64 or self.hitbox.bottom % 1280 < 64 or \
                           self.hitbox.left % 1280 < 64 or self.hitbox.top % 1280 < 64 or \
                           self.hitbox.right % 1280 > 895 or self.hitbox.bottom % 1280 > 895


class Gun(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(gun_group, all_sprites)
        self.normal_image = load_image('images\\pistol.png', -1)
        self.image = load_image('images\\pistol.png', -1)
        self.x = tile_width * pos_x + 75
        self.y = tile_height * pos_y + 40
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.damage = 5
        self.bv = 10

    def move(self, dir, n):
        self.rect[dir] += 5 * n

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.left, mouse_y - self.rect.top
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if angle < -90 or angle > 90:
            self.image = pygame.transform.flip(self.normal_image, True, False)
            self.image = pygame.transform.rotate(self.image, int(angle) - 180)
        else:
            self.image = pygame.transform.rotate(self.normal_image, int(angle))
        self.rect = self.image.get_rect(center=(983, 560))

    def shoot(self, pos):
        Bullet(pos[0], pos[1], self.bv, self.damage)


class Pistol(Gun):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.normal_image = load_image('images\\pistol.png', -1)
        self.image = load_image('images\\pistol.png', -1)
        self.bv = 10
        self.damage = 5


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, v, damage):
        super().__init__(bullet_group, all_sprites)
        self.x = player.rect.left + 55
        self.y = player.rect.top + 40
        x = uniform(x - x / 50, x + x / 50)
        y = uniform(y - y / 50, y + y / 50)
        rx = x - self.x
        ry = y - self.y
        g = ((x - self.x) ** 2 + (self.y - y) ** 2) ** 0.5
        self.vx = (x - self.x) / g * v
        self.vy = (y - self.y) / g * v
        self.damage = damage
        self.image = load_image('images\\pistol_bullet.png', -1)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.sx, self.sy = self.rect.center
        angle = (180 / math.pi) * math.atan2(rx, ry)
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.rotate(self.image, int(angle))

    def update(self):
        self.sx = self.sx + self.vx
        self.sy = self.sy + self.vy
        self.rect.left = self.sx
        self.rect.top = self.sy


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
    mouse_pos = (0, 0)
    camera = Camera()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    generate_map()
    pygame.mouse.set_visible(False)
    damage_timer = 0
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun.shoot(event.pos)
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                gun.rotate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move(0, 1)
                    gun.move(0, 1)
                    if pygame.sprite.spritecollideany(player.hitbox, walls_group):
                        player.move(0, -1)
                        gun.move(0, -1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player.png', -1)
                    else:
                        player.image = load_image('images\\player_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.direction = 'right'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move(0, -1)
                    gun.move(0, -1)
                    if pygame.sprite.spritecollideany(player.hitbox, walls_group):
                        player.move(0, 1)
                        gun.move(0, 1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_left.png', -1)
                    else:
                        player.image = load_image('images\\player_left_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.direction = 'left'
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.move(1, -1)
                    gun.move(1, -1)
                    if pygame.sprite.spritecollideany(player.hitbox, walls_group):
                        player.move(1, 1)
                        gun.move(1, 1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_back.png', -1)
                    else:
                        player.image = load_image('images\\player_back_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.direction = 'up'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.move(1, 1)
                    gun.move(1, 1)
                    if pygame.sprite.spritecollideany(player.hitbox, walls_group):
                        player.move(1, -1)
                        gun.move(1, -1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_front.png', -1)
                    else:
                        player.image = load_image('images\\player_front_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.direction = 'down'
                if pygame.sprite.spritecollideany(player.hitbox, hole_group):
                    hp = player.hp
                    generate_map()
                    player.hp = hp
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        font = pygame.font.Font(None, 55)
        clock.tick(fps)
        screen.fill(pygame.Color('black'))
        tiles_group.draw(screen)
        dead_group.update()
        enemy_group.update()
        bullet_group.update()
        collide = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
        for i in range(len(collide)):
            keys = list(collide.keys())
            damage = keys[i].damage
            for j in collide[keys[i]]:
                j.hp -= damage
        enemy_group.draw(screen)
        dead_group.draw(screen)
        if player.direction == 'up':
            gun_group.draw(screen)
            player_group.draw(screen)
        else:
            player_group.draw(screen)
            gun_group.draw(screen)
        pygame.sprite.groupcollide(bullet_group, walls_group, True, False)
        pygame.sprite.groupcollide(bullet_group, bullet_stopper_group, True, False)
        bullet_group.draw(screen)
        screen.blit(font.render("Этаж " + str(floor), 1, pygame.Color('red')), (1730, 20))
        if pygame.sprite.spritecollideany(player.hitbox, enemy_group) and damage_timer == 0:
            player.hp -= 1
            damage_timer = 120
        n = 20
        for i in range(player.hp):
            screen.blit(load_image('images\\heart.png', -1), (n, 20))
            n += 84
        screen.blit(arrow, mouse_pos)
        pygame.display.flip()
        if damage_timer > 0:
            damage_timer -= 1


menu = Menu()
while in_game or menu.in_menu:
    if in_game:
        run_game()
    if menu.in_menu:
        menu.run_menu()
