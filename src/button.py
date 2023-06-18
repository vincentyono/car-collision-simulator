import pygame


class Button:
    def __init__(
        self,
        position: tuple[int, int],
        img_path: str,
        on_click: callable,
        surface: pygame.Surface,
    ):
        super().__init__()
        self.__surface = surface
        self.__image = pygame.image.load(img_path).convert_alpha()
        self.__image = pygame.transform.scale(self.__image, (250, 83))
        self.__rect = self.__image.get_rect()
        self.__rect.topleft = position
        self.__on_click = on_click

    def on_click(self):
        self.__on_click()

    def set_on_click(self, function: callable):
        self.__on_click = function

    def is_clicked(self):
        return self.__rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        self.__surface.blit(self.__image, (self.__rect.x, self.__rect.y))
