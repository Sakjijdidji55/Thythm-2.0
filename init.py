import json
import random
import threading
import time
from logging import getLogger
from pathlib import Path

import pygame

from load import (
    Raindrop,
    enter_music,
    enter_video,
    music_inform,
    normal_font,
    start_video,
    switch_video,
)
from Music import deal_name
from MusicEnd import MUSIC
from MusicManager import ThemeManager, black, enter_music_effect
from setting import MUSICSETTING
from user import HEIGHT, WIDTH, User, clock, window
from userData import user_inform

log = getLogger(__name__)
user = User(user_inform["name"], user_inform["icon_path"], user_inform["description"])


def switch_face(img: pygame.Surface):
    for p in switch_video:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        window.blit(img, (0, 0))
        window.blit(p, (0, 0))
        pygame.display.update()
        clock.tick(50)


raindrops = []


def begin():
    for p in start_video:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        window.blit(p[0], (0, 0))
        pygame.display.update()
        if p[1]:
            time.sleep(3)
        clock.tick(20)

    enter_music.play()
    enter_music_start = threading.Thread(target=lambda: enter_music_effect.play())
    text = normal_font.render(
        "轻触开始, (注：素材大部分来自与网络，侵删)", True, (255, 255, 255)
    )

    i = 0
    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            state = user.check(event)
            log.debug(state)
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and pos[1] > HEIGHT // 2
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
            ) and not user.show:  # 按下enter键
                enter_music.stop()
                enter_music_start.start()
                return
            if state == "User":
                user.show = not user.show

        window.blit(enter_video[i], (0, 0))
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))
        user.draw(window)
        i = (i + 1) % len(enter_video)

        if random.random() < 0.1:
            raindrops.append(Raindrop())

        for raindrop in raindrops:
            raindrop.fall()
            # 绘制雨滴
            raindrop.draw(window)
            # 如果雨滴超出屏幕
            if raindrop.off_screen():
                # 从雨滴列表中移除
                raindrops.remove(raindrop)
        pygame.display.update()
        clock.tick(30)


def wait_to_load(music: MUSIC, window: pygame.Surface):
    window.blit(music.image, (0, 0))
    window.blit(black, (0, 0))

    window.blit(
        music.cover,
        (
            WIDTH // 2 - music.cover.get_size()[0] // 2,
            HEIGHT // 3 - music.cover.get_size()[1] // 2,
        ),
    )

    w = music.music_writer
    n = music.music_name

    w_text = normal_font.render("作者: " + w, True, (255, 255, 255))
    n_text = normal_font.render("歌曲名: " + n, True, (255, 255, 255))

    window.blit(
        w_text,
        (WIDTH // 2 - w_text.get_width() // 2, HEIGHT // 2 + w_text.get_height() * 3),
    )
    window.blit(
        n_text,
        (WIDTH // 2 - n_text.get_width() // 2, HEIGHT // 2 + n_text.get_height() * 5),
    )

    pygame.display.update()


def help_switch(obj):
    surface = pygame.Surface((WIDTH, HEIGHT))
    obj.draw(surface)
    switch_face(surface)


# 构建音乐列表
themes_sources = []

for theme in Path("./musplays").iterdir():
    music_list = []

    for music in theme.iterdir():
        music_name = music.name.split("-")[-1]
        dealed_name = deal_name(music_name)
        with (music / "metadata.json").open() as file:
            author = json.load(file)["author"]

        music_list.append(
            MUSIC(
                music_name,
                str(music / "music.mp3"),
                1,
                author,
                music_inform[dealed_name],
            )
        )
    themes_sources.append((theme, theme / "cover.png", theme / "image.png", music_list))

cur_machine = ThemeManager(themes_sources)

setting = MUSICSETTING()
