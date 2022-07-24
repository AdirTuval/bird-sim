import pymunk
from pymunk import Vec2d

BIRD_RECT_WIDTH = 50
BIRD_RECT_HEIGHT = 100
ELASTICITY = 0.2
FRICTION = 0.4
BIRD_MASS = 20
BIRD_OPACITY = 100
BIRD_COLOR = 255, 0 ,0, BIRD_OPACITY
WING_WIDTH = 60
WING_MASS = 1

class Bird():
    def __init__(self, space, x_location) -> None:
        self.body = pymunk.Body()
        self.body.position = x_location, BIRD_RECT_HEIGHT/2
        self.shape = pymunk.Poly.create_box(self.body, (BIRD_RECT_WIDTH, BIRD_RECT_HEIGHT))
        self.shape.elasticity = ELASTICITY
        self.shape.friction = FRICTION
        self.shape.mass = BIRD_MASS
        self.shape.color = BIRD_COLOR
        space.add(self.body, self.shape)
        self.create_left_wing(space, x_location - BIRD_RECT_WIDTH/2 - WING_WIDTH/2)
        self.create_right_wing(space, x_location + BIRD_RECT_WIDTH/2 + WING_WIDTH/2)

    def create_left_wing(self, space, x_location):
        self.left_wing = Wing(space, (x_location, BIRD_RECT_HEIGHT))
        c = pymunk.PivotJoint(self.body, self.left_wing.body, (-BIRD_RECT_WIDTH/2-5,BIRD_RECT_HEIGHT/2), (WING_WIDTH/2,0))
        space.add(c)

    def create_right_wing(self, space, x_location):
        self.right_wing = Wing(space, (x_location, BIRD_RECT_HEIGHT))
        c = pymunk.PivotJoint(self.body, self.right_wing.body, (BIRD_RECT_WIDTH/2+5 ,BIRD_RECT_HEIGHT/2), (-WING_WIDTH/2,0))
        space.add(c)


class Wing():
    def __init__(self, space, position) -> None:
        self.body = pymunk.Body()
        self.body.position = position
        self.shape = pymunk.Segment(self.body, (0-WING_WIDTH/2,0), (WING_WIDTH/2,0), 6)
        self.shape.mass = WING_MASS
        self.shape.friction = 0.7
        space.add(self.body, self.shape)
