import sys
import threading
from load import *


class MusicChoicer:
    def __init__(self, songs_list, theme, father):
        """
        :param songs_list: 歌曲列表
        :param theme: 主题类
        :param father: 主题的父类
        """
        self.positions = (72 / 1536 * WIDTH, 376 / 1536 * WIDTH)
        self.line_pos = (
            (912 / 1536 * WIDTH, 96 / 1536 * WIDTH),
            (552 / 1536 * WIDTH, 456 / 1536 * WIDTH),
            (992 / 1536 * WIDTH, 896 / 1536 * WIDTH),
        )
        self.bk_pos = (
            700 / 1536 * WIDTH,
            216 / 1536 * WIDTH,
        )  # 通过计算得到的背景图片位置
        self.text_positions = [
            [
                (192 / 1536 * WIDTH, 256 / 1536 * WIDTH),
                (312 / 1536 * WIDTH, 236 / 1536 * WIDTH),
                (312 / 1536 * WIDTH, 316 / 1536 * WIDTH),
            ],
            [
                (112 / 1536 * WIDTH, 416 / 1536 * WIDTH),
                (232 / 1536 * WIDTH, 396 / 1536 * WIDTH),
                (232 / 1536 * WIDTH, 476 / 1536 * WIDTH),
            ],
            [
                (192 / 1536 * WIDTH, 576 / 1536 * WIDTH),
                (312 / 1536 * WIDTH, 556 / 1536 * WIDTH),
                (312 / 1536 * WIDTH, 636 / 1536 * WIDTH),
            ],
            [
                (272 / 1536 * WIDTH, 736 / 1536 * WIDTH),
                (392 / 1536 * WIDTH, 716 / 1536 * WIDTH),
                (392 / 1536 * WIDTH, 796 / 1536 * WIDTH),
            ],
        ]
        self.index_font = pygame.font.Font(
            "./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(80 / 1536 * WIDTH)
        )
        self.rank_font = pygame.font.Font(
            "./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(60 / 1536 * WIDTH)
        )
        self.text_size = pygame.font.Font(
            "./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(40 / 1536 * WIDTH)
        )
        self.text_color = (255, 255, 255)
        self.line_color = (255, 255, 255, 64)
        self.songs_list = songs_list  # 歌曲列表
        self.song_spacing = 160 / 1536 * WIDTH
        self.index = [len(self.songs_list) - 1, 0, 1, 2]
        self.father = theme
        self.father_father = father

    def set_music(self):
        for song in self.songs_list:
            song.set_father(self)
            song.load()

    def start(self):
        self.songs_list[self.index[1]].play_sound()

    def get_cur_music(self):
        return self.songs_list[self.index[1]]

    def draw(self, window):
        window.blit(
            self.songs_list[self.index[1]].image, (0, 0)
        )  # 添加背景图片，为当前音乐的背景
        window.blit(black, (0, 0))  # 添加黑色背景

        window.blit(return_img, (25 / 1536 * WIDTH, 40 / 1536 * WIDTH))  # 添加返回按钮
        window.blit(set_img, (150 / 1536 * WIDTH, 40 / 1536 * WIDTH))  # 添加设置按钮

        window.blit(songlist_img, self.positions)  # 添加歌单图片
        pygame.draw.line(
            window, self.line_color, self.line_pos[0], self.line_pos[1], 4
        )  # 添加分割线
        pygame.draw.line(
            window, self.line_color, self.line_pos[1], self.line_pos[2], 4
        )  # 添加分割线

        theme_name = self.text_size.render(
            self.father.name, True, (128, 128, 128)
        )  # 添加主题名字
        window.blit(
            top_image,
            (WIDTH // 2 - 200 / 1536 * WIDTH, HEIGHT // 8 - 65 / 1536 * WIDTH),
        )  # 添加主题名字后的背景
        window.blit(
            theme_name,
            (WIDTH // 2 - theme_name.get_width() // 2, HEIGHT // 8 - 30 / 1536 * WIDTH),
        )

        # 选择难度
        window.blit(self.songs_list[self.index[1]].cover, self.bk_pos)  # 添加音乐封面
        easy_text = self.text_size.render("简单", True, self.text_color)
        window.blit(
            choiced_select_img,
            (
                self.bk_pos[0] + 150 * WIDTH // 1536,
                self.bk_pos[1] + HEIGHT // 2 + 20 * WIDTH // 1536,
            ),
        )
        window.blit(
            easy_text,
            (
                self.bk_pos[0]
                + 150 * WIDTH // 1536
                + choiced_select_img.get_width() // 2
                - easy_text.get_width() // 2,
                self.bk_pos[1]
                + HEIGHT // 2
                + 20 * WIDTH // 1536
                + choiced_select_img.get_height() // 2
                - easy_text.get_height() // 2,
            ),
        )
        mid_text = self.text_size.render("中等", True, self.text_color)
        window.blit(
            choiced_select_img,
            (
                self.bk_pos[0] + 170 * WIDTH // 1536 + choiced_select_img.get_width(),
                self.bk_pos[1] + HEIGHT // 2 + 20 * WIDTH // 1536,
            ),
        )
        window.blit(
            mid_text,
            (
                self.bk_pos[0]
                + 170 * WIDTH // 1536
                + choiced_select_img.get_width()
                + choiced_select_img.get_width() // 2
                - mid_text.get_width() // 2,
                self.bk_pos[1]
                + HEIGHT // 2
                + 20 * WIDTH // 1536
                + choiced_select_img.get_height() // 2
                - mid_text.get_height() // 2,
            ),
        )
        hard_text = self.text_size.render("困难", True, self.text_color)
        window.blit(
            choiced_select_img,
            (
                self.bk_pos[0]
                + 190 * WIDTH // 1536
                + 2 * choiced_select_img.get_width(),
                self.bk_pos[1] + HEIGHT // 2 + 20 * WIDTH // 1536,
            ),
        )
        window.blit(
            hard_text,
            (
                self.bk_pos[0]
                + 190 * WIDTH // 1536
                + 2 * choiced_select_img.get_width()
                + choiced_select_img.get_width() // 2
                - hard_text.get_width() // 2,
                self.bk_pos[1]
                + HEIGHT // 2
                + 20 * WIDTH // 1536
                + choiced_select_img.get_height() // 2
                - hard_text.get_height() // 2,
            ),
        )
        for i in range(3):
            if i == self.get_cur_music().state - 1:
                continue
            window.blit(
                choiced_img,
                (
                    self.bk_pos[0]
                    + 150 * WIDTH // 1536
                    + i * (20 + choiced_select_img.get_width()),
                    self.bk_pos[1] + HEIGHT // 2 + 20 * WIDTH // 1536,
                ),
            )

        best_rank = self.rank_font.render(
            "Best Rank:" + self.songs_list[self.index[1]].best_rank,
            True,
            (255, 255, 255),
        )
        window.blit(
            best_rank,
            (
                self.bk_pos[0] + WIDTH // 2 - best_rank.get_width(),
                self.bk_pos[1] - 80 / 1536 * WIDTH,
            ),
        )

        for i in range(4):
            name = self.songs_list[self.index[i]].music_name
            writer = self.songs_list[self.index[i]].music_writer
            index_surface = self.index_font.render(
                str(self.index[i] + 1), True, self.text_color
            )
            name_surface = self.text_size.render(name, True, self.text_color)
            writer_surface = self.text_size.render(
                writer, True, self.text_color
            )  # 渲染文字
            window.blit(index_surface, self.text_positions[i][0])
            window.blit(name_surface, self.text_positions[i][1])
            window.blit(
                writer_surface, self.text_positions[i][2]
            )  # 一个界面中显示4首歌曲，每首歌曲显示序号、歌名、作者，按照事先算的坐标

    def switch(self, key, window: pygame.Surface):  # key 1:淡入 2:淡出
        if key == 1:
            surface = pygame.Surface((WIDTH, HEIGHT))
            self.draw(surface)
            for i in range(255, -1, -32):
                window.fill((0, 0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                clock.tick(60)
                surface.set_alpha(i)
                window.blit(surface, (0, 0))
                pygame.display.update()
        elif key == 2:
            surface = pygame.Surface((WIDTH, HEIGHT))
            self.draw(surface)
            for i in range(0, 256, 16):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                clock.tick(60)
                surface.set_alpha(i)
                window.blit(surface, (0, 0))
                pygame.display.update()

    def scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                self.switch(1, window)  # 淡入
                self.songs_list[self.index[1]].stop_sound()  # 停止当前音乐
                self.index.append((self.index[-1] + 1) % len(self.songs_list))
                self.index.pop(0)  # 更新索引
                self.switch(2, window)
                self.songs_list[self.index[1]].play_sound()  # 播放新音乐
            elif event.button == 4:
                self.switch(1, window)
                self.songs_list[self.index[1]].stop_sound()
                self.index.insert(
                    0, (self.index[0] - 1 + len(self.songs_list)) % len(self.songs_list)
                )
                self.index.pop()  # 更新索引
                self.switch(2, window)
                self.songs_list[self.index[1]].play_sound()
            elif event.button == 1:
                pos = pygame.mouse.get_pos()
                if (
                    WIDTH // 2 - 200 / 1536 * WIDTH
                    < pos[0]
                    < WIDTH // 2 + 200 / 1536 * WIDTH
                    and HEIGHT // 8 - 65 / 1536 * WIDTH
                    < pos[1]
                    < HEIGHT // 8 + 35 / 1536 * WIDTH
                ) or (
                    25 / 1536 * WIDTH < pos[0] < 97 / 1536 * WIDTH
                    and 40 / 1536 * WIDTH < pos[1] < 112 / 1536 * WIDTH
                ):
                    self.songs_list[self.index[1]].stop_sound()
                    threading.Thread(target=lambda: enter_music_effect.play()).start()
                    return self.father_father  # 返回主题界面，并停止当前音乐，这里是点击主题文字时或者点击返回按钮时触发
                if (
                    pos[0] > self.bk_pos[0]
                    and self.bk_pos[1] < pos[1] < self.bk_pos[1] + HEIGHT // 2
                ):
                    self.songs_list[self.index[1]].stop_sound()
                    threading.Thread(target=lambda: enter_music_effect.play()).start()
                    return self.get_cur_music()  # 开始音乐
                if (
                    150 / 1536 * WIDTH < pos[0] < 222 / 1536 * WIDTH
                    and 40 / 1536 * WIDTH < pos[1] < 112 / 1536 * WIDTH
                ):
                    return "set"
                if (
                    self.bk_pos[0] + 150 * WIDTH // 1536
                    < pos[0]
                    < self.bk_pos[0]
                    + 150 * WIDTH // 1536
                    + choiced_select_img.get_width()
                    and self.bk_pos[1] + HEIGHT // 2 + 20 * WIDTH // 1536
                    < pos[1]
                    < self.bk_pos[1]
                    + HEIGHT // 2
                    + 20 * WIDTH // 1536
                    + choiced_select_img.get_height()
                ):
                    self.get_cur_music().state = 1
                if (
                    self.bk_pos[0]
                    + 170 * WIDTH // 1536
                    + choiced_select_img.get_width()
                    < pos[0]
                    < self.bk_pos[0]
                    + 170 * WIDTH // 1536
                    + 2 * choiced_select_img.get_width()
                    and self.bk_pos[1] + HEIGHT // 2 + 20 * WIDTH // 1536
                    < pos[1]
                    < self.bk_pos[1]
                    + HEIGHT // 2
                    + 20 * WIDTH // 1536
                    + choiced_select_img.get_height()
                ):
                    self.get_cur_music().state = 2
                if (
                    self.bk_pos[0]
                    + 190 * WIDTH // 1536
                    + 2 * choiced_select_img.get_width()
                    < pos[0]
                    < self.bk_pos[0]
                    + 190 * WIDTH // 1536
                    + 3 * choiced_select_img.get_width()
                    and self.bk_pos[1] + HEIGHT // 2 + 20 * WIDTH // 1536
                    < pos[1]
                    < self.bk_pos[1]
                    + HEIGHT // 2
                    + 20 * WIDTH // 1536
                    + choiced_select_img.get_height()
                ):
                    self.get_cur_music().state = 3

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.songs_list[self.index[1]].stop_sound()
                threading.Thread(target=lambda: enter_music_effect.play()).start()
                return self.get_cur_music()  # 开始音乐

            if event.key == pygame.K_ESCAPE:
                self.songs_list[self.index[1]].stop_sound()
                threading.Thread(target=lambda: enter_music_effect.play()).start()
                return self.father_father  # 返回主题界面，并停止当前音乐

            if event.key == pygame.K_DOWN:
                self.switch(1, window)
                self.songs_list[self.index[1]].stop_sound()
                self.index.insert(
                    0, (self.index[0] - 1 + len(self.songs_list)) % len(self.songs_list)
                )
                self.index.pop()  # 更新索引
                self.switch(2, window)
                self.songs_list[self.index[1]].play_sound()

            if event.key == pygame.K_UP:
                self.switch(1, window)
                self.songs_list[self.index[1]].stop_sound()
                self.index.append(
                    (self.index[-1] - 1 + len(self.songs_list)) % len(self.songs_list)
                )
                self.index.pop(0)  # 更新索引
                self.switch(2, window)
                self.songs_list[self.index[1]].play_sound()
        return None

    def set_volume(self, volume: float):
        for song in self.songs_list:
            song.set_volume(volume)

    def __str__(self):
        return "Music_Choicer"
