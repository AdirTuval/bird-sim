import sys
from collections import namedtuple
from typing import Tuple, Sequence
import logging

import numpy as np
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pymunk
from matplotlib import pyplot as plt
from pymunk import pygame_util, Vec2d
from camera import Camera
from bird import Bird, BirdState
from floor import Floor
from background import Background
from constants import *

logger = logging.getLogger(__name__)

# DEBUG PRINTS - enable only when zoom is not set.
debug_draw_dv = False
debug_draw_lift = False
debug_draw_drag_force = False


class BirdSim():
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    DT = 1 / FPS
    GRAVITY = -1000

    def __init__(self, *, gui: bool = False):
        # pymunk physics simulator
        self.space = pymunk.Space(threaded=True)
        self.space.threads = 2
        self.space.gravity = 0, GRAVITY
        self.bird = Bird(self.space, self.WIDTH / 2)
        self.floor = Floor(self.space, self.WIDTH)

        # gui
        self.gui = gui
        if self.gui:
            pymunk.pygame_util.positive_y_is_up = True
            pygame.init()
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            self.gui_controller = pygame_util.DrawOptions(self.window)
            self.bg = Background(self.window)
            self.clock = pygame.time.Clock()
            self.zoom = Camera(self.gui_controller, self.bird, self.WIDTH, self.HEIGHT)
            self.text = pygame.font.Font(None, 16).render(HELP_TEXT, True, pygame.Color("black"))

    @classmethod
    def translate_coords(cls, v):
        return v[0], cls.HEIGHT - v[1]

    @staticmethod
    def int_point(p):
        return int(p[0]), int(p[1])

    def draw_dv(self, dv_left: Vec2d, dv_right: Vec2d):
        pygame.draw.line(self.window, BLACK,
                         pygame_util.to_pygame(self.bird.left_wing.body.position, self.window),
                         pygame_util.to_pygame(self.bird.left_wing.body.position + dv_left, self.window))
        pygame.draw.line(self.window, BLACK,
                         pygame_util.to_pygame(self.bird.right_wing.body.position, self.window),
                         pygame_util.to_pygame(self.bird.right_wing.body.position + dv_right, self.window))

    def draw_lift(self, lift_left: Vec2d, lift_right: Vec2d):
        pygame.draw.line(self.window, RED,
                         pygame_util.to_pygame(self.bird.left_wing.body.position, self.window),
                         pygame_util.to_pygame(self.bird.left_wing.body.position + lift_left, self.window))
        pygame.draw.line(self.window, RED,
                         pygame_util.to_pygame(self.bird.right_wing.body.position, self.window),
                         pygame_util.to_pygame(self.bird.right_wing.body.position + lift_right, self.window))

    def draw_drag_force(self, drag_force: Vec2d, applied_point: Vec2d):
        pygame.draw.line(self.window, WHITE,
                         pygame_util.to_pygame(applied_point, self.window),
                         pygame_util.to_pygame(applied_point + drag_force, self.window), 10)

    @staticmethod
    def lift(m: float, dt: float, dv: Vec2d):
        down_force = m / dt * dv
        return -down_force

    def apply_drag_force(self, body: pymunk.Body, *, drag_coeff: float = DRAG_COEFFICIENT) -> Tuple[Vec2d, Vec2d]:
        pointing_direction = Vec2d(1, 0).rotated(body.angle)
        flight_direction = Vec2d(*body.velocity)
        flight_direction, flight_speed = flight_direction.normalized_and_length()

        dot = flight_direction.dot(pointing_direction)

        drag_force_magnitude = (1 - abs(dot)) * (flight_speed ** 2) * drag_coeff * body.mass
        drag_force = drag_force_magnitude * -flight_direction

        body.apply_force_at_local_point(drag_force)
        body.angular_velocity *= ANGULAR_VELOCITY_DECAY

        return drag_force, body.position

    def left_wing_down(self):
        self.bird.left_wing_down()

    def right_wing_down(self):
        self.bird.right_wing_down()

    def left_wing_up(self):
        self.bird.left_wing_up()

    def right_wing_up(self):
        self.bird.right_wing_up()

    def get_state(self) -> BirdState:
        return self.bird.get_state()

    def run_simulation_interactive(self):
        if not self.gui \
                and hasattr(self, 'window') \
                and hasattr(self, 'bg') \
                and hasattr(self, 'zoom') \
                and hasattr(self, 'clock'):
            raise AssertionError("BirdSim was not configured to run with a GUI, try instantiate with gui.")

        running = True
        run_physics = True

        dv_left = Vec2d(0, 0)
        dv_right = Vec2d(0, 0)
        prev_v_left = Vec2d(0, 0)
        prev_v_right = Vec2d(0, 0)
        lift_left = Vec2d(0, 0)
        lift_right = Vec2d(0, 0)

        while running:
            self.window.fill((0, 0, 0))
            self.bg.update(self.bird.position)
            self.bg.render()

            if debug_draw_dv:
                self.draw_dv(dv_left, dv_right)

            if debug_draw_lift:
                self.draw_lift(lift_left, lift_right)

            if run_physics:
                drag_force, applied_point = self.apply_drag_force(self.bird.body)
                if debug_draw_drag_force:
                    self.draw_drag_force(drag_force, applied_point)

                dv_left = self.bird.left_wing.body.velocity - prev_v_left
                dv_right = self.bird.right_wing.body.velocity - prev_v_right
                prev_v_left = self.bird.left_wing.body.velocity
                prev_v_right = self.bird.right_wing.body.velocity
                lift_left = self.lift(self.bird.left_wing.WING_AREA, DT, dv_left)
                lift_right = self.lift(self.bird.right_wing.WING_AREA, DT, dv_right)

            # capture movement keys
            if pygame.key.get_pressed()[pygame.K_f]:  # Down left
                self.left_wing_down()

            if pygame.key.get_pressed()[pygame.K_j]:  # Down right
                self.right_wing_down()

            if pygame.key.get_pressed()[pygame.K_d]:  # Up left
                self.left_wing_up()

            if pygame.key.get_pressed()[pygame.K_k]:  # Up right
                self.right_wing_up()

            # capture game settings keys
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and (
                        event.key in [pygame.K_ESCAPE, pygame.K_q]
                ):
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pygame.image.save(self.window, "bird_capture.png")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    run_physics = not run_physics
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.bird.re_origin()

            self.zoom.update()
            self.space.debug_draw(self.gui_controller)
            bird_height = pygame.font.Font(None, 16).render(str(self.bird.y), True, pygame.Color("red"))
            self.window.blit(self.text, (5, 5))
            self.window.blit(bird_height, (5, 20))
            pygame.display.update()

            if run_physics:
                self.space.step(self.DT)

            self.clock.tick(self.FPS)

        pygame.quit()

    def run_simulation_offline(self, policy: np.ndarray, *, gui: bool = False) -> Tuple[float, Sequence[float]]:
        """
        Run simulation for TRAIN_TIME_SEC seconds and return the result

        Returns:
            final altitude and altitudes graph over simulation time
        """

        if policy.size != POLICY_LEN:
            try:
                policy = policy.reshape((60, 2))
                policy = np.repeat(policy, 10, axis=0)
                policy = policy.reshape(1200)
            except:
                raise AttributeError(f"policy must be at length of {POLICY_LEN}")

        if gui and not self.gui:
            logger.warning("simulation was set to run with gui, but simulator was not instantiated with gui. Continue without gui")

        bird_altitudes = []

        for i in range(0, policy.size, 2):
            if gui and self.gui:
                self.window.fill((0, 0, 0))
                self.bg.update(self.bird.position)
                self.bg.render()

            self.apply_drag_force(self.bird.body)

            if policy[i] == -1:  # Down left
                self.left_wing_down()

            if policy[i + 1] == -1:  # Down right
                self.right_wing_down()

            if policy[i] == 1:  # Up left
                self.left_wing_up()

            if policy[i + 1] == 1:  # Up right
                self.right_wing_up()

            bird_altitudes.append(self.bird.y)

            if gui and self.gui:
                self.zoom.update()
                self.space.debug_draw(self.gui_controller)
                bird_height = pygame.font.Font(None, 16).render(str(self.bird.y), True, pygame.Color("red"))
                self.window.blit(self.text, (5, 5))
                self.window.blit(bird_height, (5, 20))
                pygame.display.update()

            self.space.step(self.DT)

            if gui and self.gui:
                self.clock.tick(self.FPS)

        return self.bird.y, bird_altitudes


if __name__ == '__main__':
    alts = {}
    with open(f'out/ga3_600.npy', 'rb') as f:
        example_policy = np.load(f)
        BirdSim(gui=True).run_simulation_offline(policy=example_policy, gui=True)
        # BirdSim(gui=True).run_simulation_interactive()



