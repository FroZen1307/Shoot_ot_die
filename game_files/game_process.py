import pygame


class PlayerOne(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(player_sprites)
        self.trigger = 0
        self.frames = []
        self.cur_frame = 8
        self.cut_sheet()
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (130, 130))
        self.position = [350, 0]
        self.rect = self.rect.move(self.position)
        self.last_dir = 'right'
        self.allow = 1
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self):
        sheet = pygame.image.load('sprites\\Adventure_Character_Simple.png')
        self.rect = pygame.Rect(0, 0, sheet.get_width() // 8,
                                sheet.get_height() // 20)

        for j in range(20):
            for w in range(8):
                frame_location = (self.rect.w * w, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def moving(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d] and self.rect.x < 719:
            self.last_dir = 'right'
            if self.trigger == 0:
                if self.cur_frame == 8:
                    self.cur_frame = 16
                elif self.cur_frame == 21:
                    self.cur_frame = 16
                else:
                    self.cur_frame += 1
                self.trigger = 4
            else:
                self.trigger -= 1
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (130, 130))
            self.rect.x += 5
        elif key[pygame.K_a] and self.rect.x > -40:
            self.last_dir = 'left'
            if self.trigger == 0:
                if self.cur_frame == 8:
                    self.cur_frame = 16
                elif self.cur_frame == 21:
                    self.cur_frame = 16
                else:
                    self.cur_frame += 1
                self.trigger = 4
            else:
                self.trigger -= 1
            self.image = pygame.transform.flip(pygame.transform.scale(self.frames[self.cur_frame], (130, 130)), True,
                                               False)
            self.rect.x -= 5
        else:
            if self.last_dir == 'right':
                self.cur_frame = 8
                self.image = pygame.transform.scale(self.frames[self.cur_frame], (130, 130))
            else:
                self.cur_frame = 8
                self.image = pygame.transform.flip(pygame.transform.scale(self.frames[self.cur_frame], (130, 130)),
                                                   True,
                                                   False)

    def jump(self):
        if pygame.key.get_pressed()[pygame.K_w] and self.allow == 1:
            jump_power = 100
            if jump_power > 0:
                self.rect.y -= jump_power
                jump_power -= 1
            self.allow = 0

    def gravity(self):
        if self.rect.y < 10 and (50 < self.rect.x < 300 or 500 < self.rect.x < 750):
            self.rect.y += 5
        elif self.rect.y < 135 and 300 < self.rect.x < 500:
            self.rect.y += 5
        elif (self.rect.y < 260 and (self.rect.x < 50 or 750 < self.rect.x)) or (
                60 < self.rect.y < 260 and (50 < self.rect.x < 300 or 500 < self.rect.x < 750)) or (
                285 < self.rect.y < 260 and 300 < self.rect.x < 500):
            self.rect.y += 5
        else:
            self.allow = 1


class Land(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(all_sprites)
        self.image = pygame.image.load('sprites\\platforms.png')
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.mask = pygame.mask.from_surface(self.image)


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
    player_sprites = pygame.sprite.Group()
    pygame.display.set_caption('Shoot or die')
    land_mask = pygame.mask.from_surface(pygame.image.load('sprites\\platforms.png'))

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
    player_sprites.draw(screen)
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
                player_sprites.draw(screen)
                pygame.display.flip()
            else:
                field.frame = 0
                field.bg = pygame.image.load("BG_frames\\Frame_" + str(field.frame) + ".gif").convert_alpha()
                field.bg = pygame.transform.scale(field.bg, (800, 400))
                field.screen.blit(field.bg, (0, 0))
                all_sprites.draw(field.screen)
                player_sprites.draw(screen)
                pygame.display.flip()

        player_one.gravity()
        player_one.jump()
        player_one.moving()
    pygame.quit()
