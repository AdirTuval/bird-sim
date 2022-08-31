from collections import namedtuple
from itertools import product
import pygame

Point = namedtuple("Point", ["x", "y"])
BACKGROUD_SLOW_FACTOR = 0.2

class Background():
    i = 0
    def __init__(self, displaySurf):
        self.displaySurf = displaySurf
        self.bgimage = pygame.image.load('../assets/bg.jfif')
        self.rectBGimg = self.bgimage.get_rect()
        self.rects_to_draw = []

    def update(self, center_of_intrest):
        center_of_intrest *= BACKGROUD_SLOW_FACTOR
        w, h = self.rectBGimg.width, self.rectBGimg.height
        # CAM_FOV_PAD = 200
        left_limit = int(center_of_intrest[0])# - CAM_FOV_PAD)
        left_limit = left_limit % w  # round to nearest multiple of bg width
        bottom_limit = int(center_of_intrest[1])# - CAM_FOV_PAD)
        bottom_limit = bottom_limit % h  # round to nearest multiple of bg height

        self.i += 1
        self.i %= 100
        # if self.i == 0: #uncoment for debuuging
        #     print(bottom_limit, left_limit)

        self.rects_to_draw = []
        for i, j in product([0,1,2], [-1,0,1]):
            self.rects_to_draw.append(Point(i * w - left_limit, j * h + bottom_limit))

    def render(self):
        for point in self.rects_to_draw:
            self.displaySurf.blit(self.bgimage, (point.x, point.y))
