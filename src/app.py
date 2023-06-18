import os
import pygame
import pymunk.pygame_util
from car import Car
from button import Button
from text_box import TextBox


class App:
    def __init__(self, width: int = 1200, height: int = 800, fps: int = 60):
        # Initialize pygame
        pygame.init()

        # load icon
        icon_path = os.path.join(os.getcwd(), "assets", "favicon.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

        # set application title
        pygame.display.set_caption("Car Collision Simulator")

        # pygame initial configuration
        self.__FPS: int = fps
        self.__running: bool = True
        self.__clock = pygame.time.Clock()

        # pymunk initial configuration
        self.__space = pymunk.Space()
        self.__space.gravity = 0, 0

        # set window size
        self.__window = pygame.display.set_mode((width, height))
        self.__draw_options = pymunk.pygame_util.DrawOptions(self.__window)

        # control panel configuration
        self.__control_panel_window = pygame.Surface(
            (width, height * 0.5)
        )  # height is 50% of window

        self.__control_panel_window.fill(pygame.Color(31, 31, 31))
        # button
        self.__control_panel_buttons = [
            Button(
                (50, (height - 150) - ((3 - 1) * 100)),
                os.path.join(os.getcwd(), "assets", f"scenario_{1}_button.png"),
                self.__scenario_1,
                self.__window,
            ),
            Button(
                (50, (height - 150) - ((3 - 2) * 100)),
                os.path.join(os.getcwd(), "assets", f"scenario_{2}_button.png"),
                self.__scenario_2,
                self.__window,
            ),
            Button(
                (50, (height - 150) - ((3 - 3) * 100)),
                os.path.join(os.getcwd(), "assets", f"scenario_{3}_button.png"),
                self.__scenario_3,
                self.__window,
            ),
        ]

        self.__util_buttons = [
            Button(
                (width - 300, (height - 150) - ((3 - 1) * 100)),
                os.path.join(os.getcwd(), "assets", "start_button.png"),
                self.__handle_start_button,
                self.__window,
            ),
            Button(
                (width - 300, (height - 150) - ((3 - 2) * 100)),
                os.path.join(os.getcwd(), "assets", "reset_button.png"),
                self.__handle_reset_button,
                self.__window,
            ),
        ]

        # text box
        self.__text_boxes = [
            TextBox(
                (
                    (self.__window.get_width() / 2) - 200,
                    50 + (self.__window.get_height() / 2),
                ),
                "Car 1 Speed",
                "km/hr",
                self.__window,
            ),
            TextBox(
                (
                    (self.__window.get_width() / 2) - 200,
                    60 + 50 + (self.__window.get_height() / 2),
                ),
                "Car 1 Mass",
                "kg",
                self.__window,
            ),
            TextBox(
                (
                    (self.__window.get_width() / 2) - 200,
                    120 + 50 + 50 + (self.__window.get_height() / 2),
                ),
                "Car 2 Speed",
                "km/hr",
                self.__window,
            ),
            TextBox(
                (
                    (self.__window.get_width() / 2) - 200,
                    180 + 50 + 50 + (self.__window.get_height() / 2),
                ),
                "Car 2 Mass",
                "kg",
                self.__window,
            ),
        ]

        # cars
        self.__cars = []

        # default scenario
        self.__current_scenario = 1
        self.__scenario_1()

        # pymunk collision handler
        self.__collision = self.__space.add_collision_handler(1, 2)

        self.__time = 0
        self.__stop_time = True
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def __handle_start_button(self):
        self.__stop_time = False
        for body in self.__cars:
            self.__space.reindex_shapes_for_body(body.get_body())

        for textbox in self.__text_boxes:
            if "Mass" in textbox.get_label() and textbox.get_value() == 0:
                print("Mass cannot be 0")
                return

            if textbox.get_label() == "Car 1 Speed":
                self.__cars[0].set_velocity(textbox.get_value())

            if textbox.get_label() == "Car 1 Mass":
                self.__cars[0].set_mass(textbox.get_value())

            if textbox.get_label() == "Car 2 Speed":
                self.__cars[1].set_velocity(textbox.get_value())

            if textbox.get_label() == "Car 2 Mass":
                self.__cars[1].set_mass(textbox.get_value())

    def __handle_reset_button(self):
        self.__stop_time = True
        self.__time = 0

        self.__space = pymunk.Space()
        self.__cars = []

        if self.__current_scenario == 1:
            self.__scenario_1()

        elif self.__current_scenario == 2:
            self.__scenario_2()

        elif self.__current_scenario == 3:
            self.__scenario_3()

    def __scenario_1(self):
        self.__current_scenario = 1
        self.__space = pymunk.Space()
        self.__cars = [
            Car(
                1,
                (0, 200 - 51),
                (0, 0),
                2500,
                0,
                1,
                self.__space,
                self.__window,
            ),
            Car(
                2,
                (1200 - 204, 200 - 51),
                (0, 0),
                2500,
                180,
                2,
                self.__space,
                self.__window,
            ),
        ]

    def __scenario_2(self):
        self.__current_scenario = 2
        self.__space = pymunk.Space()
        self.__cars = [
            Car(
                1,
                (0, 200 - 51),
                (0, 0),
                2500,
                0,
                1,
                self.__space,
                self.__window,
            ),
            Car(
                2,
                (1200 / 2, 200 - 51),
                (0, 0),
                2500,
                0,
                2,
                self.__space,
                self.__window,
            ),
        ]

    def __scenario_3(self):
        self.__current_scenario = 3
        self.__space = pymunk.Space()
        self.__cars = [
            Car(
                1,
                (50, 450),
                (0, 0),
                2500,
                90,
                1,
                self.__space,
                self.__window,
                self.__draw_options,
            ),
            Car(
                2,
                (1200 - 204, 200 - 51),
                (0, 0),
                2500,
                180,
                2,
                self.__space,
                self.__window,
                self.__draw_options,
            ),
        ]

    def __begin(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict) -> bool:
        self.__space._set_damping(0.1)
        self.__stop_time = True

        return True

    def __pre_solve(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict
    ) -> bool:
        return True

    def __post_solve(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict
    ) -> None:
        print(f"Force: {arbiter.total_impulse}")

    def run(self) -> None:
        self.__collision.begin = self.__begin
        self.__collision.pre_solve = self.__pre_solve
        self.__collision.post_solve = self.__post_solve

        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False

                if event.type == pygame.USEREVENT:
                    if not self.__stop_time:
                        self.__time += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.__control_panel_buttons:
                        if button.is_clicked():
                            button.on_click()

                    for button in self.__util_buttons:
                        if button.is_clicked():
                            button.on_click()

                    for text_box in self.__text_boxes:
                        if text_box.is_clicked():
                            text_box.set_active(True)
                        else:
                            text_box.set_active(False)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        for text_box in self.__text_boxes:
                            if text_box.is_active():
                                text_box.on_backspace_keypress()
                    else:
                        for text_box in self.__text_boxes:
                            if text_box.is_active():
                                text_box.on_unicode_keypress(event.unicode)

            self.__window.fill(pygame.Color(235, 236, 240))

            for i, car in enumerate(self.__cars):
                car.draw()

            self.__window.blit(
                self.__control_panel_window,
                (0, self.__window.get_height() * 0.5),
            )

            for button in self.__control_panel_buttons:
                button.draw()

            for text_box in self.__text_boxes:
                text_box.draw()

            for button in self.__util_buttons:
                button.draw()

            pygame.display.update()
            for car in self.__cars:
                self.__space.reindex_shapes_for_body(car.get_body())
            self.__space.debug_draw(self.__draw_options)
            self.__space.step(1 / self.__FPS)
            self.__clock.tick(self.__FPS)

        pygame.quit()
