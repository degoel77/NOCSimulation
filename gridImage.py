import sys
#sys.path.insert(0, '/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages')

import pygame
from pygame.locals import *

class gridImage:
    def __init__ (self, xMax, yMax):
        self.GRID_SIZE_X = xMax
        self.GRID_SIZE_Y = yMax
        self.circle_key = {}
        self.circle_num = 0
        # set up pygame
        pygame.init()
        self.windowSurface = pygame.display.set_mode(((xMax * 125), yMax * 125), 0, 32)
        self.windowSurface.fill([0,0,0])
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0 , 0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.PURPLE = (255,0,255)
        self.X = 100
        self.Y = 100
        self.basicFont = pygame.font.SysFont(None, 18)
        # draw circles
        for i in range(self.GRID_SIZE_X):
            for j in range(self.GRID_SIZE_Y):
                pygame.draw.circle(self.windowSurface, self.WHITE, ((i + 1) * self.X , (xMax * 125) - ((j + 1) * self.Y)), 25, 4)
                self.circle_key["Circle " + str(self.circle_num)] = ((i + 1) * self.X , (xMax * 125)- ((j + 1) * self.Y))
                self.circle_num += 1
        # draw horizontal lines
        for i in range(self.GRID_SIZE_X - 1):
            for j in range(self.GRID_SIZE_Y):
                pygame.draw.line(self.windowSurface, self.WHITE, (((i + 1) * self.X) + 21, ((xMax * 125) -(j + 1) * self.Y)),
                                 (((i+2) * self.X) - 21, (xMax * 125) - ((j + 1) * self.Y)), 4)

        # draw vertical lines
        for i in range(self.GRID_SIZE_X):
            for j in range(self.GRID_SIZE_Y - 1):
                pygame.draw.line(self.windowSurface, self.WHITE, ((i + 1) * self.X, (xMax * 125) - (((j + 1) * self.Y) + 21)),
                                 (((i + 1) * self.X), (xMax * 125) - (((j + 2) * self.Y) - 21)), 4)

    def circle_write(self, circle_num, object):
        circle_cord = self.circle_key.get("Circle " + str(circle_num))
        text = self.basicFont.render(str(object), True, self.WHITE, (0,0,0))
        textRect = text.get_rect()
        textRect.centerx = circle_cord[0]
        textRect.centery = circle_cord[1]
        self.windowSurface.blit(text, textRect)


    def line_write(self, circle_num1, direction, changeColor, object):
        color = self.GREEN
        if changeColor:
            color = self.RED
        if direction == "N":
            circle_num2 = circle_num1 + 1
            xOfst = 10
            yOfst = -10
        if direction == "E":
            circle_num2 = circle_num1 + self.GRID_SIZE_Y
            xOfst = 10
            yOfst = -10
        if direction == "S":
            circle_num2 = circle_num1 - 1
            xOfst = -10
            yOfst = 10
        if direction == "W":
            circle_num2 = circle_num1 - self.GRID_SIZE_Y
            xOfst = -10
            yOfst = 10
        circle_cord1 = self.circle_key.get("Circle " + str(circle_num1))
        if circle_num2 >= 0 and circle_num2 <= (self.GRID_SIZE_X * self.GRID_SIZE_Y) - 1 :
            circle_cord2 = self.circle_key.get("Circle " + str(circle_num2))
            text = self.basicFont.render(str(object), True, color, (0,0,0))
            textRect = text.get_rect()
            textRect.centerx = (circle_cord1[0] + circle_cord2[0])/2 + xOfst
            textRect.centery = (circle_cord1[1] + circle_cord2[1])/2 + yOfst
            if direction == "N":
                if (circle_cord2[1] - circle_cord1[1]) < 125:
                    self.windowSurface.blit(text, textRect)
            elif direction == "S":
                if (circle_cord1[1] - circle_cord2[1]) < 125:
                    self.windowSurface.blit(text, textRect)
            else:
                self.windowSurface.blit(text, textRect)

    def run(self):
        pygame.display.update()
        # run the game loop
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
