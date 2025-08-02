import pygame
import random
import math
from load import *

Fifty = 50/1536*WIDTH # 这里1536
Thirty = 30/1536*WIDTH

class Ball:
    def __init__(self,x:int, y:int,test_y:int, state: int):
        self.x = x
        self.y = y
        self.speed = get_speed(state)
        self.length = 10/1536*WIDTH
        self.test_y = test_y
        self.img = pygame.transform.scale(circle_img, (Fifty, Fifty))


    def draw(self,window: pygame.Surface):

        window.blit(self.img,(self.x,self.y))
    
        # 画框
        pygame.draw.circle(window,(255,255,255),(self.x+Fifty/2, self.test_y+Fifty/2), Fifty/2, 4)

    def update(self):
        self.y += self.speed

    def check(self):
        if abs(self.y - self.test_y) < 20:
            return 2
        elif abs(self.y - self.test_y) < 40:
            return 1
        return 0
    
    def is_out_of_line(self):
        return self.y - self.test_y > 40
        
class LONGBALL:
    def __init__(self,x:int, y:int,length:int,test_y:int, state: int):
        '''
        length: 长度
        test_y: 测试点
        '''
        self.x = x
        self.y = y
        self.speed = get_speed(state)
        # print(length)
        self.length = length
        self.test_y = test_y
        self.win = False
        self.img = pygame.transform.scale(long_ball_img, (Fifty, self.length))
        self.img_up = pygame.transform.scale(long_ball_up, (Fifty, Fifty/2))
        self.img_down = pygame.transform.scale(long_ball_down, (Fifty, Fifty/2))
        self.start = False
        self.ischeck = False
        self.score = 0
        self.total_length = self.length
        
    def draw(self,window: pygame.Surface):
        window.blit(self.img_up,(self.x,self.y-Fifty/2))
        window.blit(self.img,(self.x,self.y))
        window.blit(self.img_down,(self.x,self.y+self.length))
        pygame.draw.circle(window,(255,255,255),(self.x+Fifty/2, self.test_y+Fifty/2), Fifty/2, 4)
    

    def update(self):
        self.y += self.speed
        if self.y + self.length >= self.test_y + Fifty/2:
            if self.test_y - self.y + Fifty/2> 0:
                self.img = pygame.transform.scale(long_ball_img, (Fifty, self.test_y - self.y + Fifty/2))
                self.length = self.test_y - self.y + Fifty/2
                
    def check(self):
        if abs(self.y - self.test_y + self.total_length - Fifty/2) < 20:
            return 2
        elif abs(self.y - self.test_y + self.total_length - Fifty/2) < 40:
            return 1
        return 0
        
    def is_out_of_line(self):
        return self.y - self.test_y > Fifty // 2 + 20
    
class RaindropBall:
    def __init__(self,x:int, y:int, radius:int, test_y:int, state: int):
        '''
        radius: 半径
        test_y: 测试点
        '''
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = get_speed(state)
        self.test_y = test_y
        self.img = pygame.transform.scale(rains_img, (Thirty, Thirty/2+Thirty/2*math.sqrt(3)))

        
    def draw(self,window: pygame.Surface):
        window.blit(self.img,(self.x+Fifty/5,self.y))
        pygame.draw.circle(window, (255, 255, 255), (self.x + Fifty/2, self.test_y + Fifty/2), Fifty/2, 4)


    def update(self):
        self.y += self.speed
        
    def check(self):
        if abs(self.y - self.test_y) < 10:
            return 1
        return 0

    def is_out_of_line(self):
        return self.y - self.test_y > 10
    
# 定义粒子类
class Particle:
    def __init__(self,x: int, y: int, color: tuple):
        self.x = x
        self.y = y
        self.vx = (random.random() - 0.5) * 10
        self.vy = (random.random() - 0.5) * 10
        self.size = random.random() * 15 + 2
        self.color = color
    

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.size *= 0.95

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)

    def is_out_of_line(self):
        return self.size < 1

def make_particles(x,y,color):
    return [Particle(x,y,color) for _ in range(20)]