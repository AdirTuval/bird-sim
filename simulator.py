import sys
from typing import Tuple
import logging

import pygame
import pymunk
from pymunk import pygame_util, Vec2d
from camera import Camera
from bird import Bird
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

    def __init__(self, *, interactive: bool = False):
        # pymunk physics simulator
        self.space = pymunk.Space(threaded=True)
        self.space.threads = 2
        self.space.gravity = 0, GRAVITY
        self.bird = Bird(self.space, self.WIDTH / 2)
        self.floor = Floor(self.space, self.WIDTH)

        # interactive
        self.gui = True if interactive else False
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

    def run_simulation(self):
        if self.gui:
            assert hasattr(self, 'window')
            assert hasattr(self, 'bg')
            assert hasattr(self, 'zoom')
            assert hasattr(self, 'clock')
            self.run_simulation_interactive()
        else:
            assert hasattr(self, 'policy')
            self.run_simulation_offline()

    def run_simulation_interactive(self):
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
                self.bird.left_wing_down()

            if pygame.key.get_pressed()[pygame.K_j]:  # Down right
                self.bird.right_wing_down()

            if pygame.key.get_pressed()[pygame.K_d]:  # Up left
                self.bird.left_wing_up()

            if pygame.key.get_pressed()[pygame.K_k]:  # Up right
                self.bird.right_wing_up()

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

    def run_simulation_offline(self):
        pass


if __name__ == '__main__':
    sys.exit(BirdSim(interactive=True).run_simulation())
