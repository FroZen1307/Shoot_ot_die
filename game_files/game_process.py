import pygame


def drawing_platforms():
    map = ['----------------',
           '-              -',
           '-              -',
           '-----       ----',
           '-              -',
           '-     -----    -',
           '-              -',
           '----------------']

    x = y = 0  # координаты
    for row in map:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Land(x, y)
                all_sprites.add(pf)
                platforms.append(pf)

            x += 50  # блоки платформы ставятся на ширине блоков
        y += 50  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля


class PlayerOne(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(player_sprites)
        self.trigger = 0
        self.frames = []
        self.cur_frame = 8
        self.cut_sheet()
        self.image = pygame.Surface((48, 48))
        self.image.fill(pygame.Color(pygame.color.Color('black')))
        #self.image = pygame.transform.scale(self.frames[self.cur_frame], (100, 100))
        self.position = [50, 200]
        self.rect = pygame.Rect(50, 200, 48, 48)
        self.last_dir = 'right'
        self.yvel = 0
        self.onGround = False
        self.xvel = 0
        self.MOVE_SPEED = 5
        self.JUMP_POWER = 15
        self.GRAVITY = 0.35

    def cut_sheet(self):
        sheet = pygame.image.load('sprites\\Adventure_Character_Simple.png')
        self.rect = pygame.Rect(0, 0, sheet.get_width() // 8,
                                sheet.get_height() // 20)

        for j in range(20):
            for w in range(8):
                frame_location = (self.rect.w * w, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

        self.onGround = False  # На земле ли я?

    def update(self, platforms):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -self.JUMP_POWER

        if key[pygame.K_a]:
            self.last_dir = 'left'
            self.xvel = self.MOVE_SPEED * -1  # Лево = x- n
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
            #self.image = pygame.transform.flip(pygame.transform.scale(self.frames[self.cur_frame], (130, 130)), True,
                                              # False)

        if key[pygame.K_d]:
            self.last_dir = 'right'
            self.xvel = self.MOVE_SPEED  # Право = x + n
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
            #self.image = pygame.transform.scale(self.frames[self.cur_frame], (130, 130))

        if not (key[pygame.K_d] or key[pygame.K_a]):
            if self.last_dir == 'right':
                self.cur_frame = 8
                #self.image = pygame.transform.scale(self.frames[self.cur_frame], (130, 130))
            else:
                self.cur_frame = 8
                #self.image = pygame.transform.flip(pygame.transform.scale(self.frames[self.cur_frame], (130, 130)),
                                                   #True,
                                                   #False)
            self.xvel = 0

        if not self.onGround:
            self.yvel += self.GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверхa
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает


class Land(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color(pygame.color.Color('black')))
        self.image = pygame.transform.scale(pygame.image.load('sprites\\platforms.png'), (50, 50))
        self.rect = pygame.Rect(x, y, 50, 50)


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
    platforms = []
    drawing_platforms()

    field = Field(screen)
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

        player_one.update(all_sprites)
        fps_timer = pygame.time.Clock()
        # fps_timer.tick(60)
    pygame.quit()
