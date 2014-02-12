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
        self.array = [[]]

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
    pygame.display.flip()
    clock.tick(60)
