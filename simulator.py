import pygame
import pymunk.pygame_util
from camera import Camera
from pymunk import Vec2d
import pymunk
from bird import Bird, Wing
from floor import Floor
import math
from background import Background

HELP_TEXT = """Use Arrows (up, down, left, right) to move the camera, a and z to zoom in / out.
R - restart"""

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


def calc_velocity_vectors(origin, v, side=LEFT):
    origin = Vec2d(*int_point(origin))
    if v[1] > 0:
        Vec2d(0, 0)
    down_force = origin + Vec2d(*int_point(v))
    lift_force = negate_point(down_force, origin)
    # pygame.draw.line(window, "black", translate_coords(origin), translate_coords(lift_force))
    return 0, lift_force[1]  # Hacky shit, canceling X force.


def run_simulation():
    run_physics = True
    prior_v_left = None
    dv_left = None
    prior_v_right = None
    dv_right = None

    
    while True:
        window.fill((0,0,0))
        bg.update()
        bg.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(window, "bird_capture.png")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                bird.left_wing.body.apply_impulse_at_local_point((0, 300), (-Wing.WING_WIDTH, 0))
                bird.right_wing.body.apply_impulse_at_local_point((0, 300), (Wing.WING_WIDTH, 0))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                bird.left_wing.body.apply_impulse_at_local_point((0, -100), (-Wing.WING_WIDTH, 0))
                bird.right_wing.body.apply_impulse_at_local_point((0, -100), (Wing.WING_WIDTH, 0))
                left_lift = calc_velocity_vectors(bird.left_wing.body.position, (AIR_MASS / DT) * dv_left)
                right_lift = calc_velocity_vectors(bird.right_wing.body.position, (AIR_MASS / DT) * dv_right)
                bird.body.apply_impulse_at_local_point(left_lift, (-Bird.BIRD_RECT_WIDTH / 2, Bird.BIRD_RECT_HEIGHT / 2))
                bird.body.apply_impulse_at_local_point(right_lift, (Bird.BIRD_RECT_WIDTH / 2, Bird.BIRD_RECT_HEIGHT / 2))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_physics = not run_physics
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                bird.re_origin()

        if run_physics:
            dv_left = bird.left_wing.body.velocity - prior_v_left if prior_v_left else bird.left_wing.body.velocity
            prior_v_left = bird.left_wing.body.velocity
            dv_right = bird.right_wing.body.velocity - prior_v_right if prior_v_right else bird.right_wing.body.velocity
            prior_v_right = bird.right_wing.body.velocity

        zoom.update()
        space.debug_draw(draw_options)
        pygame.display.update()
        if run_physics:
            space.step(DT)
        clock.tick(FPS)


if __name__ == '__main__':
    run_simulation()
