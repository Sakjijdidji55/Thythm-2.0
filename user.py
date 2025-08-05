import sys

import pygame

from load import (
    HEIGHT,
    WIDTH,
    board,
    font,
    font1,
    icon,
    return_img,
    set_img,
    userboard,
    window,
)
from userData import set_user_inform, user_inform, user_inform_path

authors = ["正趣果上课", "14911.", "友人A", "风笙"]
information = ["24级FZU", "24级CDUT", "24级CMC", "24级SWMU"]


def show():
    about = font.render("作者: ", True, (0, 0, 0))
    window.blit(
        about,
        (WIDTH - userboard.get_width() + 100 / 1536 * WIDTH, 220 / 1536 * WIDTH),
    )  # 在用户面板上绘制作者

    author = font.render("迷路的小朋友", True, (0, 0, 0))
    window.blit(
        author,
        (
            WIDTH - userboard.get_width() // 3 - author.get_width() // 2,
            270 / 1536 * WIDTH,
        ),
    )

    info = font1.render("24级SYSU", True, (0, 0, 0))
    window.blit(
        info,
        (
            WIDTH - userboard.get_width() // 3 - info.get_width() // 2,
            300 / 1536 * WIDTH,
        ),
    )

    # 在用户面板上绘制创作者们
    helper = font.render("协作者: ", True, (0, 0, 0))
    window.blit(
        helper, (WIDTH - userboard.get_width() + 175 / 1536 * WIDTH, 370 / 1536 * WIDTH)
    )

    for i in range(len(authors)):
        author = font.render(authors[i], True, (0, 0, 0))
        window.blit(
            author,
            (
                WIDTH - userboard.get_width() // 3 - author.get_width() // 2,
                430 / 1536 * WIDTH + 70 * i,
            ),
        )  # 在用户面板上绘制创作者们

    for i in range(len(information)):
        info = font1.render(information[i], True, (0, 0, 0))
        window.blit(
            info,
            (
                WIDTH - userboard.get_width() // 3 - info.get_width() // 2,
                460 / 1536 * WIDTH + 70 * i,
            ),
        )


class User:
    def __init__(self, name, icon_path, description):
        self.name = name
        self.show = False
        self.description = description
        self.icon = pygame.transform.scale(
            pygame.image.load(icon_path), (100 / 1536 * WIDTH, 100 / 1536 * WIDTH)
        )

    def draw(self, window: pygame.Surface):
        if self.show:
            window.blit(userboard, (WIDTH - userboard.get_width(), 0))
            window.blit(
                self.icon,
                (WIDTH - userboard.get_width() + 10 / 1536 * WIDTH, 10 / 1536 * WIDTH),
            )  # 在用户面板上绘制用户头像

            name = font.render("User: " + self.name, True, (0, 0, 0))
            window.blit(
                name,
                (
                    WIDTH - userboard.get_width() // 2 - name.get_width() // 2,
                    50 / 1536 * WIDTH,
                ),
            )  # 在用户面板上绘制用户名称

            description = font.render("简介: " + self.description, True, (0, 0, 0))
            window.blit(
                description,
                (
                    WIDTH - userboard.get_width() // 2 - description.get_width() // 2,
                    135 / 1536 * WIDTH,
                ),
            )  # 在用户面板上绘制用户简介

            show()

            window.blit(
                set_img,
                (
                    WIDTH - set_img.get_width() - 25 / 1536 * WIDTH,
                    HEIGHT - set_img.get_height() * 2 - 80 / 1536 * WIDTH,
                ),
            )
            window.blit(
                return_img,
                (
                    WIDTH - return_img.get_width() - 25 / 1536 * WIDTH,
                    HEIGHT - return_img.get_height() - 40 / 1536 * WIDTH,
                ),
            )

        window.blit(
            icon, (WIDTH - icon.get_width() - 20 / 1536 * WIDTH, 20 / 1536 * WIDTH)
        )

    def check(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (
                    WIDTH - icon.get_width() - 20 / 1536 * WIDTH
                    < pos[0]
                    < WIDTH - 20 / 1536 * WIDTH
                    and 20 / 1536 * WIDTH
                    < pos[1]
                    < 20 / 1536 * WIDTH + icon.get_height()
                ):
                    return "User"  # 检查鼠标点击的位置是否在用户图标的范围内
                if (
                    WIDTH - userboard.get_width()
                    < pos[0]
                    < WIDTH - userboard.get_width() + board.get_width()
                    and 0 < pos[1] < board.get_height()
                ):
                    set_user_inform(user_inform_path=user_inform_path)
                    self.name = user_inform["name"]
                    self.description = user_inform["description"]
                    self.icon = pygame.transform.scale(
                        pygame.image.load(user_inform["icon_path"]),
                        (100 / 1536 * WIDTH, 100 / 1536 * WIDTH),
                    )
                    return "Board"  # 如果点击了用户界面，则返回"Board"，并且弹出修改用户信息的窗口
                if (
                    WIDTH - set_img.get_width() - 25 / 1536 * WIDTH
                    < pos[0]
                    < WIDTH - 25 / 1536 * WIDTH
                    and HEIGHT - set_img.get_height() * 2 - 80 / 1536 * WIDTH
                    < pos[1]
                    < HEIGHT - set_img.get_height() - 80 / 1536 * WIDTH
                ):
                    return "Set"  # 如果点击了设置按钮，则返回"Set"
                if (
                    WIDTH - return_img.get_width() - 25 / 1536 * WIDTH
                    < pos[0]
                    < WIDTH - 25 / 1536 * WIDTH
                    and HEIGHT - return_img.get_height() - 40 / 1536 * WIDTH
                    < pos[1]
                    < HEIGHT - 40 / 1536 * WIDTH
                ):
                    pygame.quit()
                    sys.exit()  # 如果点击了返回按钮，则退出程序


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    user = User("迷路的小朋友", "image/icon.png", "24级SYSU")
    while running:
        for event in pygame.event.get():
            result = user.check(event)
            if result is not None:
                if result == "User":
                    user.show = not user.show
                print(result)
                break
        user.draw(screen)
        pygame.display.flip()
        clock.tick(60)
