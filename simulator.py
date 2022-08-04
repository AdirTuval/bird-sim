import sys
from typing import Tuple

import pygame
from pymunk import pygame_util
from camera import Camera
import pymunk
from pymunk import Vec2d
from bird import Bird
from floor import Floor
from background import Background
from constants import *

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
DT = 1 / FPS
GRAVITY = -1000
FLOOR_HEIGHT = 10
BACKGROUND_COLOR = "white"
AIR_MASS = 0.5
LEFT = 0
RIGHT = 1

pymunk.pygame_util.positive_y_is_up = True

window = pygame.display.set_mode((WIDTH, HEIGHT))
bg = Background(window)
clock = pygame.time.Clock()
space = pymunk.Space(threaded=True)
space.threads = 2
space.gravity = 0, GRAVITY
draw_options = pygame_util.DrawOptions(window)

bird = Bird(space, WIDTH / 2)
zoom = Camera(draw_options, bird, WIDTH, HEIGHT)
floor = Floor(space, WIDTH)
text = pygame.font.Font(None, 16).render(HELP_TEXT, True, pygame.Color("black"))


def translate_coords(v):
    return v[0], HEIGHT - v[1]


def int_point(p):
    return int(p[0]), int(p[1])


def draw_dv(dv_left: Vec2d, dv_right: Vec2d):
    pygame.draw.line(window, BLACK,
                     pygame_util.to_pygame(bird.left_wing.body.position, window),
                     pygame_util.to_pygame(bird.left_wing.body.position + dv_left, window))
    pygame.draw.line(window, BLACK,
                     pygame_util.to_pygame(bird.right_wing.body.position, window),
                     pygame_util.to_pygame(bird.right_wing.body.position + dv_right, window))


def draw_lift(lift_left: Vec2d, lift_right: Vec2d):
    pygame.draw.line(window, RED,
                     pygame_util.to_pygame(bird.left_wing.body.position, window),
                     pygame_util.to_pygame(bird.left_wing.body.position + lift_left, window))
    pygame.draw.line(window, RED,
                     pygame_util.to_pygame(bird.right_wing.body.position, window),
                     pygame_util.to_pygame(bird.right_wing.body.position + lift_right, window))


def draw_drag_force(drag_force: Vec2d, applied_point: Vec2d):
    pygame.draw.line(window, WHITE,
                     pygame_util.to_pygame(applied_point, window),
                     pygame_util.to_pygame(applied_point + drag_force, window), 10)


def lift(m: float, dt: float, dv: Vec2d):
    down_force = m / dt * dv
    return -down_force


def apply_drag_force(body: pymunk.Body, *, drag_coeff: float = DRAG_COEFFICIENT) -> Tuple[Vec2d, Vec2d]:
    pointing_direction = Vec2d(1, 0).rotated(body.angle)
    flight_direction = Vec2d(*body.velocity)
    flight_direction, flight_speed = flight_direction.normalized_and_length()

    dot = flight_direction.dot(pointing_direction)

    drag_force_magnitude = (1 - abs(dot)) * (flight_speed ** 2) * drag_coeff * body.mass
    drag_force = drag_force_magnitude * -flight_direction

    body.apply_force_at_local_point(drag_force)
    body.angular_velocity *= ANGULAR_VELOCITY_DECAY

    return drag_force, body.position


def run_simulation():
    # DEBUG PRINTS - enable only when zoom is not set.
    debug_draw_dv = False
    debug_draw_lift = False
    debug_draw_drag_force = False

    running = True
    run_physics = True
    dv_left = Vec2d(0, 0)
    dv_right = Vec2d(0, 0)
    prev_v_left = Vec2d(0, 0)
    prev_v_right = Vec2d(0, 0)
    lift_left = Vec2d(0, 0)
    lift_right = Vec2d(0, 0)

    while running:
        window.fill((0, 0, 0))
        bg.update(bird.position)
        bg.render()

        if debug_draw_dv:
            draw_dv(dv_left, dv_right)

        if debug_draw_lift:
            draw_lift(lift_left, lift_right)

        if run_physics:
            drag_force, applied_point = apply_drag_force(bird.body)
            if debug_draw_drag_force:
                draw_drag_force(drag_force, applied_point)

            dv_left = bird.left_wing.body.velocity - prev_v_left
            dv_right = bird.right_wing.body.velocity - prev_v_right
            prev_v_left = bird.left_wing.body.velocity
            prev_v_right = bird.right_wing.body.velocity
            lift_left = lift(bird.left_wing.WING_AREA, DT, dv_left)
            lift_right = lift(bird.right_wing.WING_AREA, DT, dv_right)

        # capture movement keys
        if pygame.key.get_pressed()[pygame.K_f]:  # Down left
            bird.left_wing_down()

        if pygame.key.get_pressed()[pygame.K_j]:  # Down right
            bird.right_wing_down()

        if pygame.key.get_pressed()[pygame.K_d]:  # Up left
            bird.left_wing_up()

        if pygame.key.get_pressed()[pygame.K_k]:  # Up right
            bird.right_wing_up()

        # capture game settings keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and (
                    event.key in [pygame.K_ESCAPE, pygame.K_q]
            ):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(window, "bird_capture.png")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_physics = not run_physics
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                bird.re_origin()

        zoom.update()
        space.debug_draw(draw_options)
        window.blit(text, (5, 5))
        bird_height = pygame.font.Font(None, 16).render(str(bird.y), True, pygame.Color("red"))
        window.blit(bird_height, (5, 20))
        pygame.display.update()

        if run_physics:
            space.step(DT)

        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    run_simulation()
