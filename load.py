import random
import threading
import os
import time
import pygame
from method import load_from_json
from pynput.keyboard import Key, Controller
from userData import *

pygame.init()

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
clock = pygame.time.Clock()
fps = 60
speed = 5/1536*WIDTH

musics = load_from_json("music_data/music_path.json")
music_names =  list(musics.keys())
start_video = []
enter_video = []
switch_video = []

for file in os.listdir('./enter'):
    path = "./enter/"+file
    enter_video.append(pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT)))
              
for file in os.listdir('./start'):
    path = "./start/"+file
    start_video.append([pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT)),False])
    
start_video[0][1] = True    
start_video[30][1] = True    
start_video[-1][1] = True    
    
for file in os.listdir('./switch'):
    path = "./switch/"+file
    switch_video.append(pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT)))
    
window = pygame.display.set_mode((WIDTH, HEIGHT))    
pygame.display.set_caption("THYTHM")

black = pygame.image.load("./image/black.png").convert_alpha()
black.set_alpha(128)
black = pygame.transform.scale(black, (WIDTH, HEIGHT))
small_setting_length = 72/1536*WIDTH

circle_img = pygame.image.load('./image/ball.png')
rains_img = pygame.image.load('./image/raintap.png')
long_ball_img = pygame.image.load('./image/long.png')
long_ball_up = pygame.image.load('./image/longup.png')
long_ball_down = pygame.image.load('./image/longdown.png')
icon = pygame.transform.scale(pygame.image.load("./image/icon.png"), (100/1536*WIDTH, 100/1536*WIDTH)) # 游戏头像
userboard = pygame.transform.scale(pygame.image.load("./image/userboard.png"), (HEIGHT*0.6, HEIGHT)) # 用户板
board = pygame.transform.scale(pygame.image.load("./image/board.png"), (120/1536*WIDTH,120/1536*WIDTH)) # 作为用户信息的板
return_img = pygame.transform.scale(pygame.image.load('./image/Userreturn.png'),(small_setting_length,small_setting_length)) # 返回按钮
set_img = pygame.transform.scale(pygame.image.load('./image/Userset.png'),(small_setting_length,small_setting_length)) # 设置按钮
big_return_img = pygame.transform.scale(pygame.image.load('./image/Userreturn.png'),(100/1536*WIDTH,100/1536*WIDTH)) # 返回按钮
continue_img = pygame.transform.scale(pygame.image.load('./image/continue.png'),(100/1536*WIDTH,100/1536*WIDTH))
songlist_img = pygame.transform.scale(pygame.image.load("./image/songlist.png"), (560/1536*WIDTH,160/1536*WIDTH))
top_image = pygame.transform.scale(pygame.image.load('./image/themeTop.png'),(400/1536*WIDTH,100/1536*WIDTH))
left = pygame.transform.scale(pygame.image.load('./image/left.png'),(100/1536*WIDTH,100/1536*WIDTH))
right = pygame.transform.scale(pygame.image.load('./image/right.png'),(100/1536*WIDTH,100/1536*WIDTH))
perfect_img = pygame.transform.scale(pygame.image.load('./image/perfect.png'),(400/1536*WIDTH,100/1536*WIDTH))
good_img = pygame.transform.scale(pygame.image.load('./image/good.png'),(400/1536*WIDTH,100/1536*WIDTH))
miss_img = pygame.transform.scale(pygame.image.load('./image/miss.png'),(400/1536*WIDTH,100/1536*WIDTH))
stop_img = pygame.transform.scale(pygame.image.load('./image/stop.png'),(small_setting_length,small_setting_length))

sound_effect = pygame.mixer.Sound('./music/sound_effect.MP3')
enter_music = pygame.mixer.Sound("./music/enter.mp3")
enter_music_effect = pygame.mixer.Sound("./music/enter_effect.MP3")
gameover_music = pygame.mixer.Sound("./music/gameover.MP3")

normal_font = pygame.font.Font("./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(50/1536*WIDTH))
font = pygame.font.Font("./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(30/1536*WIDTH)) # 用户信息的字体， size 30
font1 = pygame.font.Font("./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(20/1536*WIDTH)) # 用户信息的字体， size 20

music_inform = {}

for name in music_names:
    music_inform[name] = "未开始"
music_inform = get_music_inform(music_inform)

class Raindrop:
    # 初始化雨滴的属性
    def __init__(self):
        # 随机生成雨滴的初始位置
        self.x = random.randint(0, WIDTH)
        self.y = 0
        # 随机生成雨滴的速度
        self.speed = random.randint(5, 15)
        # 随机生成雨滴的长度
        self.length = random.randint(10, 20)

    # 雨滴下落的方法
    def fall(self):
        # 雨滴的y坐标增加速度
        self.y += self.speed

    # 绘制雨滴的方法
    def draw(self,window):
        # 在窗口上绘制雨滴
        pygame.draw.line(window, (211, 211, 211), (self.x, self.y), (self.x, self.y + self.length), 2)

    # 判断雨滴是否超出屏幕的方法
    def off_screen(self):
        # 如果雨滴的y坐标大于屏幕的高度，则返回True
        return self.y > HEIGHT       

# 创建一个键盘控制器, 直接切换成英文
keyboard = Controller()
# 按下shift键
keyboard.press(Key.shift)
# 释放shift键
keyboard.release(Key.shift)