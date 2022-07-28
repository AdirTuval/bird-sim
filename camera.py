import pygame
import pymunk.pygame_util
import pymunk
from constants import *

class Camera:
    def __init__(self, draw_options, bird, width, height ):
        self.translation = pymunk.Transform()
        self.scaling = 0.8
        self.draw_options = draw_options
        self.bird = bird
        self.last_position = self.bird.body.position
        self.width = width
        self.height = height
    
    def update(self):    
        keys = pygame.key.get_pressed()
        zoom_in = int(keys[pygame.K_a])
        zoom_out = int(keys[pygame.K_z])


        self.translation = self.translation.translated(
            self.get_position_delta_of(0),
            self.get_position_delta_of(1)
        )

        self.scaling *= 1 + (ZOOM_SPEED * zoom_in - ZOOM_SPEED * zoom_out)

        # to zoom with center of screen as origin we need to offset with
        # center of screen, scale, and then offset back
        self.draw_options.transform = (
            pymunk.Transform.translation(self.width / 2, self.height / 2)
            @ pymunk.Transform.scaling(self.scaling)
            @ self.translation
            @ pymunk.Transform.translation(-self.width / 2, -self.height / 2)
        )
        self.last_position = self.bird.body.position

    def get_position_delta_of(self, cord):
        return self.last_position[cord] - self.bird.body.position[cord]
