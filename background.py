import pygame

class Background():
      def __init__(self,displaySurf):
            self.displaySurf = displaySurf
            self.bgimage = pygame.image.load('assets/bg.jfif')
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = self.rectBGimg.height
            self.bgX2 = 0
 
            self.moving_speed = 1
         
      def update(self):
        self.bgY1 -= self.moving_speed
        self.bgY2 -= self.moving_speed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height
             
      def render(self):
         self.displaySurf.blit(self.bgimage, (self.bgX1, self.bgY1))
         self.displaySurf.blit(self.bgimage, (self.bgX1+self.rectBGimg.width, self.bgY1))
         
         self.displaySurf.blit(self.bgimage, (self.bgX2, self.bgY2))
         self.displaySurf.blit(self.bgimage, (self.bgX2+self.rectBGimg.width, self.bgY2))