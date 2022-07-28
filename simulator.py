import pygame
import pymunk.pygame_util
from pymunk import Vec2d
import pymunk
from bird import BIRD_RECT_HEIGHT, BIRD_RECT_WIDTH, Bird
from floor import Floor
import math

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
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, GRAVITY
draw_options = pymunk.pygame_util.DrawOptions(window)

bird = Bird(space, WIDTH / 2)
floor = Floor(space, WIDTH)

def translate_coords(v):
    return v[0], HEIGHT - v[1]

def int_point(p):
    return int(p[0]), int(p[1])

def negate_point(p0,p1):
    p0 -= p1
    p0 *= -1
    p0 += p1
    return p0

def calc_velocity_vectors(origin, v, side=LEFT):
    origin = Vec2d(*int_point(origin))
    if v[1] > 0:
        Vec2d(0,0)
    down_force = origin + Vec2d(*int_point(v))
    lift_force = negate_point(down_force, origin)
    pygame.draw.line(window, "black", translate_coords(origin), translate_coords(lift_force))
    return 0, lift_force[1] # Hacky shit, canceling X force.




def run_simulation():

    run_physics = True
    prior_v_left = None
    dv_left = None
    prior_v_right = None
    dv_right = None

    font = pygame.font.Font(None, 16)
    text = font.render(
        HELP_TEXT,
        True,
        pygame.Color("black"),
    )
    translation = pymunk.Transform()
    scaling = 1
    rotation = 0

    while True:
        window.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(window, "bird_capture.png")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                bird.left_wing.body.apply_impulse_at_local_point((0,300),(-30,0))
                bird.right_wing.body.apply_impulse_at_local_point((0,300),(30,0))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                bird.left_wing.body.apply_impulse_at_local_point((0,-100),(-30,0))
                bird.right_wing.body.apply_impulse_at_local_point((0,-100),(30,0))
                left_lift = calc_velocity_vectors(bird.left_wing.body.position, (AIR_MASS/DT)*dv_left)
                right_lift = calc_velocity_vectors(bird.right_wing.body.position,(AIR_MASS/DT)*dv_right)
                bird.body.apply_impulse_at_local_point(left_lift, (-BIRD_RECT_WIDTH / 2, BIRD_RECT_HEIGHT/2))
                bird.body.apply_impulse_at_local_point(right_lift, (BIRD_RECT_WIDTH / 2, BIRD_RECT_HEIGHT/2))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_physics = not run_physics
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                bird.re_origin()



        keys = pygame.key.get_pressed()
        left = int(keys[pygame.K_LEFT])
        up = int(keys[pygame.K_UP])
        down = int(keys[pygame.K_DOWN])
        right = int(keys[pygame.K_RIGHT])
        zoom_in = int(keys[pygame.K_a])
        zoom_out = int(keys[pygame.K_z])

        if pymunk.pygame_util.positive_y_is_up:
            up, down = down, up

        translate_speed = 10
        translation = translation.translated(
            translate_speed * left - translate_speed * right,
            translate_speed * up - translate_speed * down,
        )

        zoom_speed = 0.1
        scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

        # to zoom with center of screen as origin we need to offset with
        # center of screen, scale, and then offset back
        draw_options.transform = (
            pymunk.Transform.translation(300, 300)
            @ pymunk.Transform.scaling(scaling)
            @ translation
            @ pymunk.Transform.translation(-300, -300)
        )


        if run_physics:
            dv_left = bird.left_wing.body.velocity - prior_v_left if prior_v_left else bird.left_wing.body.velocity
            prior_v_left = bird.left_wing.body.velocity
            dv_right = bird.right_wing.body.velocity - prior_v_right if prior_v_right else bird.right_wing.body.velocity
            prior_v_right = bird.right_wing.body.velocity


        # lift = get_lift()

        window.fill(BACKGROUND_COLOR)
        window.blit(text, (5, 5))
        space.debug_draw(draw_options)
        pygame.display.update()
        if run_physics:
            space.step(DT)
        clock.tick(FPS)




if __name__ == '__main__':
    run_simulation()