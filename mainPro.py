import pygame as pg
import sys
from PIL import Image


def load_image(name, colorkey=None):
    image = pg.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pg.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret


# функция для написания правил
def write_rules(screen):
    rules = ['Задача каждого из игроков - убить другого игрока',
             'Используйте оружие дальнего и ближнего боя, передвигайтесь, прыгайте',
             'Управление для первого игрока: W - прыгать, A - идти влево, D - идти вправо,',
             'F - бить (ближним оружием), G - стрелять (дальним оружием)',
             'Управление для второго игрока: стрелка вверх - прыгать, cтрелка "<" - идти влево, стрелка ">" -',
             '- идти вправо, ,(Б) - бить (ближним оружием), .(Ю) - стрелять (дальним оружием)',
             'У игроков по 3 жизни, один выстрел (попавший в игрока) отнимает одну жизнь!']
    coords = [50, 60]
    font = pg.font.Font(None, 20)
    for i in range(len(rules)):
        if i == len(rules) - 3:
            text = font.render(rules[i], True, (0, 0, 0))
            screen.blit(text, coords)
            coords[1] += 50
            # сдвигаем по иксу, чтобы кнопка 'Back' не мешала
            coords[0] += 155
        else:
            text = font.render(rules[i], True, (0, 0, 0))
            screen.blit(text, coords)
            coords[1] += 50


SIZE_OF_BUTTON = (200, 100)


class Button(pg.sprite.Sprite):
    def __init__(self, sheet, rows, columns, x, y, pressed=False, *group):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.pressed = pressed

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pg.transform.scale(sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size)), SIZE_OF_BUTTON))

    def update(self):
        if not self.pressed:
            self.image = self.frames[0]
        elif self.pressed and len(self.frames) > 1:
            self.image = self.frames[1]

    def button_rect(self):
        return pg.Rect(self.rect[0], self.rect[1], SIZE_OF_BUTTON[0], SIZE_OF_BUTTON[1])

    def terminate(self):
        pg.quit()
        sys.exit()


# стартовый экран

class StartScreen:

    def __init__(self, screen):
        self.fon = split_animated_gif('fon_of_game.gif')
        self.screen = screen

    def renew(self, k):
        image = pg.transform.scale(self.fon[k], (width, height))
        self.screen.blit(image, (0, 0))

    def len_of_cadrs(self):
        return len(self.fon) - 1


# экран для ввода ников (второй экран)

class NicknamesScreen:
    def __init__(self, screen):
        global gif2
        self.first_nick = ''
        self.second_nick = ''
        self.screen = screen
        # фон экрана для ввода ников
        self.second_screen_fon = gif2
        # текущий кадр гиф-картинки
        self.cur_cadr = 0

    # обновляем гиф-картинку второго экрана
    def renew(self):
        image = pg.transform.scale(self.second_screen_fon[self.cur_cadr], (width, height))
        self.screen.blit(image, (0, 0))
        if self.cur_cadr == len(self.second_screen_fon) - 1:
            self.cur_cadr = 0
        else:
            self.cur_cadr += 1


class InputBox:
    def __init__(self, color, x, y, width, height, screen, user=1):
        self.screen = screen
        self.x, self.y, self.width, self.height = x, y, width, height
        pg.draw.rect(self.screen, color, (x, y, width, height), 0)
        font = pg.font.Font(None, 35)
        text = font.render(f"пользователь {user}", True, (71, 116, 194))
        screen.blit(text, (x, y - 30))

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)


if __name__ == '__main__':
    # заранее загружаем фон второго экрана
    gif2 = split_animated_gif('fon_of_second_screen.gif')
    pg.init()
    size = width, height = 800, 400
    screen = pg.display.set_mode(size)

    pressed_start = False
    running = -1
    fps = 10
    clock = pg.time.Clock()
    x_pos = 0
    v = 10  # п
    all_sprites = pg.sprite.Group()
    sprite_home = pg.sprite.Group()
    # спрайты кнопки 'play'
    # спрайты кнопок 'exit'
    second_page_sprite_group = pg.sprite.Group()
    start_screen = StartScreen(screen)
    nicknames_screen = NicknamesScreen(screen)
    # кнопка 'play'
    button_play = Button(load_image('buttons_start.png', -1), 1, 2, width // 2 - 100, height // 2 - 100, False, all_sprites)
    # кнопка 'exit'
    button_exit = Button(load_image('exit.png', -1), 1, 1, width // 2 - 100, height - 200, False, all_sprites)
    # текущий кадр гиф-картинки заднего фона
    button_rules = Button(load_image('button_rules.png', -1), 1, 1, width // 2 - 100, height // 2 + 105, False, all_sprites)
    button_home = Button(load_image('Back.png', -1), 1, 1, 0, height // 2 + 100, False, sprite_home)
    cur_cadr_of_gif = 0
    pressed_start = False
    image_2 = load_image('name.png', (255, 255, 255))
    pg.mixer.music.load("music.mp3")
    pg.mixer.music.play(-1)
    image_rules = pg.transform.scale(load_image('rules_fon.jpg'), (width, height))

    while running:
        # задний фон - гиф-картинка, поэтому она должна обновляться
        start_screen.renew(cur_cadr_of_gif)
        screen.blit(image_2, (20, 20))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 1
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_play.button_rect().collidepoint(pg.mouse.get_pos()):
                    button_play = Button(load_image('buttons_start.png', -1), 1, 2, width // 2 - 100, height // 2 - 100, True, all_sprites)
                    pressed_start = True
                    running = 2
                elif button_exit.button_rect().collidepoint(pg.mouse.get_pos()):
                    button_exit.terminate()
                else:
                    pressed_start = False
                if button_rules.button_rect().collidepoint(pg.mouse.get_pos()):
                    running_rules = 1
                    while running_rules:
                        for ev in pg.event.get():
                            if ev.type == pg.QUIT:
                                running_rules = 0
                            elif ev.type == pg.MOUSEBUTTONDOWN:
                                if button_home.button_rect().collidepoint(pg.mouse.get_pos()):
                                    running_rules = 0
                        screen.blit(image_rules, (0, 0))
                        write_rules(screen)
                        sprite_home.draw(screen)
                        pg.display.flip()
                        clock.tick(fps)
        # если пользователь нажал на кнопку 'play', то она должна нажаться

        all_sprites.update()
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(fps)
        running -= 1
        # задний фон - гиф-картинка, поэтому она должна обновляться
        cur_cadr_of_gif = (cur_cadr_of_gif + 1) % start_screen.len_of_cadrs()
    if pressed_start:
        running = -1
    # ники
    txt1 = ''
    txt2 = ''
    font = pg.font.Font(None, 50)
    text = font.render("введите ник!", True, (85, 137, 230))
    # флажки, которые показывают, в в каком прямоугольнике мы печатаем
    first = False
    second = False
    shift = False
    while running:
        nicknames_screen.renew()
        screen.blit(text, (width // 2 - text.get_width() // 2, 20))
        first_box = InputBox((176, 172, 173), 50, 90, 250, 35, screen)
        second_box = InputBox((176, 172, 173), 500, 90, 250, 35, screen, 2)
        nick1 = font.render(txt1, True, (168, 224, 229))
        screen.blit(nick1, (53, 90))
        nick2 = font.render(txt2, True, (168, 224, 229))
        screen.blit(nick2, (503, 90))
        button_start = Button(load_image('second_start.png', -1), 1, 1, width - 200, height - 100, False, second_page_sprite_group)
        second_page_sprite_group.update()
        second_page_sprite_group.draw(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 1
            elif event.type == pg.MOUSEBUTTONDOWN:
                if first_box.get_rect().collidepoint(pg.mouse.get_pos()):
                    first = True
                    second = False
                elif second_box.get_rect().collidepoint(pg.mouse.get_pos()):
                    second = True
                    first = False
                #  если пользователь нажали на кнопку 'start'
                elif button_start.button_rect().collidepoint(pg.mouse.get_pos()):
                    pass
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_LSHIFT, pg.K_RSHIFT]:
                    shift = True
                elif event.key == pg.K_BACKSPACE:
                    if first and len(txt1) >= 1:
                        txt1 = txt1[:-1]
                    elif second and len(txt2) >= 1:
                        txt2 = txt2[:-1]
                else:
                    for i in range(26):
                        if event.key == getattr(pg, 'K_' + chr(ord('a') + i)):
                            if shift:
                                letter = chr(ord('a') + i).upper()
                            else:
                                letter = chr(ord('a') + i)
                            if first and len(txt1) <= 11:
                                txt1 += letter
                            elif second and len(txt2) <= 11:
                                txt2 += letter
            elif event.type == pg.KEYUP:
                if event.key in [pg.K_LSHIFT, pg.K_RSHIFT]:
                    shift = False
        pg.display.flip()
        clock.tick(fps)
        running -= 1
