import pygame
import string


class TextBox:
    def __init__(
        self, position: tuple[int, int], label: str, unit: str, surface: pygame.Surface
    ):
        self.__value = "0"
        self.__position = position
        self.__label = label
        self.__surface = surface
        self.__font_size = 42
        self.__unit = unit
        self.__font = pygame.font.Font(None, self.__font_size)
        self.__label_surface = self.__font.render(
            label, True, pygame.Color(255, 255, 255)
        )
        self.__value_surface = self.__font.render(
            self.__value, True, pygame.Color(255, 255, 255)
        )
        self.__unit_surface = self.__font.render(
            self.__unit, True, pygame.Color(255, 255, 255)
        )

        self.__text_box_rect = pygame.draw.rect(
            self.__surface,
            pygame.Color(51, 125, 178),
            (
                self.__position[0] + self.__label_surface.get_width() + 8,
                self.__position[1],
                100,
                self.__font_size + 8,
            ),
            border_radius=5,
        )

        self.__is_active = False

    def get_value(self) -> float:
        if len(self.__value) == 0:
            print("Please input all textbox")
        else:
            return float(self.__value)

    def get_label(self) -> str:
        return self.__label

    def is_active(self) -> bool:
        return self.__is_active

    def set_active(self, active: bool) -> None:
        if active:
            self.__value = "0"
        self.__is_active = active

    def on_unicode_keypress(self, value: str) -> None:
        if value in string.digits and len(self.__value) < 5:
            if self.__value[0] == "0":
                self.__value = self.__value[1:] + value
            else:
                self.__value += value

    def on_backspace_keypress(self) -> None:
        if len(self.__value) > 0:
            self.__value = self.__value[:-1]

        if len(self.__value) == 0:
            self.__value = "0"

    def is_clicked(self) -> bool:
        return self.__text_box_rect.collidepoint(pygame.mouse.get_pos())

    def draw(self) -> None:
        if self.__is_active:
            pygame.draw.rect(
                self.__surface,
                pygame.Color(255, 99, 71),
                (
                    self.__position[0] + self.__label_surface.get_width() + 8 - 4,
                    self.__position[1] - 4,
                    100 + 8,
                    self.__font_size + 8 + 8,
                ),
                border_radius=10,
            )

        pygame.draw.rect(
            self.__surface,
            pygame.Color(51, 125, 178),
            (
                self.__position[0] + self.__label_surface.get_width() + 8,
                self.__position[1],
                100,
                self.__font_size + 8,
            ),
            border_radius=5,
        )

        self.__value_surface = self.__font.render(
            self.__value, True, pygame.Color(255, 255, 255)
        )

        self.__surface.blit(
            self.__label_surface, (self.__position[0], self.__position[1] + 8)
        )

        self.__surface.blit(
            self.__value_surface,
            (
                self.__position[0] + self.__label_surface.get_width() + 16,
                self.__position[1] + 12,
            ),
        )
        self.__surface.blit(
            self.__unit_surface,
            (
                self.__position[0] + self.__label_surface.get_width() + 100 + 20,
                self.__position[1] + 12,
            ),
        )
