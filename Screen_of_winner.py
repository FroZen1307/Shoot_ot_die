import pygame as pg
import sys
from mainPro import split_animated_gif, load_image, Button
import random


class WinnerScreen:
    def __init__(self, screen):
        global gif3
        self.screen = screen
        # фон экрана для ввода ников
        self.winner_screen_fon = gif3
        # текущий кадр гиф-картинки
        self.cur_cadr = 0

    # обновляем гиф-картинку второго экрана
    def renew(self):
        image = pg.transform.scale(self.winner_screen_fon[self.cur_cadr], (width, height))
        self.screen.blit(image, (0, 0))
        if self.cur_cadr == len(self.winner_screen_fon) - 1:
            self.cur_cadr = 0
        else:
            self.cur_cadr += 1


if __name__ == '__main__':
    gif3 = split_animated_gif('fon_of_winner.gif')
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
    text = font.render(f"'ник победителя'", True, (161, 26, 101))
    # корона победителя должна появляться и исчезать, чтобы было эффектнее, поэтому задаём таймер
    timer = 0
    # корона должна появляться на 1 секунду, мы ставим флажок
    flag = False
    # секунды, на которые появляется корона
    seconds = 0
    pg.mixer.music.load("winner_music.mp3")
    pg.mixer.music.play(-1)
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
                # если нажата кнопка 'активность', ты мы должны перейти к экрану итоговой статистики
                if home_button.button_rect().collidepoint(pg.mouse.get_pos()):
                    pass
                elif button_stats.button_rect().collidepoint(pg.mouse.get_pos()):
                    # если нажали на кнопку статистики, то вылезает экран с итоговой статистикой
                    running_stat = 1
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
                        screen.blit(font.render("игрок 1", True, (160, 178, 222)), (width // 2 - 100, 50))
                        screen.blit(font.render("игрок 2", True, (160, 178, 222)), (width // 2 + 100, 50))
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
