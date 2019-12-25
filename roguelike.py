import pygame

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
fps = 60
clock = pygame.time.Clock()


def draw_menu():
    pygame.draw.rect(screen, pygame.Color('red'),
                     (width // 4, height // 3, width // 2, height // 12), 1)
    pygame.draw.rect(screen, pygame.Color('red'),
                     (width // 4, height // 24 * 11, width // 2, height // 12),
                     1)
    pygame.draw.rect(screen, pygame.Color('red'),
                     (width // 4, height // 12 * 7, width // 2, height // 12),
                     1)
    pygame.draw.rect(screen, pygame.Color('red'),
                     (width // 4, height // 24 * 17, width // 2, height // 12),
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
                (width // 3 + 75, height // 24 * 17 + 5))


screen.fill(pygame.Color('black'))
draw_menu()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    clock.tick(fps)
    pygame.display.flip()
