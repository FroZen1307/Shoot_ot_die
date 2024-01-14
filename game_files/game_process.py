import pygame


class PlayerOne(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet()
        self.image = pygame.transform.scale(self.frames[0], (130, 130))
        self.position = (50, 260)
        self.rect = self.rect.move(self.position)

    def cut_sheet(self):
        sheet = pygame.image.load('sprites\\Adventure_Character_Simple.png')
        self.rect = pygame.Rect(0, 0, sheet.get_width() // 8,
                                sheet.get_height() // 20)

        for j in range(20):
            for i in range(8):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def running_left(self):
        pass


class Land(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(all_sprites)
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
    all_sprites = pygame.sprite.Group()

    field = Field(screen)
    for i in range(0, 800, 50):
        Land(i, 350)
    for k in range(50, 300, 50):
        Land(k, 100)
    for g in range(300, 500, 50):
        Land(g, 225)
    for m in range(500, 750, 50):
        Land(m, 100)
    player_one = PlayerOne()

    all_sprites.draw(field.screen)
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
                all_sprites.draw(field.screen)
                pygame.display.flip()
            else:
                field.frame = 0
                field.bg = pygame.image.load("BG_frames\\Frame_" + str(field.frame) + ".gif").convert_alpha()
                field.bg = pygame.transform.scale(field.bg, (800, 400))
                field.screen.blit(field.bg, (0, 0))
                all_sprites.draw(field.screen)
                pygame.display.flip()
    pygame.quit()
