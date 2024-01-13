import pygame


class Land(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(lands_sprites)
        self.image = pygame.image.load('sprites\\platforms.png')
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height


class Field:

    def __init__(self, main_screen):
        self.screen = main_screen
        self.frame = 0
        self.bg = pygame.image.load("BG_frames\\Frame_" + str(self.frame) + ".gif").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (800, 400))
        screen.blit(self.bg, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    lands_sprites = pygame.sprite.Group()

    field = Field(screen)
    for i in range(0, 800, 50):
        Land(i, 350)

    lands_sprites.draw(field.screen)
    pygame.display.flip()
    bg_changer = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if bg_changer.tick() % 2 == 0:
            if field.frame != 534:
                field.frame += 1
                field.bg = pygame.image.load("BG_frames\\Frame_" + str(field.frame) + ".gif").convert_alpha()
                field.bg = pygame.transform.scale(field.bg, (800, 400))
                field.screen.blit(field.bg, (0, 0))
                lands_sprites.draw(field.screen)
                pygame.display.flip()
            else:
                field.frame = 0
                field.bg = pygame.image.load("BG_frames\\Frame_" + str(field.frame) + ".gif").convert_alpha()
                field.bg = pygame.transform.scale(field.bg, (800, 400))
                field.screen.blit(field.bg, (0, 0))
                lands_sprites.draw(field.screen)
                pygame.display.flip()
    pygame.quit()
