from collections import namedtuple
from itertools import product
import pygame
Point = namedtuple("Point", ["x", "y"])
class Background():
      def __init__(self,displaySurf):
            self.displaySurf = displaySurf
            self.bgimage = pygame.image.load('assets/bg.jfif')
            self.rectBGimg = self.bgimage.get_rect()
            self.rects_to_draw = []
         
      def update(self,center_of_intrest):
            w,h = self.rectBGimg.width, self.rectBGimg.height
            CAM_FOV_PAD = 200
            left_limit = int(center_of_intrest[0] - CAM_FOV_PAD)
            left_limit = left_limit // w * w # round to nearest multiple of bg width
            bottom_limit = int(center_of_intrest[1] - CAM_FOV_PAD)
            bottom_limit = bottom_limit // h * h # round to nearest multiple of bg height
            
            self.rects_to_draw = []
            for i,j in product(range(3),range(3)):
                  self.rects_to_draw.append(Point(i*w, j*h))
      
             
      def render(self):
         for point in self.rects_to_draw:
            self.displaySurf.blit(self.bgimage, (point.x, point.y))
