import pygame

def init():
    global display
    global clock

    pygame.init()
    display = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()

def loop(update=None):
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        td = clock.tick(120)
        if update:
            update(td)

        pygame.display.flip()

    pygame.quit()
