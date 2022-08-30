import imp
from turtle import right
from typing import Union, Tuple
import pymunk
from pymunk import Vec2d
import pygame
from constants import *
from draw_blits import blitRotate
import math 
# BodyState = namedtuple('BodyState', 'position angle velocity angular_velocity')
LEFT = 'left'
RIGHT = 'right'

class BodyState:
    def __init__(self, position: Vec2d, angle: float, velocity: Vec2d, angular_velocity: float):
        self.position = position
        self.angle = angle
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.pointing_direction = Vec2d(1, 0).rotated(angle)

    def __getitem__(self, item):
        return (self.position, self.angle, self.velocity, self.angular_velocity)[item]


class BirdState:
    def __init__(self, body_state: BodyState, left_wing_state: BodyState, right_wing_state: BodyState):
        self.body_state: BodyState = body_state
        self.left_wing_state: BodyState = left_wing_state
        self.right_wing_state: BodyState = right_wing_state

    @property
    def body(self):
        return self.body_state

    @property
    def left_wing(self):
        return self.left_wing_state

    @property
    def right_wing(self):
        return self.right_wing_state

    @property
    def x(self):
        return self.body.position[0]

    @property
    def y(self):
        return self.body.position[1]

    @property
    def altitude(self):
        return self.y


class Bird():
    IMAGE_SIZE = 150
    WIDTH = 50
    HEIGHT = 100
    MASS = 5
    OPACITY = 100
    COLOR = RED
    OFFSET = 10
    ELASTICITY = 0.2
    FRICTION = 0.8

    def __init__(self, space: pymunk.Space, x_location: float) -> None:
        self.image = pygame.image.load('assets/bod.png')
        self.image = pygame.transform.scale(self.image, (self.IMAGE_SIZE, self.IMAGE_SIZE))
        self.body = pymunk.Body()
        self.body.position = x_location, self.HEIGHT / 2
        self.origin = BodyState(self.body.position, self.body.angle, self.body.velocity, self.body.angular_velocity)
        self.shape = pymunk.Poly.create_box(self.body,self.size)
        self.shape.elasticity = self.ELASTICITY
        self.shape.friction = self.FRICTION
        self.shape.mass = self.MASS
        self.shape.color = self.COLOR
        space.add(self.body, self.shape)
        self._create_left_wing(space, x_location - self.WIDTH / 2 - Wing.WIDTH / 2)
        self._create_right_wing(space, x_location + self.WIDTH / 2 + Wing.WIDTH / 2)

    def render(self, screen):
        image_to_display = self.image.copy()
        self.right_wing.render(image_to_display,self.angle_deg)
        self.left_wing.render(image_to_display,self.angle_deg)
        w, h = image_to_display.get_size()
        blitRotate(screen, image_to_display, (400,350), (w/2, h/2), self.angle_deg)

    @property
    def angle_deg(self) -> float:
        return math.degrees(self.body.angle)


    @property
    def x(self) -> float:
        return self.body.position[0]

    @property
    def y(self) -> float:
        return self.body.position[1]

    @property
    def position(self) -> Vec2d:
        return self.body.position

    @property
    def size(self):
        return (self.WIDTH, self.HEIGHT)
    
    
    @property
    def angle(self) -> float:
        return self.body.angle
    

    @property
    def velocity(self) -> Vec2d:
        return self.body.velocity

    @property
    def angular_velocity(self) -> float:
        return self.body.angular_velocity

    @property
    def mass(self) -> float:
        return self.shape.mass

    def get_state(self) -> BirdState:
        body_state = BodyState(self.position, self.angle, self.velocity, self.angular_velocity)
        left_wing_state = BodyState(self.position, self.angle, self.velocity, self.angular_velocity)
        right_wing_state = BodyState(self.position, self.angle, self.velocity, self.angular_velocity)
        return BirdState(body_state, left_wing_state, right_wing_state)

    def tail_position(self) -> Vec2d:
        return self.body.position + Vec2d(0, -self.HEIGHT / 2).rotated(self.body.angle)

    def _create_left_wing(self, space, x_location):
        self.left_wing = Wing(space, (x_location, self.HEIGHT), LEFT, self.IMAGE_SIZE)
        constraint_left = pymunk.PivotJoint(self.body, self.left_wing.body,
                                            (-self.WIDTH / 2 - self.OFFSET, self.HEIGHT / 2), (Wing.WIDTH / 2, 0))
        limit_left = pymunk.RotaryLimitJoint(self.body, self.left_wing.body, -50 * PI / 180, PI)
        space.add(limit_left)
        space.add(constraint_left)

    def _create_right_wing(self, space, x_location):
        self.right_wing = Wing(space, (x_location, self.HEIGHT), RIGHT, self.IMAGE_SIZE)
        constraint_right = pymunk.PivotJoint(self.body, self.right_wing.body,
                                             (self.WIDTH / 2 + self.OFFSET, self.HEIGHT / 2), (-Wing.WIDTH / 2, 0))
        limit_right = pymunk.RotaryLimitJoint(self.body, self.right_wing.body, -PI, 50 * PI / 180)
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
            self.body.apply_force_at_local_point((100, 20000), (0, 0))

    def right_wing_down(self):
        self.right_wing.down()
        if self._is_right_wing_pos_valid_for_force_application():
            self.body.apply_force_at_local_point((-100, 20000), (0, 0))

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
    WING_AREA = WIDTH * HEIGHT
    MASS = 2
    STRENGTH_UP = 3000
    STRENGTH_DOWN = 0
    FRICTION = 0.7
    ELASTICITY = 0.2

    def __init__(self, space: pymunk.Space, position: Union[pymunk.vec2d.Vec2d, Tuple[float, float]], side:str, bird_size) -> None:
        self.body = pymunk.Body()
        self.side = side
        self.bird_size = bird_size
        self.image = pygame.image.load(f'assets/{side}_wing.png')
        
        if side == LEFT:
            self.image = pygame.transform.scale(self.image, (self.bird_size*0.3, self.bird_size*0.15))
        if side == RIGHT:
            self.image = pygame.transform.scale(self.image, (self.bird_size*0.3, self.bird_size*0.15))
        self.body.position = position
        self.origin = BodyState(self.body.position, self.body.angle,
                                self.body.velocity, self.body.angular_velocity)
        self.shape = pymunk.Segment(self.body, (0 - self.WIDTH / 2, 0),
                                    (self.WIDTH / 2, 0), self.HEIGHT)
        self.shape.mass = self.MASS
        self.shape.elasticity = self.ELASTICITY
        self.shape.friction = self.FRICTION
        self.shape.color = YELLOW
        space.add(self.body, self.shape)

    def render(self, screen,angle_offset):
        w, h = self.image.get_size()
        s = self.bird_size/100
        angle = self.angle_deg
        if self.side == RIGHT:

            blitRotate(screen, self.image, (s * 77, s * 30), (w/8, h/3), angle-angle_offset)
        else:
            blitRotate(screen, self.image, (s * 22,s * 30), (6*w/8, h/3), angle-angle_offset)

    @property
    def angle_deg(self) -> float:
        return math.degrees(self.body.angle)



    def down(self):
        self.body.apply_force_at_local_point((0, self.STRENGTH_DOWN))

    def up(self):
        self.body.apply_force_at_local_point((0, self.STRENGTH_UP))

    def re_origin(self):
        (self.body.position, self.body.angle,
         self.body.velocity, self.body.angular_velocity) = self.origin
