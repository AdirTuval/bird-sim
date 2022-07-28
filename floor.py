import pymunk

FLOOR_HEIGHT = 10
FLOOR_ELASTICITY = 0.9
FLOOR_FRICTION = 0.4

class Floor():
    def __init__(self, space, space_width) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = space_width/2, (FLOOR_HEIGHT/2)
        self.shape = pymunk.Poly.create_box(self.body, (space_width * 10, FLOOR_HEIGHT))
        self.shape.elasticity = FLOOR_ELASTICITY
        self.shape.friction = FLOOR_FRICTION
        space.add(self.body, self.shape)