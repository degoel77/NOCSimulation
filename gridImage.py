import os
import sys

import pygame
from pygame.locals import *


# sys.path.insert(0, '/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages')


class gridImage:
    def __init__(self, xMax, yMax):
        self.GRID_SIZE_X = xMax
        self.GRID_SIZE_Y = yMax
        self.circle_key = {}
        self.circle_num = 0
        # set up pygame
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        info = pygame.display.Info()
        self.size = info.current_h - 100
        self.windowSurface = pygame.display.set_mode((self.size, self.size))
        self.windowSurface.fill([0, 0, 0])
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (255, 0, 255)
        self.margin = 25
        self.cellWidthX = (self.size - 2 * self.margin) / self.GRID_SIZE_X
        self.cellWidthY = (self.size - 2 * self.margin) / self.GRID_SIZE_Y
        self.circleRadius = (self.cellWidthX + self.cellWidthY) / 10
        self.lineWidth = 4
        print(f"SELF.CELLWIDTHX = {self.cellWidthY}")
        self.X = 100
        self.Y = 100
        self.basicFont = pygame.font.SysFont(None, int(self.size / 50))
        # draw circles
        for i in range(self.GRID_SIZE_X):
            for j in range(self.GRID_SIZE_Y):
                print((self.margin + i * self.cellWidthX,
                       self.margin + j * self.cellWidthY))
                pygame.draw.circle(self.windowSurface, self.WHITE,
                                   (self.margin + (i + 0.5) * self.cellWidthX,
                                    self.margin + (j + 0.5) * self.cellWidthY),
                                   self.circleRadius, self.lineWidth)
                self.circle_key["Circle " + str(self.circle_num)] = (self.margin + (i + 0.5) * self.cellWidthX,
                                                                     self.margin + (j + 0.5) * self.cellWidthY)
                self.circle_num += 1
        # draw horizontal lines
        for i in range(self.GRID_SIZE_X - 1):
            for j in range(self.GRID_SIZE_Y):
                startPos = (self.margin + (i + 0.5) * self.cellWidthX + self.circleRadius,
                            self.margin + (j + 0.5) * self.cellWidthY)
                finalPos = (self.margin + (i + 1.5) * self.cellWidthX - self.circleRadius,
                            self.margin + (j + 0.5) * self.cellWidthY)
                pygame.draw.line(self.windowSurface,
                                 self.WHITE, startPos, finalPos, self.lineWidth)

        # draw vertical lines
        for i in range(self.GRID_SIZE_X):
            for j in range(self.GRID_SIZE_Y - 1):
                startPos = (self.margin + (i + 0.5) * self.cellWidthX,
                            self.margin + (j + 0.5) * self.cellWidthY + self.circleRadius)
                finalPos = (self.margin + (i + 0.5) * self.cellWidthX,
                            self.margin + (j + 1.5) * self.cellWidthY - self.circleRadius)
                pygame.draw.line(self.windowSurface,
                                 self.WHITE, startPos, finalPos, self.lineWidth)

    def circle_write(self, circle_num, object):
        circle_cord = self.circle_key.get("Circle " + str(circle_num))
        text = self.basicFont.render(str(object), True, self.WHITE, (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = circle_cord[0]
        textRect.centery = circle_cord[1]
        self.windowSurface.blit(text, textRect)

    def line_write(self, circle_num1, direction, changeColor, object):
        margin = self.circleRadius/2
        color = self.GREEN
        if changeColor:
            color = self.RED
        if direction == "N":
            circle_num2 = circle_num1 + 1
        elif direction == "E":
            circle_num2 = circle_num1 + self.GRID_SIZE_Y
        elif direction == "S":
            circle_num2 = circle_num1 - 1
        elif direction == "W":
            circle_num2 = circle_num1 - self.GRID_SIZE_Y
        circle_cord1 = self.circle_key.get("Circle " + str(circle_num1))
        if circle_num2 >= 0 and circle_num2 <= (self.GRID_SIZE_X * self.GRID_SIZE_Y) - 1:
            circle_cord2 = self.circle_key.get("Circle " + str(circle_num2))
            text = self.basicFont.render(str(object), True, color, (0, 0, 0))
            textRect = text.get_rect()
            if direction == "N":
                textRect.left = circle_cord1[0] + margin
                textRect.centery = (
                    circle_cord1[1] + circle_cord2[1])/2 - margin
            elif direction == "E":
                textRect.bottom = circle_cord1[1] - margin
                textRect.centerx = (
                    circle_cord1[0] + circle_cord2[0])/2 - margin
            elif direction == "S":
                textRect.right = circle_cord1[0] - margin
                textRect.centery = (
                    circle_cord1[1] + circle_cord2[1])/2 + margin
            elif direction == "W":
                textRect.top = circle_cord1[1] + margin
                textRect.centerx = (
                    circle_cord1[0] + circle_cord2[0])/2 + margin
            self.windowSurface.blit(text, textRect)

    def run(self):
        pygame.display.update()
        pygame.image.save(self.windowSurface, "NOCImage.png")
        # run the game loop
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
