import pygame
import sys
import math
from pygame.locals import *  # pygame.の省略用コード※関数は省略不可

# 画像
img_bg = pygame.image.load("images/background.png")
img_pl = [
    pygame.image.load("images/player.png"),
    pygame.image.load("images/player_l.png"),
    pygame.image.load("images/player_r.png"),
    pygame.image.load("images/player_burner.png"),
]
imb_bu = pygame.image.load("images/bullet.png")

# ============ 定数 ============
BULLET_MAX = 100  # 発射できる弾の数

# ============ 変数 ============
bg_y = 0  # 背景スクロール用
tmr = 0  # タイマー
k_space = 0  # スペースキー用
k_z = 0  # zキー用
# プレイヤー
pl_x = 480  # x座標
pl_y = 360  # y座標
pl_d = 0  # 傾き
# 弾
bu_no = 0
bu_f = [False] * BULLET_MAX  # 発射中フラグ
bu_x = [0] * BULLET_MAX  # x座標
bu_y = [0] * BULLET_MAX  # y座標
bu_a = [0] * BULLET_MAX  # 角度


# プレイヤー操作関数
def movd_pl(src, key):
    global pl_x, pl_y, pl_d, k_space, k_z
    pl_d = 0
    # キー操作処理(1は押したとき)
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
    k_space = (k_space + 1) * key[K_SPACE]
    if k_space % 5 == 1:
        set_bullet(0)
    k_z = (k_z + 1) * key[K_z]
    if k_z == 1:
        set_bullet(10)
    src.blit(img_pl[3], [pl_x - 8, pl_y + 40 + (tmr % 3) * 2])
    src.blit(img_pl[pl_d], [pl_x - 37, pl_y - 48])


# 弾のセット関数
def set_bullet(typ):
    global bu_no
    # 単発
    if typ == 0:
        bu_f[bu_no] = True
        bu_x[bu_no] = pl_x
        bu_y[bu_no] = pl_y - 50
        bu_a[bu_no] = 270
        bu_no = (bu_no + 1) % BULLET_MAX
    # 放射
    if typ == 10:
        for a in range(160, 390, 10):
            bu_f[bu_no] = True
            bu_x[bu_no] = pl_x
            bu_y[bu_no] = pl_y - 50
            bu_a[bu_no] = a
            bu_no = (bu_no + 1) % BULLET_MAX


# 弾の移動関数
def move_bullet(src):
    for i in range(BULLET_MAX):
        if bu_f[i]:
            bu_x[i] += 36 * math.cos(math.radians(bu_a[i]))
            bu_y[i] += 36 * math.sin(math.radians(bu_a[i]))
            img_rz = pygame.transform.rotozoom(imb_bu, -90 - bu_a[i], 1.0)
            src.blit(
                img_rz,
                [bu_x[i] - img_rz.get_width() / 2, bu_y[i] - img_rz.get_height() / 2],
            )
            if bu_y[i] < 0 or bu_x[i] < 0 or bu_x[i] > 960:
                bu_f[i] = False


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
        move_bullet(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
