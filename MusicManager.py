from load import *
from MusicChoicer import *
import threading


class theme:
    def __init__(
        self, name: str, cover: str, image: str, music_list: list, father: object
    ):
        """
        name: 主题名称
        cover: 主题图片
        image: 主题背景图片
        music_list: 主题音乐列表
        father: 父类
        """
        self.name = name
        self.cover = pygame.transform.scale(
            pygame.image.load(cover), (WIDTH // 2, HEIGHT // 2)
        )
        self.image = pygame.transform.scale(pygame.image.load(image), (WIDTH, HEIGHT))
        self.MusicChoice = MusicChoicer(music_list, self, father)
        threading.Thread(target=self.MusicChoice.set_music()).start()
        self.text_size = pygame.font.Font(
            "./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(50 / 1536 * WIDTH)
        )

    def draw(self, window: pygame.Surface):
        window.blit(self.image, (0, 0))
        window.blit(black, (0, 0))
        window.blit(return_img, (25 / 1536 * WIDTH, 40 / 1536 * WIDTH))  # 返回按钮
        window.blit(set_img, (150 / 1536 * WIDTH, 40 / 1536 * WIDTH))  # 设置按钮
        window.blit(top_image, (WIDTH // 2 - 200 / 1536 * WIDTH, HEIGHT // 8))
        name = self.text_size.render(self.name, True, (0, 0, 0))
        window.blit(
            name, (WIDTH // 2 - name.get_width() // 2, HEIGHT // 8 + 25 / 1536 * WIDTH)
        )
        window.blit(self.cover, (WIDTH // 4, HEIGHT // 4 + HEIGHT // 8))  # 覆盖图片


class ThemeManager:
    def __init__(self, theme_sources: list):
        """
        theme_list: 主题列表
        """
        self.theme_sources = theme_sources  # 主题源文件列表
        self.current_theme_index = 0
        self.sound = pygame.mixer.Sound("./gamemusic/pianocd - 星河.mp3")

    def init_themes(self):
        self.theme_list = []
        for source in self.theme_sources:
            self.theme_list.append(
                theme(source[0], source[1], source[2], source[3], self)
            )  # 创建主题对象

    def start(self):
        self.sound.play(-1)

    def get_current_theme_MusicChoicer(self):
        return self.theme_list[self.current_theme_index].MusicChoice  # 返回音乐选择器

    def get_current_theme(self):
        return self.theme_list[self.current_theme_index]  # 返回当前主题

    def draw(self, window: pygame.Surface):
        current_theme = self.get_current_theme()
        current_theme.draw(window)  # 绘制当前主题
        window.blit(
            left, (100 / 1536 * WIDTH, HEIGHT // 2 + HEIGHT // 8 - 50 / 1536 * WIDTH)
        )
        window.blit(
            right,
            (WIDTH - 200 / 1536 * WIDTH, HEIGHT // 2 + HEIGHT // 8 - 50 / 1536 * WIDTH),
        )  # 左右按钮

    def switch(self, key, window):  # key 1:淡入 2:淡出
        if key == 1:
            surface = pygame.Surface((WIDTH, HEIGHT))
            self.draw(surface)
            for i in range(255, -1, -32):  # 从完全透明到完全不透明
                window.fill((0, 0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                clock.tick(30)
                surface.set_alpha(i)
                window.blit(surface, (0, 0))
                pygame.display.update()
        elif key == 2:
            surface = pygame.Surface((WIDTH, HEIGHT))
            self.draw(surface)
            for i in range(0, 256, 16):  # 从完全不透明到完全透明
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                clock.tick(60)
                surface.set_alpha(i)
                window.blit(surface, (0, 0))
                pygame.display.update()

    def change_theme(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # 向左切换主题
                self.switch(1, window)
                self.current_theme_index = (self.current_theme_index - 1) % len(
                    self.theme_list
                )
                self.switch(2, window)
            elif event.key == pygame.K_RIGHT:  # 向右切换主题
                self.switch(1, window)
                self.current_theme_index = (self.current_theme_index + 1) % len(
                    self.theme_list
                )
                self.switch(2, window)
            elif event.key == pygame.K_RETURN:  # 按下回车键
                threading.Thread(target=lambda: enter_music_effect.play()).start()
                self.sound.stop()
                return self.get_current_theme_MusicChoicer()
            elif event.key == pygame.K_ESCAPE:  # 按下esc键
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if (
                    pos[0] > 100 / 1536 * WIDTH
                    and pos[0] < 200 / 1536 * WIDTH
                    and pos[1] > HEIGHT // 2 + HEIGHT // 8 - 50 / 1536 * WIDTH
                    and pos[1] < HEIGHT // 2 + HEIGHT // 8 + 50 / 1536 * WIDTH
                ):
                    self.switch(1, window)
                    self.current_theme_index = (self.current_theme_index - 1) % len(
                        self.theme_list
                    )  # 点到了左边,向左切换
                    self.switch(2, window)
                elif (
                    pos[0] > WIDTH - 200 / 1536 * WIDTH
                    and pos[0] < WIDTH - 100 / 1536 * WIDTH
                    and pos[1] > HEIGHT // 2 + HEIGHT // 8 - 50 / 1536 * WIDTH
                    and pos[1] < HEIGHT // 2 + HEIGHT // 8 + 50 / 1536 * WIDTH
                ):
                    self.switch(1, window)
                    self.current_theme_index = (self.current_theme_index + 1) % len(
                        self.theme_list
                    )  # 点到了右边，向右切换
                    self.switch(2, window)
                if (
                    pos[0] > WIDTH // 4
                    and pos[0] < WIDTH // 4 + WIDTH // 2
                    and pos[1] > HEIGHT // 4 + HEIGHT // 8
                    and pos[1] < HEIGHT // 4 + HEIGHT // 8 + HEIGHT // 2
                ):  # 点击了主题图片或者按下回车键
                    threading.Thread(target=lambda: enter_music_effect.play()).start()
                    self.sound.stop()
                    return self.get_current_theme_MusicChoicer()
                if (
                    pos[0] > 25 / 1536 * WIDTH
                    and pos[0] < 97 / 1536 * WIDTH
                    and pos[1] > 40 / 1536 * WIDTH
                    and pos[1] < 112 / 1536 * WIDTH
                ):
                    pygame.quit()
                    sys.exit()  # 点击return按钮退出游戏
                if (
                    pos[0] > 150 / 1536 * WIDTH
                    and pos[0] < 222 / 1536 * WIDTH
                    and pos[1] > 40 / 1536 * WIDTH
                    and pos[1] < 112 / 1536 * WIDTH
                ):
                    return "set"  # 点击set按钮进入设置界面
        return None

    def set_volume(self, v):
        self.sound.set_volume(v)
        for theme in self.theme_list:
            theme.MusicChoice.set_volume(v)

    def __str__(self):
        return "MusicManager"
