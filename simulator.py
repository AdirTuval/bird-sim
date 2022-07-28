import pygame
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

from camera import Camera
import pymunk
from bird import Bird
from floor import Floor
from background import Background

HELP_TEXT = """Use A,Z to zoom. D,F - control left wing, J,K - control right wing."""

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
DRAG_COEFFICIENT = 0.0002

pymunk.pygame_util.positive_y_is_up = True

window = pygame.display.set_mode((WIDTH, HEIGHT))
bg = Background(window)
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, GRAVITY
draw_options = pymunk.pygame_util.DrawOptions(window)

bird = Bird(space, WIDTH / 2)
zoom = Camera(draw_options, bird, WIDTH, HEIGHT)
floor = Floor(space, WIDTH)


def translate_coords(v):
    return v[0], HEIGHT - v[1]


def int_point(p):
    return int(p[0]), int(p[1])


def negate_point(p0, p1):
    p0 -= p1
    p0 *= -1
    p0 += p1
    return p0


def apply_drag_force(body: pymunk.Body, tail_position: Vec2d):
    pointing_direction = Vec2d(1, 0).rotated(body.angle)
    flight_direction = Vec2d(*body.velocity)
    flight_direction, flight_speed = flight_direction.normalized_and_length()

    dot = flight_direction.dot(pointing_direction)
    drag_force_magnitude = (
            (1 - abs(dot)) * flight_speed ** 2 * DRAG_COEFFICIENT * body.mass
    )
    body_tail_position = body.position + tail_position.rotated(body.angle)
    body.apply_impulse_at_world_point(
        drag_force_magnitude * -flight_direction, body_tail_position
    )
    body.angular_velocity *= 0.5


def run_simulation():
    run_physics = True

    while True:
        window.fill((0, 0, 0))
        bg.update()
        bg.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(window, "bird_capture.png")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_j: bird.right_wing_down()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k: bird.right_wing_up()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f: bird.left_wing_down()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d: bird.left_wing_up()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: run_physics = not run_physics
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r: bird.re_origin()



        zoom.update()
        space.debug_draw(draw_options)

        if run_physics:
            apply_drag_force(bird.body, Vec2d(0, -bird.BIRD_RECT_HEIGHT/2))

        pygame.display.update()
        if run_physics:
            space.step(DT)
        clock.tick(FPS)


if __name__ == '__main__':
    run_simulation()
