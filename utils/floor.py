import pymunk
from utils.constants import *
import pygame


class Floor():
    HEIGHT = 60
    ELASTICITY = 0.9
    FRICTION = 0.9
    COLOR = BROWN
    AREA_FACTOR = 100

    def __init__(self, space, space_width) -> None:
        self.image = pygame.image.load('../assets/floor.jpg')
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = space_width / 2, -self.HEIGHT/2
        self.shape = pymunk.Poly.create_box(self.body, (space_width * self.AREA_FACTOR, self.HEIGHT))
        self.shape.elasticity = self.ELASTICITY
        self.shape.friction = self.FRICTION
        self.shape.color = self.COLOR
        space.add(self.body, self.shape)

    def render(self, screen: pygame.Surface, bird_hight):

        screen_width, screen_hight = screen.get_size()
        image_to_display = pygame.transform.scale(self.image, (screen_width, screen_hight/2 ))
        screen.blit(image_to_display, (0,376 + bird_hight))