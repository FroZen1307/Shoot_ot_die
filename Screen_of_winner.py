import pygame as pg
import sys
from mainPro import split_animated_gif, load_image, Button

screen_rect = (0, 0, 800, 600)
GRAVITY = 0.5


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


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
    sec = 0
    image = pg.transform.scale(load_image('winner.png', -1), (300, 150))
    corona = pg.transform.scale(load_image('corona_real.jpg', -1), (150, 115))
    font = pg.font.Font(None, 50)
    text = font.render(f"'ник победителя'", True, (71, 116, 194))
    # корона победителя должна появляться и исчезать, чтобы было эффектнее, поэтому задаём таймер
    timer = 0
    # корона должна появляться на 1 секунду, мы ставим флажок
    flag = False
    # секунды, на которые появляется корона
    seconds = 0
    while running:
        winner_screen.renew()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 0
        if sec == 50:
            for i in range(3):
                create_particles((random.randint(0, 800), random.randint(0, 600)))
            sec = 0
        screen.blit(image, (width // 2 - 125, height // 2 - 70))
        screen.blit(text, (width // 2 - 115, height // 2 - 20))
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
        sec += 1

        pg.display.flip()
        clock.tick(fps)
