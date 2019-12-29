import os
import pygame

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60


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
    def __init__(self, tile_type, pos_x, pos_y, game):
        super().__init__(game.tiles_group, game.all_sprites)
        self.image = game.tile_images[tile_type]
        self.rect = self.image.get_rect().move(game.tile_width * pos_x,
                                               game.tile_height * pos_y)


class Game:
    def __init__(self):
        self.in_game = False
        self.tiles_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.tile_images = {'wall': load_image('images\\wall.png'),
                            'empty': load_image('images\\floor.png')}
        self.tile_width = 64
        self.tile_height = 64

    def load_level(self):
        with open('data/levels/basic.txt', 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def draw_level(self):
        level = self.load_level()
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y, self)
                elif level[y][x] == '#':
                    Tile('wall', x, y, self)
                elif level[y][x] == '@':
                    Tile('empty', x, y, self)

    def run_game(self):
        global screen
        screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        self.load_level()
        self.draw_level()
        while self.in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.in_game = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            clock.tick(fps)
            screen.fill(pygame.Color('black'))
            self.all_sprites.draw(screen)
            pygame.display.flip()


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
                            game.in_game = True
            clock.tick(fps)
            pygame.display.flip()


game = Game()
menu = Menu()
while game.in_game or menu.in_menu:
    if game.in_game:
        game.run_game()
    if menu.in_menu:
        menu.run_menu()
