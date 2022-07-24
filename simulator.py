import pygame
import pymunk.pygame_util
import pymunk
from bird import Bird
from floor import Floor

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
DT = 1 / FPS
GRAVITY = 1000
FLOOR_HEIGHT = 10
BACKGROUND_COLOR = "white"
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, GRAVITY
draw_options = pymunk.pygame_util.DrawOptions(window)

bird = Bird(position=(WIDTH/2, HEIGHT-100), space=space)
floor = Floor(space, WIDTH, HEIGHT)

def run_simulation():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        window.fill(BACKGROUND_COLOR)
        space.debug_draw(draw_options)
        pygame.display.update()
        space.step(DT)
        clock.tick(FPS)



if __name__ == '__main__':
    run_simulation()