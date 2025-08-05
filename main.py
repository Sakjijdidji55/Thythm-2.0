import os
import random
import sys
import time
from logging import getLogger

import psutil
import pygame

import user
from init import (
    HEIGHT,
    WIDTH,
    Raindrop,
    begin,
    clock,
    cur_machine,
    deal_name,
    help_switch,
    music_inform,
    raindrops,
    setting,
    wait_to_load,
    window,
)
from load import font, fps
from MusicEnd import MusicEnd
from userData import music_inform_path, save_music_inform

log = getLogger(__name__)

t = time.time()
cur_machine.init_themes()
Manager = cur_machine
log.debug("init time: %ss", time.time() - t)
begin()
help_switch(cur_machine)  # 初始化游戏

# 定义状态
ThemeManager_state = 1
Music_choicer_state = 2
Music_running_state = 3
Music_end_state = 4

# 初始化主题管理器
cur_state = ThemeManager_state
cur_machine.start()

# 计算FPS
last_time = time.time()
cnt = 0
text = font.render("FPS: " + str(fps), True, (255, 255, 255))
pid = os.getpid()
p = psutil.Process(pid)

while True:
    memory_rss = p.memory_info().rss / 1024 / 1024
    print(
        "memory_rss:", memory_rss, "MB"
    )  # 打印内存占用, memory_rss: 4337.1015625 MB,缓存4G左右

    # 计算FPS
    if time.time() - last_time > 1:
        last_time = time.time()
        text = font.render("FPS: " + str(cnt), True, (255, 255, 255))
        cnt = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 头像位置
        if cur_state != Music_running_state:
            qry = user.check(event)
            if qry == "User":
                user.show = not user.show
            if qry == "Set":
                setting.WaitToChoice = True
        # 设置
        if setting.is_WaitToChoice():
            setting.is_check_set(event)
            Manager.set_volume(setting.get_volume())
            fps = setting.get_fps()
            log.debug(cur_state)
        elif not user.show:
            if cur_state == ThemeManager_state:  # 这样当检查setting时不会检测主题
                next_state = cur_machine.change_theme(event)
                if next_state == "set":
                    setting.WaitToChoice = True  # 设置设为打开状态
                elif next_state is not None:
                    cur_state = Music_choicer_state
                    cur_machine = next_state
                    help_switch(cur_machine)  # 进入对应主题的歌曲选择器
                    cur_machine.start()
            elif cur_state == Music_choicer_state:
                log.debug(cur_state)
                next = cur_machine.scroll(event)
                if next == "set":
                    setting.WaitToChoice = True
                elif next is not None:
                    cur_machine = next
                    if str(cur_machine) == "MusicManager":  # 回退到主题选择器
                        cur_state = ThemeManager_state
                        help_switch(cur_machine)
                        cur_machine.start()
                    else:  # 进入歌曲，开始主游戏
                        window.fill((0, 0, 0))
                        wait_to_load(cur_machine, window)
                        time.sleep(3)
                        cur_machine.effect = setting.effect_state
                        cur_machine.start()  # 开始主游戏
                        cur_state = Music_running_state
            elif cur_state == Music_running_state:
                cur_machine.check_short_and_long(event)  # 检查游戏逻辑
                state = cur_machine.is_check_setting(event, window)  # 是否点击暂停
                if state and state != "notReturn":
                    if str(state) == "Music_Choicer":  # 暂停后返回歌曲选择器
                        cur_state = Music_choicer_state
                        cur_machine = state
                        help_switch(cur_machine)
                        cur_machine.start()
            elif cur_state == Music_end_state:
                log.debug(cur_machine)
                next = cur_machine.check(event)  # 检查游戏结束后的逻辑
                if next == "set":
                    setting.WaitToChoice = True
                elif next is not None:
                    cur_machine = next
                    log.debug("%r %s", cur_machine, cur_machine)
                    if str(cur_machine) == "Music_Choicer":  # 返回歌曲选择器
                        cur_state = Music_choicer_state
                        help_switch(cur_machine)
                        cur_machine.start()
                    elif str(cur_machine) == "Music":  # 重新开始游戏
                        time.sleep(0.1)
                        cur_machine.effect = setting.effect_state
                        cur_machine.start()
                        cur_state = Music_running_state
                    log.debug(cur_state)

    cur_machine.draw(window)  # 绘制游戏界面

    if cur_state == Music_running_state:
        cur_machine.check_long_and_rain()  # 检查长按和下雨
        cur_machine.update()  # 更新游戏状态
        cur_machine.check()  # 检查每个物件的状态

        if cur_machine.is_music_over():
            cur_state = Music_end_state  # 游戏结束
            cur_name = deal_name(cur_machine.music_name[:])
            print(cur_machine.score, cur_machine.total_score)
            music_end = MusicEnd(
                cur_machine,
                cur_machine.score,
                cur_machine.total_score,
                cur_machine.prefect,
                cur_machine.good,
                cur_machine.miss,
            )
            music_inform[cur_name] = music_end.rank  # 更新歌曲信息
            cur_machine.best_rank = music_end.rank  # 更新最佳成绩
            save_music_inform(
                music_inform=music_inform, music_inform_path=music_inform_path
            )  # 保存歌曲信息
            cur_machine = music_end
            help_switch(cur_machine)  # 切换到游戏结束界面
    else:
        user.draw(window)  # 绘制用户信息

    if random.random() < 0.1:  # 随机生成雨滴
        raindrops.append(Raindrop())

    for raindrop in raindrops[:]:
        raindrop.fall()
        raindrop.draw(window)
        if raindrop.off_screen():
            raindrops.remove(raindrop)

    if setting.is_WaitToChoice():
        setting.draw(window)

    window.blit(
        text, (WIDTH - text.get_width() - 10, HEIGHT - text.get_height() - 10)
    )  # 绘制帧率
    cnt += 1

    pygame.display.update()
    clock.tick(fps)  # 控制游戏循环频率
