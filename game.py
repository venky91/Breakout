import pygame
import os

pygame.init()

done = False

class Window:

    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 500

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT))

class Block_Matrix:

    def __init__(self):
        self.array = []
        self.top = 0
        for row in range(8):
            self.left = 0
            self.array.append([])
            for index, column in enumerate(range(6)):
                self.array[row].append(pygame.Rect(self.left, self.top,
                    100,20,))
                self.left += 100
                if index == 5:
                    self.top += 20

    def render(self, window):

        for row, x in enumerate(range(8)):
            for column, x in enumerate(range(6)):
                pygame.draw.rect(window.screen,(0,255,0),
                        self.array[row][column]) 


class Ball:

    UPRIGHT = False
    UPLEFT = True
    DOWNLEFT = False
    DOWNRIGHT = False
    
    SPEED = 2 #rate at which the ball's coordinates changes
    RADIUS = 6

    def __init__(self):
        self.x = 240
        self.y = 400
        self.speedX = 0
        self.speedY = 0
        " initialized coordinates and coordinate speed"

    """checks the direction of the ball and makes appropriate changes to
    direction"""
    def update(self):
        
        if self.UPRIGHT:
            self.x += self.SPEED
            self.y -= self.SPEED
        if self.UPLEFT:
            self.x -= self.SPEED
            self.y -= self.SPEED
        if self.DOWNLEFT:
            self.x -= self.SPEED
            self.y += self.SPEED
        if self.DOWNRIGHT:
            self.x += self.SPEED
            self.y += self.SPEED

        if (self.x - 6) < 0:
            if self.DOWNLEFT:
                self.DOWNLEFT = False
                self.DOWNRIGHT = True
            elif self.UPLEFT:
                self.UPLEFT = False
                self.UPRIGHT = True

        if (self.x + 6 > 500):
            if self.DOWNRIGHT:
                self.DOWNRIGHT = False
                self.DOWNLEFT = True
            elif self.UPRIGHT:
                self.UPRIGHT = False
                self.UPLEFT = True

        if (self.y - 6 < 0):
            if self.UPLEFT:
                self.UPLEFT = False
                self.DOWNLEFT = True
            elif self.UPRIGHT:
                self.UPRIGHT = False
                self.DOWNRIGHT = True

    def render(self, window):
        pygame.draw.circle(window.screen, (255,0,0), (self.x, self.y), self.RADIUS)

class Paddle:

    def __init__(self, window):
        self.x = (window.WINDOW_WIDTH/2) - 65
        self.y = window.WINDOW_HEIGHT - 100
        self.rect = pygame.Rect(self.x,self.y, 130, 2)
        self.moveSpeed = 4
        pygame.draw.rect(window.screen,(255,255,255), ( self.rect))

    def processInput(self, pressed):
        if pressed[pygame.K_LEFT]: 
            self.rect.left -= self.moveSpeed
            if self.rect.left < 0:
                self.rect.left = 0

        if pressed[pygame.K_RIGHT]: 
            self.rect.left += self.moveSpeed
            if self.rect.right > 500:
                self.rect.right = 500


    def render(self, window):
        pygame.draw.rect(window.screen,(255,255,255), self.rect) 

window = Window()
ball = Ball()
clock = pygame.time.Clock()
paddle = Paddle(window)
matrix = Block_Matrix()

while not done:

    window.screen.fill((0,0,0))
    filtered_events = []

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True

        filtered_events.append(event)

    pressed = pygame.key.get_pressed() 
    paddle.processInput(pressed)
    ball.update()
    ball.render(window)
    paddle.render(window)
    matrix.render(window)
    pygame.display.flip() #update screen
    clock.tick(60) #60 fps
