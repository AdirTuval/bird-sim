import sys
import pygame
from pymunk import pygame_util
from camera import Camera
import pymunk
from pymunk.vec2d import Vec2d
from bird import Bird
from floor import Floor
from background import Background
from constants import *

pygame.init()

pygame_util.positive_y_is_up = True

window = pygame.display.set_mode((WIDTH, HEIGHT))
bg = Background(window)
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, GRAVITY
draw_options = pygame_util.DrawOptions(window)

bird = Bird(space, WIDTH / 2)
# zoom = Camera(draw_options, bird, WIDTH, HEIGHT)
floor = Floor(space, WIDTH)
text = pygame.font.Font(None, 16).render(HELP_TEXT, True, pygame.Color("black"))


def translate_coords(v):
    return v[0], HEIGHT - v[1]


def int_point(p):
    return int(p[0]), int(p[1])


def negate_point(p0, p1):
    p0 -= p1
    p0 *= -1
    p0 += p1
    return p0


def lift(m: float, dt: float, dv: Vec2d):
    down_force = m / dt * dv
    # lift = negate_point(down_force, position)
    return -down_force


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

def run_simulation():
    # DEBUG PRINTS
    d_draw_dv = True
    d_draw_lift = True

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
        bg.update(bird.body.position)
        bg.render()

        if run_physics:
            dv_left = bird.left_wing.body.velocity - prev_v_left
            dv_right = bird.right_wing.body.velocity - prev_v_right
            prev_v_left = bird.left_wing.body.velocity
            prev_v_right = bird.right_wing.body.velocity

            lift_right = lift(AIR_MASS, DT, dv_right)
            lift_left = lift(AIR_MASS, DT, dv_left)

        if d_draw_dv:
            draw_dv(dv_left, dv_right)

        if d_draw_lift:
            draw_lift(lift_left, lift_right)

        # capture movement keys
        if pygame.key.get_pressed()[pygame.K_j]:
            bird.right_wing_down()

        if pygame.key.get_pressed()[pygame.K_k]:
            bird.right_wing_up()

        if pygame.key.get_pressed()[pygame.K_f]:
            bird.left_wing_down()

        if pygame.key.get_pressed()[pygame.K_d]:
            bird.left_wing_up()

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

        # zoom.update()
        space.debug_draw(draw_options)
        window.blit(text, (5, 5))
        bird_height = pygame.font.Font(None, 16).render(str(bird.body.position[1]), True, pygame.Color("red"))
        window.blit(bird_height, (5, 20))
        pygame.display.update()
        if run_physics:
            space.step(DT)
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    run_simulation()
