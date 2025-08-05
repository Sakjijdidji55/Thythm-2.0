import random
import sys
from logging import getLogger

import pygame
from method import load_from_json, deal_name
from load import *
from node import *
from setting import *


log = getLogger(__name__)
music_notes = load_from_json("music_data/music_notes.json")

TEST_Y = 650 / 1536 * WIDTH
default_init_pos = [
    (WIDTH // 6 - 15 / 1536 * WIDTH, 0),
    (WIDTH // 2 - 15 / 1536 * WIDTH, 0),
    (WIDTH // 6 * 5 - 15 / 1536 * WIDTH, 0),
    (WIDTH // 3 - 15 / 1536 * WIDTH, 0),
    (WIDTH // 3 * 2 - 15 / 1536 * WIDTH, 0),
]
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)


class MUSICPAUSER:
    def __init__(self):
        self.choice = False

    def draw(self, window):
        rect_surface = pygame.Surface((WIDTH // 3, HEIGHT // 3))  # 创建一个矩形表面
        rect_surface.set_alpha(200)  # 设置透明度
        rect_surface.fill((0, 0, 0))  # 填充颜色
        window.blit(rect_surface, (WIDTH // 3, HEIGHT // 3))  # 在窗口上绘制矩形表面
        window.blit(
            big_return_img,
            (WIDTH // 3 + WIDTH // 12 - 36, HEIGHT // 3 + HEIGHT // 6 - 36),
        )
        window.blit(
            continue_img,
            (WIDTH // 2 + WIDTH // 12 - 36, HEIGHT // 3 + HEIGHT // 6 - 36),
        )

    def check(self, event):
        # 检查事件类型是否为鼠标点击事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查鼠标点击的按钮是否为左键
            if event.button == 1:
                # 获取鼠标点击的位置
                pos = pygame.mouse.get_pos()
                # 检查鼠标点击的位置是否在第一个选项的范围内
                if (
                    WIDTH // 3 + WIDTH // 12 - 36 <= pos[0]
                    and pos[0] <= WIDTH // 3 + WIDTH // 12 + 36
                    and HEIGHT // 3 + HEIGHT // 6 - 36 <= pos[1]
                    and pos[1] <= HEIGHT // 3 + HEIGHT // 6 + 36
                ):
                    # 设置选项为已选择
                    self.choice = True
                    return "return"
                # 检查鼠标点击的位置是否在第二个选项的范围内
                elif (
                    WIDTH // 2 + WIDTH // 12 - 36 <= pos[0]
                    and pos[0] <= WIDTH // 2 + WIDTH // 12 + 36
                    and HEIGHT // 3 + HEIGHT // 6 - 36 <= pos[1]
                    and pos[1] <= HEIGHT // 3 + HEIGHT // 6 + 36
                ):
                    # 设置选项为已选择
                    self.choice = True
                    # 返回'continue'
                    return "continue"


class music:
    # 初始化音乐类，传入音乐名称、路径、音量、作者
    def __init__(
        self,
        music_name: str,
        music_path: str,
        music_volume: float,
        music_writer: str,
        rank: str,
    ):
        self.music_name = music_name
        self.music_path = music_path
        self.music_volume = music_volume
        self.music_writer = music_writer
        # 加载背景音乐
        self.background_music = pygame.mixer.Sound(self.music_path)
        self.best_rank = rank
        # 加载节奏
        self.music_notes = music_notes[deal_name(music_name)]
        self.length = self.background_music.get_length() * 1000

    # 播放音乐
    def play(self):
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play()

    # 停止音乐
    def stop(self):
        pygame.mixer.music.stop()

    # 暂停音乐
    def pause(self):
        pygame.mixer.music.pause()

    # 继续播放音乐
    def continue_play(self):
        pygame.mixer.music.unpause()

    # 设置音量
    def set_volume(self, volume: float):
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)
        self.background_music.set_volume(self.music_volume)

    # 重新播放音乐
    def replay(self):
        pygame.mixer.music.rewind()

    def play_sound(self):
        self.background_music.play()

    def stop_sound(self):
        self.background_music.stop()

    # 获取音乐名称
    def get_name(self):
        return self.music_name

    # 获取音乐路径
    def get_path(self):
        return self.music_path

    # 获取音乐音量
    def get_volume(self):
        return self.music_volume

    # 获取音乐作者
    def get_writer(self):
        return self.music_writer

    def is_music_over(self):
        return pygame.mixer.music.get_busy() == 0

    def get_cur_pos(self):
        try:
            return pygame.mixer.music.get_pos() / self.length
        except:
            return 1


class MUSIC(music):
    def __init__(
        self,
        music_name: str,
        music_path: str,
        music_volume: float,
        music_writer: str,
        rank: str,
        father=None,
        state: int = 1,
    ):
        super().__init__(music_name, music_path, music_volume, music_writer, rank)
        self.effect = True
        self.father = father
        self.shortBalls = []
        self.longBalls = []
        self.rainBalls = []
        self.particles = []
        self.score = 1  # 当前得分
        self.total_score = 1  # 总分
        self.prefect = 0  # 完美
        self.good = 0  # 好的
        self.miss = 0  # 未命中
        self.continue_bit = 0  # 继续
        self.every_place_ball = {
            default_init_pos[0]: None,
            default_init_pos[1]: None,
            default_init_pos[2]: None,
            default_init_pos[3]: None,
            default_init_pos[4]: None,
        }  # 每个位置是的球
        self.is_load = False
        self.state = state

    def load(self):
        self.image = pygame.transform.scale(
            pygame.image.load(musics[deal_name(self.music_name)]["image"]),
            (WIDTH, HEIGHT),
        )
        self.cover = pygame.transform.scale(
            pygame.image.load(musics[deal_name(self.music_name)]["cover"]),
            (WIDTH // 2, HEIGHT // 2),
        )
        self.font = pygame.font.Font(
            "./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", int(50 / 1536 * WIDTH)
        )
        self.is_load = True

    def set_father(self, father):
        self.father = father

    def start(self):
        self.replay()
        self.score = 1
        self.total_score = 1
        self.prefect = 0
        self.good = 0
        self.miss = 0
        self.continue_bit = 0
        self.every_place_ball = {
            default_init_pos[0]: None,
            default_init_pos[1]: None,
            default_init_pos[2]: None,
            default_init_pos[3]: None,
            default_init_pos[4]: None,
        }  # 每个位置是的球
        self.shortBalls = []
        self.longBalls = []
        self.rainBalls = []
        self.particles = []
        self.play()
        self.start_time = time.time()
        self.idx = 0

    def draw(self, window: pygame.Surface):
        window.blit(self.image, (0, 0))
        window.blit(black, (0, 0))
        window.blit(stop_img, (25 / 1536 * WIDTH, 40 / 1536 * WIDTH))

        pygame.draw.line(
            window, (255, 255, 255), (0, 0), (WIDTH * self.get_cur_pos(), 0), 4
        )

        continue_text = self.font.render(
            "Continue: " + str(self.continue_bit), True, (255, 255, 255)
        )
        score_text = self.font.render(
            "Score: " + str(round(self.score / self.total_score * 100, 2)) + "%",
            True,
            (255, 255, 255),
        )

        window.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, 75))
        window.blit(score_text, (WIDTH - score_text.get_width() - WIDTH // 20, 75))

        for ball in self.shortBalls:
            ball.draw(window)

        for ball in self.longBalls:
            ball.draw(window)

        for ball in self.rainBalls:
            ball.draw(window)

        for particle in self.particles:
            particle.draw(window)

    def valid_ball(self, pos):
        if self.every_place_ball[pos] and self.every_place_ball[pos].y < WIDTH // 4:
            return False
        return True

    def not_have_many_ball_(self):
        return (
            sum([
                1
                for ball in self.every_place_ball.values()
                if ball and ball.y < WIDTH // 4
            ])
            < 3
        )

    def set_state(self, state: int):
        self.state = state

    def update(self):
        while (
            self.not_have_many_ball_()
            and self.idx < len(self.music_notes)
            and self.music_notes[self.idx] - (time.time() - self.start_time)
            < TEST_Y / (get_speed(self.state) * 1000 / fps) + 0.1
        ):
            if (
                self.music_notes[self.idx]
                - (time.time() - self.start_time)
                - TEST_Y / (get_speed(self.state) * 1000 / fps)
            ) < 0.1:
                pos = random.choice(default_init_pos)
                r = random.random()
                if r < 0.3:
                    if self.valid_ball(pos):
                        self.total_score += 20
                        self.score += 20
                        self.shortBalls.append(
                            Ball(
                                pos[0], pos[1] - 50 * WIDTH // 1536, TEST_Y, self.state
                            )
                        )
                        self.every_place_ball[pos] = self.shortBalls[-1]
                elif r < 0.5:
                    if self.valid_ball(pos):
                        self.total_score += 100
                        self.score += 100
                        length = random.randint(50, 400) * WIDTH // 1536
                        self.longBalls.append(
                            LONGBALL(
                                pos[0],
                                pos[1] - length - 25 * WIDTH // 1536,
                                length,
                                TEST_Y,
                                self.state,
                            )
                        )
                        self.every_place_ball[pos] = self.longBalls[-1]
                else:
                    if self.valid_ball(pos):
                        self.total_score += 10
                        self.score += 10
                        self.rainBalls.append(
                            RaindropBall(
                                pos[0],
                                pos[1] - 50 * WIDTH // 1536,
                                15 * WIDTH // 1536,
                                TEST_Y,
                                self.state,
                            )
                        )
                        self.every_place_ball[pos] = self.rainBalls[-1]
            self.idx += 1

        for ball in self.shortBalls:
            ball.update()

        for ball in self.longBalls:
            ball.update()

        for ball in self.rainBalls:
            ball.update()

        for particle in self.particles:
            particle.update()

    def check(self):
        for ball in self.shortBalls:
            if ball.is_out_of_line():
                self.score -= 20
                self.miss += 1
                self.continue_bit = 0
                self.shortBalls.remove(ball)
                del ball

        for ball in self.longBalls:
            if ball.is_out_of_line():
                if ball.score == 0:
                    self.score -= 100
                    self.continue_bit = 0
                    self.miss += 1
                elif ball.score == 1:
                    self.score -= 25
                    self.good += 1
                elif ball.score == 2:
                    self.prefect += 1
                self.longBalls.remove(ball)
                del ball

        for ball in self.rainBalls:
            if ball.is_out_of_line():
                self.score -= 10
                self.miss += 1
                self.continue_bit = 0
                self.rainBalls.remove(ball)
                del ball

        for particle in self.particles:
            if particle.is_out_of_line():
                self.particles.remove(particle)
                del particle

    def check_long_and_rain(self):
        is_any_key_pressed = any(pygame.key.get_pressed())  # 检查是否有键被按下
        if is_any_key_pressed:
            for ball in self.longBalls:
                if ball.ischeck:
                    if ball.ischeck % 10 == 0:
                        self.continue_bit += 1
                        self.particles.extend(
                            make_particles(
                                ball.x + 25 / 1536 * WIDTH,
                                TEST_Y + 25 * WIDTH // 1536,
                                green if ball.score == 2 else blue,
                            )
                        )
                    ball.ischeck += 1

            for ball in self.rainBalls:
                check = ball.check()
                if check:  # 检查球是否被击中且未被检查
                    if self.effect:
                        threading.Thread(target=sound_effect.play).start()
                    log.debug("rain")
                    self.continue_bit += 1
                    self.prefect += 1
                    self.particles.extend(
                        make_particles(
                            ball.x + 25 / 1536 * WIDTH,
                            TEST_Y + 25 * WIDTH // 1536,
                            green,
                        )
                    )
                    self.rainBalls.remove(ball)
                    del ball

    def check_short_and_long(self, event):
        if event.type == pygame.KEYDOWN:  # 检测是否有键被按下
            cnt = sum(pygame.key.get_pressed())  # 获取按下的键的数量
            log.debug(cnt)
            for ball in self.shortBalls:
                check = ball.check()  # 检查球是否被击中
                if check and cnt:
                    if self.effect:
                        threading.Thread(target=sound_effect.play).start()
                    cnt -= 1
                    self.score -= 5 * (2 - check)
                    self.continue_bit += 1
                    if check == 1:
                        self.good += 1
                        self.particles.extend(
                            make_particles(
                                ball.x + 25 / 1536 * WIDTH,
                                TEST_Y + 25 * WIDTH // 1536,
                                blue,
                            )
                        )
                        self.shortBalls.remove(ball)
                        del ball
                    elif check == 2:
                        self.prefect += 1
                        self.particles.extend(
                            make_particles(
                                ball.x + 25 / 1536 * WIDTH,
                                TEST_Y + 25 * WIDTH // 1536,
                                green,
                            )
                        )
                        self.shortBalls.remove(ball)
                        del ball

            for ball in self.longBalls:
                check = ball.check()
                if check and not ball.ischeck:  # 检查球是否被击中且未被检查
                    ball.ischeck = 1
                    if cnt == 0:
                        continue
                    if self.effect:
                        threading.Thread(target=sound_effect.play).start()
                    cnt -= 1
                    ball.score = check

    def wait_three_seconds(self, window, obj):
        start_time = time.time()
        f = pygame.font.Font("./font/SanJiLuRongTi/SanJiLuRongTi-2.ttf", 200)
        while time.time() - start_time < 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            obj.draw(window)
            text = f.render(
                str(int(4 - time.time() + start_time)), True, (255, 255, 255)
            )
            window.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2,
                ),
            )
            pygame.display.update()
            clock.tick(60)

    def is_check_setting(self, event, window):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if (
                25 / 1536 * WIDTH <= pos[0] <= 97 / 1536 * WIDTH
                and pos[1] >= 40 / 1536 * WIDTH
                and pos[1] <= 112 / 1536 * WIDTH
                and event.button == 1
            ):  # 检测是否点击了暂停按钮
                self.pause()  # 暂停
                musicpauser = MUSICPAUSER()  # 创建一个MUSICPAUSER对象
                while not musicpauser.choice:
                    clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if musicpauser.check(event) == "continue":
                            self.wait_three_seconds(window, self)
                            self.continue_play()
                            return "notReturn"
                    musicpauser.draw(window)
                    pygame.display.update()
                threading.Thread(target=lambda: enter_music_effect.play()).start()
                return self.father

    def __str__(self):
        return "Music"
