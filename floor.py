import pymunk
from constants import *



class Floor():
    HEIGHT = 60
    ELASTICITY = 0.9
    FRICTION = 0.9
    COLOR = BROWN
    AREA_FACTOR = 100

    def __init__(self, space, space_width) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = space_width / 2, -self.HEIGHT/2
        self.shape = pymunk.Poly.create_box(self.body, (space_width * self.AREA_FACTOR, self.HEIGHT))
        self.shape.elasticity = self.ELASTICITY
        self.shape.friction = self.FRICTION
        self.shape.color = self.COLOR
        space.add(self.body, self.shape)
