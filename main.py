import pygame
import sys
from pygame.locals import *  # pygame.の省略用コード

# 画像
img_bg = pygame.image.load("images/background.png")
img_pl = [
    pygame.image.load("images/player.png"),
    pygame.image.load("images/player_l.png"),
    pygame.image.load("images/player_r.png"),
    pygame.image.load("images/player_burner.png"),
]

# ============ 変数 ============
bg_y = 0  # 背景スクロール用
tmr = 0  # タイマー
# プレイヤー
pl_x = 480  # x座標
pl_y = 360  # y座標
pl_d = 0  # 傾き


# プレイヤー操作関数
def movd_pl(src, key):
    global pl_x, pl_y, pl_d
    pl_d = 0
    if key[K_UP] == 1:
        pl_y -= 20
        if pl_y < 80:
            pl_y = 80
    if key[K_DOWN] == 1:
        pl_y += 20
        if pl_y > 640:
            pl_y = 640
    if key[K_LEFT] == 1:
        pl_d = 1
        pl_x -= 20
        if pl_x < 40:
            pl_x = 40
    if key[K_RIGHT] == 1:
        pl_d = 2
        pl_x += 20
        if pl_x > 920:
            pl_x = 920
    src.blit(img_pl[3], [pl_x - 8, pl_y + 40 + (tmr % 3) * 2])
    src.blit(img_pl[pl_d], [pl_x - 37, pl_y - 48])


def main():
    global bg_y, tmr
    pygame.init()
    pygame.display.set_caption("Shooting Game")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # F1キーでフルスクリーンモード
                if event.key == K_F1:
                    screen = pygame.display.set_mode((960, 720), FULLSCREEN)
                # F2キー or ESCキーで通常表示
                if event.key == pygame.K_F2 or event.key == K_ESCAPE:
                    screen = pygame.display.set_mode((960, 720))

        tmr += 1

        # 背景スクロール処理
        bg_y = (bg_y + 16) % 720
        screen.blit(img_bg, [0, bg_y - 720])
        screen.blit(img_bg, [0, bg_y])

        key = pygame.key.get_pressed()
        movd_pl(screen, key)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
