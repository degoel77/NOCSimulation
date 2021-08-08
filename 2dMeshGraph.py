#import sys
#sys.path.insert(0, '/Users/deepakgoel/Library/Python/3.7/lib/python/site-packages')

##import pygame
##from pygame.locals import *
##
### set up pygame
##pygame.init()
##windowSurface = pygame.display.set_mode((800, 600))
##surf1 = pygame.Surface((800,600))
###BLACK = (255, 255, 255)
##BLACK = (0, 255, 0)
##X = 75
##Y = 75
##GRID_SIZE_X = 1
##GRID_SIZE_Y = 1
##for i in range(GRID_SIZE_X):
##    for j in range(GRID_SIZE_Y):
##        pygame.draw.circle(surf1, BLACK, ((i + 1) * X, (j + 1) * Y), 4,1)
###for i in range(GRID_SIZE_X - 1):
###    for j in range(GRID_SIZE_Y):
###        pygame.draw.line(windowSurface, BLACK, (((i + 1) * X) + 21, (j + 1) * Y), (((i+2) * X) - 21, (j + 1) * Y), 4)
###for i in range(GRID_SIZE_X):
###    for j in range(GRID_SIZE_Y - 1):
###        pygame.draw.line(windowSurface, BLACK, ((i + 1) * X, (((j + 1) * Y) + 21)), (((i + 1) * X), ((j + 2) * Y) - 21), 4)
##
##windowSurface.blit(surf1, (0,0))
### run the game loop
##while True:
##    pygame.display.update()
##    for event in pygame.event.get():
##        if event.type == QUIT:
##            pygame.quit()
##            sys.exit()
import pygame, sys

pygame.init()
width  = 400
height = 400
screen = pygame.display.set_mode((width, height))
surf1 = pygame.Surface((width,height))
surf1.fill((0,255,0))
pygame.draw.circle(surf1, (0,0,0), (200,200), 5)
screen.blit(surf1, (0,0))
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
pygame.quit()
