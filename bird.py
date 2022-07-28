import pymunk
import math

YELLOW = 255, 255, 0, 100
PI = math.pi
WING_FORCE = 300


class Bird():
    RECT_WIDTH = 50
    RECT_HEIGHT = 100
    MASS = 3
    OPACITY = 100
    COLOR = 255, 0, 0, OPACITY
    OFFSET = 10
    ELASTICITY = 0.2
    FRICTION = 0.4

    def __init__(self, space, x_location) -> None:
        self.body = pymunk.Body()
        self.body.position = x_location, self.RECT_HEIGHT / 2
        self.origin = (self.body.position, self.body.angle,
                       self.body.velocity, self.body.angular_velocity)
        self.shape = pymunk.Poly.create_box(self.body, (self.RECT_WIDTH, self.RECT_HEIGHT))
        self.shape.elasticity = self.ELASTICITY
        self.shape.friction = self.FRICTION
        self.shape.mass = self.MASS
        self.shape.color = self.COLOR
        space.add(self.body, self.shape)
        self._create_left_wing(space, x_location - self.RECT_WIDTH / 2 - Wing.WIDTH / 2)
        self._create_right_wing(space, x_location + self.RECT_WIDTH / 2 + Wing.WIDTH / 2)

    def _create_left_wing(self, space, x_location):
        self.left_wing = Wing(space, (x_location, self.RECT_HEIGHT))
        constraint_left = pymunk.PivotJoint(self.body, self.left_wing.body, (-self.RECT_WIDTH / 2 - self.OFFSET, self.RECT_HEIGHT / 2), (Wing.WIDTH / 2, 0))
        limit_left = pymunk.RotaryLimitJoint(self.body, self.left_wing.body, -PI / 2, PI)
        space.add(limit_left)
        space.add(constraint_left)

    def _create_right_wing(self, space, x_location):
        self.right_wing = Wing(space, (x_location, self.RECT_HEIGHT))
        constraint_right = pymunk.PivotJoint(self.body, self.right_wing.body, (self.RECT_WIDTH / 2 + self.OFFSET, self.RECT_HEIGHT / 2), (-Wing.WIDTH / 2, 0))
        limit_right = pymunk.RotaryLimitJoint(self.body, self.right_wing.body, -PI, PI / 2)
        space.add(limit_right)
        space.add(constraint_right)

    def re_origin(self):
        (self.body.position, self.body.angle,
         self.body.velocity, self.body.angular_velocity) = self.origin
        self.left_wing.re_origin()
        self.right_wing.re_origin()

    def left_wing_down(self):
        self.left_wing.down()
        if self._is_left_wing_pos_valid_for_force_application():
            self.body.apply_impulse_at_local_point((100,1000), (0,0))

    def right_wing_down(self):
        self.right_wing.down()
        if self._is_left_wing_pos_valid_for_force_application():
            self.body.apply_impulse_at_local_point((-100,1000), (0,0))

    def left_wing_up(self):
        self.left_wing.up()

    def right_wing_up(self):
        self.right_wing.up()
    
    def _is_left_wing_pos_valid_for_force_application(self):
        return self.left_wing.body.angle < 0.7

    def _is_right_wing_pos_valid_for_force_application(self):
        return self.right_wing.body.angle > -0.7

class Wing():
    WIDTH = 60
    HEIGHT = 6
    MASS = 1

    def __init__(self, space, position) -> None:
        self.body = pymunk.Body()
        self.body.position = position
        self.origin = (self.body.position, self.body.angle,
                       self.body.velocity, self.body.angular_velocity)
        self.shape = pymunk.Segment(self.body, (0 - self.WIDTH / 2, 0),
                                    (self.WIDTH / 2, 0), self.HEIGHT)
        self.shape.mass = self.MASS
        self.shape.friction = 0.7
        self.shape.color = YELLOW
        space.add(self.body, self.shape)

    def down(self):
        self.body.apply_impulse_at_local_point((0, -WING_FORCE*3), (0, 0))

    def up(self):
        self.body.apply_impulse_at_local_point((0, WING_FORCE*3), (0, 0))

    def re_origin(self):
        (self.body.position, self.body.angle,
         self.body.velocity, self.body.angular_velocity) = self.origin
