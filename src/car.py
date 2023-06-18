import pymunk
import pygame
import pymunk.pygame_util
import math
import os
import numpy as np


class Car:
    def __init__(
        self,
        car_number: int,
        position: tuple[float, float],
        velocity: tuple[float, float],
        mass: float,
        angle: float,
        collision_type: int,
        space: pymunk.Space,
        surface: pygame.Surface,
        debug=None,
    ):
        super().__init__()

        self.__car_number = car_number

        # load image
        self.__image = pygame.image.load(
            os.path.join(os.getcwd(), "assets", "yellow_car.png")
        ).convert_alpha()

        # rotate image
        self.__angle = angle

        # set size base on image
        self.__image = pygame.transform.rotate(self.__image, angle)
        self.__rect = self.__image.get_rect()

        # modeling car using pymunk

        self.__shape = pymunk.Poly.create_box(
            None,
            (self.__image.get_width(), self.__image.get_height()),
        )
        self.__moment = pymunk.moment_for_box(
            mass, (self.__image.get_width(), self.__image.get_height())
        )
        self.__body = pymunk.Body(mass, self.__moment, body_type=pymunk.Body.DYNAMIC)
        self.__shape.body = self.__body
        self.__shape.friction = 1
        self.__shape.elasticity = 0

        self.__shape.color = pygame.Color(0, 0, 0)

        self.__body._set_position(position)
        self.__rect.center = position

        self.__body.moment = self.__moment
        self.__shape.collision_type = collision_type

        self.__surface = surface

        self.__initial_velocity = 0

        space.add(self.__body, self.__shape)

        self.__font = pygame.font.Font(None, 30)

    def get_body(self):
        return self.__body

    def get_mass(self):
        return self.__body._get_mass()

    def set_mass(self, mass: float):
        self.__body._set_mass(mass)

    def get_velocity(self):
        return self.__body._get_velocity()

    def get_speed(self):
        return math.sqrt(
            self.__body._get_velocity()[0] ** 2 + self.__body._get_velocity()[1] ** 2
        )

    def get_center_of_gravity(self):
        return self.__shape.center_of_gravity

    def set_velocity(self, velocity: float):
        self.__initial_velocity = velocity

        if self.__angle >= 0 and self.__angle <= 90:
            self.__body._set_velocity(
                (
                    math.cos(np.deg2rad(self.__angle)) * velocity,
                    -math.sin(np.deg2rad(self.__angle)) * velocity,
                )
            )
        if self.__angle >= 91 and self.__angle <= 180:
            self.__body._set_velocity(
                (
                    math.cos(np.deg2rad(self.__angle)) * velocity,
                    math.sin(np.deg2rad(self.__angle)) * velocity,
                )
            )
        if self.__angle >= 181 and self.__angle <= 270:
            self.__body._set_velocity(
                (
                    math.cos(np.deg2rad(self.__angle)) * velocity,
                    math.sin(np.deg2rad(self.__angle)) * velocity,
                )
            )
        if self.__angle >= 271 and self.__angle <= 360:
            self.__body._set_velocity(
                (
                    math.cos(np.deg2rad(self.__angle)) * velocity,
                    math.sin(np.deg2rad(self.__angle)) * velocity,
                )
            )

    def get_angle(self) -> float:
        return self.__body._get_angle()

    def get_position(self) -> tuple[int, int]:
        return (self.__body.position.x, self.__body.position.y)

    def draw(self):
        self.__car_label_surface = self.__font.render(
            f"Car {self.__car_number}", True, pygame.Color(0, 0, 0)
        )

        self.__angle_surface = self.__font.render(
            f"{round(np.rad2deg(self.__body._get_angle()),2)} degrees",
            True,
            pygame.Color(0, 0, 0),
        )

        self.__speed_surface = self.__font.render(
            f"{round(self.get_speed(), 2)} km/hr", True, pygame.Color(0, 0, 0)
        )

        self.__surface.blit(
            self.__car_label_surface,
            (
                int(self.__body.position.x + (self.__image.get_width() / 4)),
                int(self.__body.position.y - 80),
            ),
        )

        self.__surface.blit(
            self.__angle_surface,
            (
                int(self.__body.position.x + (self.__image.get_width() / 4)),
                int(self.__body.position.y - 60),
            ),
        )

        self.__surface.blit(
            self.__speed_surface,
            (
                int(self.__body.position.x + (self.__image.get_width() / 4)),
                int(self.__body.position.y - 30),
            ),
        )

        self.__surface.blit(
            pygame.transform.rotate(self.__image, np.rad2deg(self.__body._get_angle())),
            (self.__body.position.x, self.__body.position.y),
        )
