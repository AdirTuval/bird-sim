import pymunk

BIRD_RECT_WIDTH = 50
BIRD_RECT_HEIGHT = 100
ELASTICITY = 0.2
FRICTION = 0.4
BIRD_MASS = 1
BIRD_OPACITY = 100
BIRD_COLOR = 255, 0 ,0, BIRD_OPACITY

class Bird():
    def __init__(self, position, space) -> None:
        self.body = pymunk.Body()
        self.body.position = position
        self.shape = pymunk.Poly.create_box(self.body, (BIRD_RECT_WIDTH, BIRD_RECT_HEIGHT))
        self.shape.elasticity = ELASTICITY
        self.shape.friction = FRICTION
        self.shape.mass = BIRD_MASS
        self.shape.color = BIRD_COLOR
        space.add(self.body, self.shape)
