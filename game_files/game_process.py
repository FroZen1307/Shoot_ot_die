import pygame
from PIL import Image
import os


def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret


class BattleField:
    def __init__(self, screen):
        self.fon = split_animated_gif('BG_gif.gif')
        self.screen = screen

    def renew(self, k):
        for i in self.fon:
            image = pygame.transform.scale(self.fon[k], (width, height))
            self.screen.blit(image, (0, 0))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    field = BattleField(screen)
    pygame.quit()
