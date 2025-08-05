import threading
import Music
from load import *

name_img = pygame.transform.scale(
    pygame.image.load("./image/EndTop.png"), (600 / 1536 * WIDTH, 100 / 1536 * WIDTH)
)


class MusicEnd:
    def __init__(
        self,
        song: Music,
        score: float,
        total: float,
        perfect: int,
        good: int,
        miss: int,
    ):
        """
        :param score: 得分
        :param total: 总分
        :param perfect: 完美数
        :param miss: 漏掉数
        :param good: 好数
        """
        self.song = song
        self.rank_size = pygame.font.Font(
            "./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(120 / 1536 * WIDTH)
        )
        self.score_size = pygame.font.Font(
            "./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(80 / 1536 * WIDTH)
        )
        self.text_size = pygame.font.Font(
            "./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(50 / 1536 * WIDTH)
        )
        self.score = score
        self.total = total
        self.perfect = perfect
        self.miss = miss
        self.good = good
        self.rank = self.get_rank(score, total)
        gameover_music.play()

    def set_volume(self, v):
        self.song.set_volume(v)

    def get_rank(self, score: float, total: float):  # 获取排名
        if score == total:
            return "SSS"
        if score / total >= 0.97:
            return "SS"
        if score / total >= 0.95:
            return "S"
        if score >= total * 0.92:
            return "A"
        if score >= total * 0.8:
            return "B"
        else:
            return "C"

    def draw(self, window: pygame.Surface):
        window.blit(self.song.image, (0, 0))  # 绘制背景
        window.blit(black, (0, 0))  # 绘制黑色背景

        window.blit(return_img, (25, 40))  # 绘制返回按钮
        window.blit(set_img, (150, 40))  # 绘制设置按钮
        window.blit(
            continue_img,
            (WIDTH - 125 / 1536 * WIDTH - WIDTH // 24, HEIGHT - 125 / 1536 * WIDTH),
        )  # 绘制继续按钮

        window.blit(
            name_img,
            (WIDTH // 4 + WIDTH // 16 - name_img.get_width() // 2, HEIGHT // 8),
        )  # 绘制top图片
        name = self.text_size.render(self.song.music_name[:12], True, (0, 0, 0))
        window.blit(
            name, (WIDTH // 4 + WIDTH // 16 - name.get_width() // 2, HEIGHT // 8 + 25)
        )

        score = self.score_size.render(
            str(int(self.score / self.total * 10000)), True, (255, 255, 255)
        )
        rank = self.rank_size.render(self.rank, True, (128, 0, 255))  # 绘制排名
        perfect = self.text_size.render(
            "Perfect: " + str(self.perfect), True, (0, 0, 0)
        )
        miss = self.text_size.render(
            "Miss: " + str(self.miss), True, (0, 0, 0)
        )  # 绘制分数
        good = self.text_size.render("Good: " + str(self.good), True, (0, 0, 0))

        # 绘制分数,数据均通过计算，可以自己试试修改
        window.blit(
            score,
            (
                WIDTH // 2 + WIDTH // 7 - score.get_width() // 2,
                HEIGHT // 8 + 10 / 1536 * WIDTH,
            ),
        )
        window.blit(
            rank,
            (
                WIDTH - WIDTH // 10 - rank.get_width() // 2,
                HEIGHT // 8 - 10 / 1536 * WIDTH,
            ),
        )

        window.blit(
            perfect_img,
            (
                WIDTH // 2 + WIDTH // 4 - perfect_img.get_width() // 2,
                HEIGHT // 2 - HEIGHT // 8,
            ),
        )
        window.blit(
            perfect,
            (
                WIDTH // 2 + WIDTH // 4 - perfect.get_width() // 2,
                HEIGHT // 2 - HEIGHT // 8 + 25,
            ),
        )
        window.blit(
            good_img,
            (
                WIDTH // 2 + WIDTH // 4 - good_img.get_width() // 2,
                HEIGHT // 2 + 140 / 1536 * WIDTH - HEIGHT // 8,
            ),
        )
        window.blit(
            good,
            (
                WIDTH // 2 + WIDTH // 4 - good.get_width() // 2,
                HEIGHT // 2 + 165 / 1536 * WIDTH - HEIGHT // 8,
            ),
        )
        window.blit(
            miss_img,
            (
                WIDTH // 2 + WIDTH // 4 - miss_img.get_width() // 2,
                HEIGHT // 2 + 280 / 1536 * WIDTH - HEIGHT // 8,
            ),
        )
        window.blit(
            miss,
            (
                WIDTH // 2 + WIDTH // 4 - miss.get_width() // 2,
                HEIGHT // 2 + 305 / 1536 * WIDTH - HEIGHT // 8,
            ),
        )

        window.blit(
            self.song.cover, (WIDTH // 16, HEIGHT // 4 + HEIGHT // 8)
        )  # 绘制歌曲封面

    def check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if (
                pos[0] >= 25 / 1536 * WIDTH
                and pos[0] <= 112 / 1536 * WIDTH
                and pos[1] >= 40 / 1536 * WIDTH
                and pos[1] <= 112 / 1536 * WIDTH
            ):
                gameover_music.stop()
                return self.song  # 重新开始

            if (
                pos[0] >= 150 / 1536 * WIDTH
                and pos[0] <= (150 + 72) / 1536 * WIDTH
                and pos[1] >= 40 / 1536 * WIDTH
                and pos[1] <= 112 / 1536 * WIDTH
            ):
                return "set"

            if (
                pos[0] >= WIDTH - 125 / 1536 * WIDTH - WIDTH // 24
                and pos[0]
                <= WIDTH - 125 / 1536 * WIDTH - WIDTH // 24 + 100 / 1536 * WIDTH
                and pos[1] >= HEIGHT - 125 / 1536 * WIDTH
                and pos[1] <= HEIGHT - 125 / 1536 * WIDTH + 100 / 1536 * WIDTH
            ):
                gameover_music.stop()
                threading.Thread(target=lambda: enter_music_effect.play()).start()
                return self.song.father  # 回到选歌界面
        return None
