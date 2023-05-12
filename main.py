import pygame
import sys
import math
import random
from pygame.locals import *  # pygame.の省略用コード※関数は省略不可

# 画像
img_bg = pygame.image.load("images/background.png")
img_pl = [
    pygame.image.load("images/player.png"),
    pygame.image.load("images/player_l.png"),
    pygame.image.load("images/player_r.png"),
    pygame.image.load("images/player_burner.png"),
]
img_bu = pygame.image.load("images/bullet.png")
img_en1 = [
    pygame.image.load("images/enemy1.png"),
    pygame.image.load("images/enemy1_atk.png"),
]
img_exp = [
    None,
    pygame.image.load("images/explosion1.png"),
    pygame.image.load("images/explosion2.png"),
    pygame.image.load("images/explosion3.png"),
    pygame.image.load("images/explosion4.png"),
    pygame.image.load("images/explosion5.png"),
]
img_energy = pygame.image.load("images/energy.png")
img_title = [
    pygame.image.load("images/nebula.png"),
    pygame.image.load("images/logo.png"),
]

# 色
BLACK = (0, 0, 0)
SILVER = (192, 208, 224)
RED = (255, 0, 0)
CYAN = (0, 224, 255)

# ============ 定数 ============
BULLET_MAX = 100  # 発射できる弾の数（最大値）
ENEMY_MAX = 100  # 敵の数（最大値）
EXPLODE_MAX = 100  # 爆発演出の数（最大値）
LINE = [-80, 800, -80, 1040]  # 敵の出現エリア枠(上, 下, 左, 右)

# ============ 変数 ============
phase = 0  # フェーズ
score = 0  # スコア
bg_y = 0  # 背景スクロール用
tmr = 0  # タイマー
k_space = 0  # スペースキー用
k_z = 0  # zキー用

# プレイヤー
pl_x = 480  # x座標
pl_y = 360  # y座標
pl_d = 0  # 傾き
pl_e = 0  # エネルギー
pl_m = 0  # 無敵状態
# 弾
bu_no = 0  # リスト番号
bu_f = [False] * BULLET_MAX  # 発射中フラグ
bu_x = [0] * BULLET_MAX  # x座標
bu_y = [0] * BULLET_MAX  # y座標
bu_a = [0] * BULLET_MAX  # 角度
# 敵1
en1_no = 0  # リスト番号
en1_f = [False] * ENEMY_MAX  # 発射中フラグ
en1_x = [0] * ENEMY_MAX  # x座標
en1_y = [0] * ENEMY_MAX  # y座標
en1_a = [0] * ENEMY_MAX  # 角度
en1_type = [0] * ENEMY_MAX  # 種類（本体or弾）
en1_speed = [0] * ENEMY_MAX  # スピード
# 爆発
exp_no = 0  # リスト番号
exp_p = [0] * EXPLODE_MAX  # 画像番号
exp_x = [0] * EXPLODE_MAX  # x座標
exp_y = [0] * EXPLODE_MAX  # y座標


# 2点間の距離を求める関数
def get_dis(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


# プレイヤー操作関数
def movd_pl(src, key):
    global pl_x, pl_y, pl_d, k_space, k_z, pl_e, pl_m
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
    if k_z == 1 and pl_e > 10:
        set_bullet(10)
        pl_e -= 10
    # 描画処理
    if pl_m % 2 == 0:
        src.blit(img_pl[3], [pl_x - 8, pl_y + 40 + (tmr % 3) * 2])
        src.blit(img_pl[pl_d], [pl_x - 37, pl_y - 48])
    if pl_m > 0:
        pl_m -= 1
        return
    # 敵との接触チェック
    for i in range(ENEMY_MAX):
        if en1_f[i]:
            w = img_en1[en1_type[i]].get_width()
            h = img_en1[en1_type[i]].get_height()
            r = int((w + h) / 4 + (74 + 96) / 4)
            if get_dis(en1_x[i], en1_y[i], pl_x, pl_y) < r**2:
                set_effect(en1_x[i], en1_y[i])
                pl_e -= 10
                if pl_e <= 0:
                    pl_e = 0
                if pl_m == 0:
                    pl_m = 60
                en1_f[i] = False


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
            img_rz = pygame.transform.rotozoom(img_bu, -90 - bu_a[i], 1.0)
            src.blit(
                img_rz,
                [bu_x[i] - img_rz.get_width() / 2, bu_y[i] - img_rz.get_height() / 2],
            )
            if bu_y[i] < 0 or bu_x[i] < 0 or bu_x[i] > 960:
                bu_f[i] = False


# 敵の出現関数
def appear_enemy():
    if tmr % 30 == 0:
        set_enemy(random.randint(20, 940), LINE[0], 90, 0, 6)


# 敵のセット関数
def set_enemy(x, y, a, ty, sp):
    global en1_no
    while True:
        if not en1_f[en1_no]:
            en1_f[en1_no] = True
            en1_x[en1_no] = x
            en1_y[en1_no] = y
            en1_a[en1_no] = a
            en1_type[en1_no] = ty
            en1_speed[en1_no] = sp
            break
        en1_no = (en1_no + 1) % ENEMY_MAX


# 敵の移動関数
def move_enemy(scrn):
    global pl_e
    for i in range(ENEMY_MAX):
        if en1_f[i]:
            ang = -90 - en1_a[i]
            png = en1_type[i]
            en1_x[i] += en1_speed[i] * math.cos(math.radians(en1_a[i]))
            en1_y[i] += en1_speed[i] * math.sin(math.radians(en1_a[i]))
            if en1_type[i] == 0 and en1_y[i] > 360:
                # 弾の発射
                set_enemy(en1_x[i], en1_y[i], 90, 1, 8)
                en1_a[i] = -45
                en1_speed[i] = 16
            if (
                en1_x[i] < LINE[2]
                or LINE[3] < en1_x[i]
                or en1_y[i] < LINE[0]
                or LINE[1] < en1_y[i]
            ):
                en1_f[i] = False
            # 弾と敵の接触判定
            if en1_type[i] != 1:
                w = img_en1[en1_type[i]].get_width()
                h = img_en1[en1_type[i]].get_height()
                r = int((w + h) / 4 + 12)
                for n in range(BULLET_MAX):
                    if (
                        bu_f[n]
                        and get_dis(en1_x[i], en1_y[i], bu_x[n], bu_y[n]) < r**2
                    ):
                        bu_f[n] = False
                        en1_f[i] = False
                        set_effect(en1_x[i], en1_y[i])
                        if pl_e < 100:
                            pl_e += 1
            # 描画処理
            img_rz = pygame.transform.rotozoom(img_en1[png], ang, 1.0)
            scrn.blit(
                img_rz,
                [en1_x[i] - img_rz.get_width() / 2, en1_y[i] - img_rz.get_height() / 2],
            )


# 爆発のセット関数
def set_effect(x, y):
    global exp_no
    exp_p[exp_no] = 1
    exp_x[exp_no] = x
    exp_y[exp_no] = y
    exp_no = (exp_no + 1) % EXPLODE_MAX


# 爆発の演出
def draw_explode(srcn):
    for i in range(EXPLODE_MAX):
        if exp_p[i] >= 1:
            srcn.blit(img_exp[exp_p[i]], [exp_x[i] - 48, exp_y[i] - 48])
            exp_p[i] += 1
            if exp_p[i] > 5:
                exp_p[i] = 0


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
        appear_enemy()
        move_enemy(screen)
        draw_explode(screen)
        screen.blit(img_energy, [40, 680])
        pygame.draw.rect(
            screen, (64, 32, 32), [40 + pl_e * 4, 680, (100 - pl_e) * 4, 12]
        )

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
