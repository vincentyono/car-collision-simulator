import os
import pygame
import pymunk.pygame_util


class App:
    def __init__(self, width: int = 1200, height: int = 800, fps: int = 60):
        pygame.init()
        icon_path = os.path.join(os.getcwd(), "assets", "favicon.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_caption("Car Collision Simulator")
        pygame.display.set_icon(icon)

        self.__FPS: int = fps
        self.__clock = pygame.time.Clock()
        self.__running: bool = True
        self.__surface = pygame.display.set_mode((width, height))
        self.__draw_options = pymunk.pygame_util.DrawOptions(self.__surface)
        self.__space = pymunk.Space()
        self.__space.gravity = (0, 0)

    def run(self) -> None:
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()

            self.__space.step(1 / self.__FPS)
            self.__clock.tick(self.__FPS)
