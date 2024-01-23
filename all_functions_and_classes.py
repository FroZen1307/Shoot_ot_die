import pygame as pg
import sys
from PIL import Image


size = width, height = 800, 400


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

# класс кнопки


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
# заранее загружаем фон второго экрана, чтоб не тратить на это энергию в будущем
gif2 = split_animated_gif('fon_of_second_screen.gif')

# экран для ввода ников


class NicknamesScreen:
    def __init__(self, screen):
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

# класс для поля ввода ников


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


# заранее загружаем фон экрана победителя, чтобы потом не тратить на это энергию
gif3 = split_animated_gif('fon_of_winner.gif')
# экран ввода ников


class WinnerScreen:
    def __init__(self, screen):
        self.screen = screen
        # фон экрана для ввода ников
        self.winner_screen_fon = gif3
        # текущий кадр гиф-картинки
        self.cur_cadr = 0

    # обновляем гиф-картинку экрана
    def renew(self):
        image = pg.transform.scale(self.winner_screen_fon[self.cur_cadr], (width, height))
        self.screen.blit(image, (0, 0))
        if self.cur_cadr == len(self.winner_screen_fon) - 1:
            self.cur_cadr = 0
        else:
            self.cur_cadr += 1


# Функция, которая открывает главный экран!!!


def MainScr():
    pg.init()
    size = width, height = 800, 400
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Shoot or die')

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
    # кнопка 'play', которая преносит на экран ввода ников
    button_play = Button(load_image('buttons_start.png', -1), 1, 2, width // 2 - 100, height // 2 - 100, False, all_sprites)
    # кнопка 'exit'
    button_exit = Button(load_image('exit.png', -1), 1, 1, width // 2 - 100, height - 200, False, all_sprites)
    # текущий кадр гиф-картинки заднего фона
    button_rules = Button(load_image('button_rules.png', -1), 1, 1, width // 2 - 100, height // 2 + 105, False, all_sprites)
    button_home = Button(load_image('Back.png', -1), 1, 1, 0, height // 2 + 100, False, sprite_home)
    cur_cadr_of_gif = 0
    # нажал ли пользователь на кнопку 'PLAY'
    pressed_start = False
    # красочное название игры
    image_2 = load_image('name.png', (255, 255, 255))
    pg.mixer.music.load("music.mp3")
    pg.mixer.music.play(-1)
    image_rules = pg.transform.scale(load_image('rules_fon.jpg'), (width, height))
    # есть ли проблема при вводе ников на втором экране
    trouble = False

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
                    # стираем все ники перед началом новой игры
                    f = open('results.txt', 'r+')
                    f.truncate(0)  # need '0' when using r+
                elif button_exit.button_rect().collidepoint(pg.mouse.get_pos()):
                    button_exit.terminate()
                else:
                    pressed_start = False
                # если нажали на кнопку 'Правила', то открываем экран с правилами
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
    # запускаем новый цикл (в будущем)
    if pressed_start:
        running = -1
    # ники по умолчанию
    nick1 = 'Player1'
    nick2 = 'Player2'
    font = pg.font.Font(None, 50)
    text = font.render("введите ник", True, (85, 137, 230))
    # флажки, которые показывают, в в каком прямоугольнике мы печатаем
    first = False
    second = False
    shift = False
    # вот и новый цикл (цикл экрана ввода ников)
    while running:
        font = pg.font.Font(None, 50)
        nicknames_screen.renew()
        screen.blit(text, (width // 2 - text.get_width() // 2, 20))
        # прямоугольники для ввода ников в них
        first_box = InputBox((176, 172, 173), 50, 90, 290, 35, screen)
        second_box = InputBox((176, 172, 173), 500, 90, 290, 35, screen, 2)
        txt1 = font.render(nick1, True, (168, 224, 229))
        screen.blit(txt1, (53, 90))
        txt2 = font.render(nick2, True, (168, 224, 229))
        screen.blit(txt2, (503, 90))
        button_start = Button(load_image('second_start.png', -1), 1, 1, width - 200, height - 100, False, second_page_sprite_group)
        # кнопка выйти домой на втором экране
        second_button_home = Button(load_image('Back.png', -1), 1, 1, 0, height // 2 + 100, False, second_page_sprite_group)
        second_page_sprite_group.update()
        second_page_sprite_group.draw(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 1
            elif event.type == pg.MOUSEBUTTONDOWN:
                if first_box.get_rect().collidepoint(pg.mouse.get_pos()):
                    # обновляем ники если пользователь начнёт их вводить
                    if nick1 == 'Player1':
                        nick1 = ''
                    first = True
                    second = False
                elif second_box.get_rect().collidepoint(pg.mouse.get_pos()):
                    # обновляем ники если пользователь начнёт их вводить
                    if nick2 == 'Player2':
                        nick2 = ''
                    second = True
                    first = False
                #  если пользователь нажали на кнопку 'start'\
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                elif button_start.button_rect().collidepoint(pg.mouse.get_pos()):
                    # ники по умолчанию, если пользователь ничего не ввёл
                    if nick1 == '':
                        nick1 = 'Player1'
                    if nick2 == '':
                        nick2 = 'Player2'
                    # если ники одинаковы
                    if nick1 == nick2:
                        trouble = True
                    else:
                        trouble = False
                    if not trouble:
                        # записываем ники игроков в файл перед началом игры
                        with open('results.txt', 'w', encoding='utf-8') as statistic:
                            statistic.write(f'{nick1} {nick2}')
                    # начинаем игру
                    running = 1
                    last_screen()
                # если пользователь нажал на кнопку 'Back', то возвращаемся на главный экран
                elif second_button_home.button_rect().collidepoint(pg.mouse.get_pos()):
                    running = 1
                    MainScr()
            elif event.type == pg.KEYDOWN:
                # схема, как вводятся ники
                if event.key in [pg.K_LSHIFT, pg.K_RSHIFT]:
                    shift = True
                elif event.key == pg.K_BACKSPACE:
                    if first and len(nick1) >= 1:
                        nick1 = nick1[:-1]
                    elif second and len(nick2) >= 1:
                        nick2 = nick2[:-1]
                else:
                    for i in range(26):
                        if event.key == getattr(pg, 'K_' + chr(ord('a') + i)):
                            if shift:
                                letter = chr(ord('a') + i).upper()
                            else:
                                letter = chr(ord('a') + i)
                            if first and len(nick1) <= 11:
                                nick1 += letter
                            elif second and len(nick2) <= 11:
                                nick2 += letter
            elif event.type == pg.KEYUP:
                if event.key in [pg.K_LSHIFT, pg.K_RSHIFT]:
                    shift = False
        # если ники одинаковы
        if trouble:
            font = pg.font.Font(None, 30)
            warning = font.render('введите, пожалуйста, разные ники', True, (217, 26, 33))
            screen.blit(warning, (width // 2 - 200, height - 50))
        pg.display.flip()
        clock.tick(fps)
        running -= 1


# функция, запускающая последний экран (экран объявления победителя)


def last_screen():
    pg.init()
    running = 1
    size = width, height = 800, 400
    screen = pg.display.set_mode(size)
    winner_screen = WinnerScreen(screen)
    clock = pg.time.Clock()
    fps = 50
    image = pg.transform.scale(load_image('winner.png', -1), (300, 150))
    corona = pg.transform.scale(load_image('corona_real.jpg', -1), (150, 115))
    font = pg.font.Font(None, 50)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    winner = []
    text = font.render(f"'ник победителя'", True, (161, 26, 101))
    # корона победителя должна появляться и исчезать, чтобы было эффектнее, поэтому задаём таймер
    timer = 0
    # корона должна появляться на 1 секунду, мы ставим флажок
    flag = False
    # секунды, на которые появляется корона
    seconds = 0
    # нажал ли игрок кнопку 'QUIT' (чтоб выйти на главный экран)
    return_home = False
    pg.mixer.music.load("winner_music.mp3")
    pg.mixer.music.play(-1)
    # группа спрайтов для последнего экрана
    last_screen_buttons_group = pg.sprite.Group()
    home_button = Button(load_image('quit.png', -1), 1, 1,
                         width // 2 - 350, height // 2 + 50, False, last_screen_buttons_group)
    sprite_home = pg.sprite.Group()
    # кнопка статистики
    font = pg.font.Font(None, 30)
    text_stat = font.render("статистика", True, (237, 54, 186))
    button_stats = Button(load_image('button_stat.png', -1), 1, 1, width // 2 - 350, height // 2 - 100, False, last_screen_buttons_group)
    while running:
        winner_screen.renew()
        last_screen_buttons_group.draw(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 0
            elif event.type == pg.MOUSEBUTTONDOWN:
                # если нажата кнопка 'QUIT', ты мы должны перейти к главному экрану
                if home_button.button_rect().collidepoint(pg.mouse.get_pos()):
                    running = 0
                    return_home = True
                elif button_stats.button_rect().collidepoint(pg.mouse.get_pos()):
                    # если нажали на кнопку статистики, то вылезает экран с итоговой статистикой
                    running_stat = 1
                    players = []
                    # занесем в список ники игроков
                    with open('results.txt', encoding='utf-8') as file_stat:
                        nicknames = file_stat.readlines()[0].split()
                        players.append(nicknames[0])
                        players.append(nicknames[1])
                    button_home_2 = Button(load_image('Back.png', -1), 1, 1, 0, height // 2 + 100, False, sprite_home)
                    # словарь самой статистики
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    sl_of_stat = {'нанесено урона': ['x', 'y'], 'количество выстрелов': ['x', 'y'], 'победитель': ['x', 'y']}
                    while running_stat:
                        for ev in pg.event.get():
                            if ev.type == pg.QUIT:
                                running_stat = 0
                            elif ev.type == pg.MOUSEBUTTONDOWN:
                                if button_home_2.button_rect().collidepoint(pg.mouse.get_pos()):
                                    running_stat = 0
                        screen.blit(load_image('fon_statist.jpg'), (0, 0))
                        # прикрепляем всю статистику по очереди
                        font = pg.font.Font(None, 30)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        screen.blit(font.render(players[0], True, (160, 178, 222)), (width // 2 - 100, 50))
                        screen.blit(font.render(players[1], True, (160, 178, 222)), (width // 2 + 100, 50))
                        # координата разных текстов статистик
                        y = 100
                        for key in sl_of_stat.keys():
                            screen.blit(font.render(key, True, (160, 178, 222)), (width // 2 - 375, y))
                            y += 50
                        # координаты информации для статистик
                        x = width // 2 - 50
                        y = 100
                        for value in sl_of_stat.values():
                            for i in range(2):
                                if i % 2 == 0:
                                    # для первого игрока
                                    x = width // 2 - 75
                                else:
                                    # для второго игрока
                                    x = width // 2 + 150
                                screen.blit(font.render(value[i], True, (160, 178, 222)), (x, y))
                            y += 50
                        sprite_home.draw(screen)
                        pg.display.flip()
                        clock.tick(fps)
        screen.blit(image, (width // 2 - 125, height // 2 - 70))
        screen.blit(text, (width // 2 - 115, height // 2 - 20))
        screen.blit(text_stat, (width // 2 - 335, height // 2 - 80))
        # если прошла одна секунда, то должна появиться корона
        if timer == 50:
            flag = True
        if flag:
            screen.blit(corona, (width // 2 - 50, height // 2 - 165))
            seconds += 1
            # если прошла 1 секунда
            if seconds == 50:
                flag = False
                seconds = 0
                timer = 1
        else:
            timer += 1
        pg.display.flip()
        clock.tick(fps)
    if return_home:
        MainScr()
