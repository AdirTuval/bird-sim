import pygame
import pymunk.pygame_util
import pymunk
from bird import Bird
from floor import Floor

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
DT = 1 / FPS
GRAVITY = -1000
FLOOR_HEIGHT = 10
BACKGROUND_COLOR = "white"
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, GRAVITY
draw_options = pymunk.pygame_util.DrawOptions(window)

bird = Bird(space, WIDTH / 2)
floor = Floor(space, WIDTH)

def run_simulation():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                bird.left_wing.body.apply_impulse_at_local_point((0,100),(-30,0))
                bird.right_wing.body.apply_impulse_at_local_point((0,100),(30,0))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                bird.left_wing.body.apply_impulse_at_local_point((0,-100),(-30,0))
                bird.right_wing.body.apply_impulse_at_local_point((0,-100),(30,0))


        window.fill(BACKGROUND_COLOR)
        space.debug_draw(draw_options)
        pygame.display.update()
        space.step(DT)
        clock.tick(FPS)



if __name__ == '__main__':
    run_simulation()