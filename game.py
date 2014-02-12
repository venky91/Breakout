import pygame
import math
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
            for index, column in enumerate(range(20)):
                self.array[row].append(pygame.Rect(self.left, self.top,
                    30,20,))
                self.left += 30
                if index == 19:
                    self.top += 20

    def update(self):
        if self.array == []:
            print("Game Over")
            return True
        else:
            return False

    def render(self, window):

        for row in self.array:
            for column in row:
                pygame.draw.rect(window.screen,(0,255,0), column) 

class Ball:

    UPRIGHT = False
    UPLEFT = False
    DOWNLEFT = True
    DOWNRIGHT = False
    
    SPEED_X = 3 #rate at which the ball's coordinates changes
    SPEED_Y = 3
    RADIUS = 6

    def __init__(self):
        self.x = 240
        self.y = 400
        " initialized coordinates and coordinate speed"
        
        self.circleRect = pygame.draw.circle(window.screen, (255,0,0), (self.x, self.y), self.RADIUS)

    """checks the direction of the ball and makes appropriate changes to
    direction"""
    def update(self):
        
        self.x += self.SPEED_X
        self.y += self.SPEED_Y

        if (self.x - 6) < 0:
            self.SPEED_X = -self.SPEED_X
                

        if (self.x + 6 > 500):
            self.SPEED_X = -self.SPEED_X

        if (self.y - 6 < 0):
            self.SPEED_Y = -self.SPEED_Y
    
    def checkCollision(self, paddle, matrix):
        "checks if the ball has hit the paddle"

        if (self.circleRect.colliderect(paddle.rect)):

            if self.DOWNLEFT and paddle.x < self.x and paddle.MOVINGRIGHT:
                self.SPEED_X = -self.SPEED_X
                self.SPEED_Y = -self.SPEED_Y
            
            elif self.DOWNLEFT and paddle.MOVINGLEFT == False and paddle.MOVINGRIGHT == False:
                self.SPEED_Y = -self.SPEED_Y

            elif self.DOWNRIGHT and paddle.MOVINGLEFT and  paddle.x >= self.x:
                self.SPEED_Y = -self.SPEED_Y

            elif self.DOWNRIGHT and paddle.x > self.x and paddle.MOVINGLEFT:
                self.SPEED_X = -self.SPEED_X
                self.SPEED_Y = -self.SPEED_Y
            
            elif self.DOWNRIGHT and paddle.MOVINGLEFT == False and paddle.MOVINGRIGHT == False:
                self.SPEED_Y = -self.SPEED_Y
            else:
                self.SPEED_Y = -self.SPEED_Y

        for row in matrix.array:
            for column in row:
                if self.circleRect.colliderect(column):
                    row.remove(column)
                    self.SPEED_Y = -self.SPEED_Y


    def render(self, window):
        self.circleRect = pygame.draw.circle(window.screen, (255,0,0), (self.x, self.y), self.RADIUS)

class Paddle:

    def __init__(self, window):
        self.x = (window.WINDOW_WIDTH/2) - 65
        self.y = window.WINDOW_HEIGHT - 100
        self.rect = pygame.Rect(self.x,self.y, 130, 2)
        self.moveSpeed = 4
        self.MOVINGLEFT = False

        pygame.draw.rect(window.screen,(255,255,255), ( self.rect))

    def processInput(self, pressed):
        if pressed[pygame.K_LEFT]: 
            self.MOVINGLEFT = True
            self.rect.left -= self.moveSpeed
            self.x -=self.moveSpeed
            if self.rect.left < 0:
                self.rect.left = 0
                self.x = 65
                self.MOVINGLEFT = False

        elif pressed[pygame.K_RIGHT]: 
            self.MOVINGRIGHT = True
            self.rect.left += self.moveSpeed
            self.x += self.moveSpeed
            if self.rect.right > 500:
                self.rect.right = 500
                self.x = 435
                self.MOVINGRIGHT = False

        else:
            self.MOVINGLEFT = False
            self.MOVINGRIGHT = False


    def render(self, window):
        pygame.draw.rect(window.screen,(255,255,255), self.rect) 

window = Window()
ball = Ball()
clock = pygame.time.Clock()
paddle = Paddle(window)
matrix = Block_Matrix()

start = False

ball.render(window)
matrix.render(window)
paddle.render(window)

while not start:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]:
        start = True

while not done:

    window.screen.fill((0,0,0))
    filtered_events = []

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True

        filtered_events.append(event)

    pressed = pygame.key.get_pressed() 
    paddle.processInput(pressed)
    ball.checkCollision(paddle, matrix)
    ball.update()
    ball.render(window)
    paddle.render(window)
    matrix.render(window)
    matrix.update()
    pygame.display.flip() #update screen
    clock.tick(60) #60 fps
