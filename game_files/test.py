import pygame
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Параметры окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Класс для спрайта
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y


# Создание спрайта и стен
player = Player()
player.rect.x = screen_width // 2
player.rect.y = screen_height // 2

left_wall = pygame.Rect(0, 0, 10, screen_height)
right_wall = pygame.Rect(screen_width - 10, 0, 10, screen_height)

# Группа спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.velocity.x = -5
            if event.key == K_RIGHT:
                player.velocity.x = 5
        elif event.type == KEYUP:
            if event.key == K_LEFT and player.velocity.x < 0:
                player.velocity.x = 0
            if event.key == K_RIGHT and player.velocity.x > 0:
                player.velocity.x = 0

    # Обновление положения спрайта
    player.update()

    # Проверка столкновений со стенами
    if player.rect.colliderect(left_wall):
        player.rect.left = left_wall.right
        player.velocity.x = max(0, player.velocity.x)
    if player.rect.colliderect(right_wall):
        player.rect.right = right_wall.left
        player.velocity.x = min(0, player.velocity.x)

    # Отрисовка
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_wall)
    pygame.draw.rect(screen, WHITE, right_wall)
    all_sprites.draw(screen)

    # Обновление экрана
    pygame.display.flip()

pygame.quit()
