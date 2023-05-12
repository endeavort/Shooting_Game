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
img_enemy = [
    pygame.image.load("images/enemy4_atk.png"),
    pygame.image.load("images/enemy1.png"),
    pygame.image.load("images/enemy2.png"),
    pygame.image.load("images/enemy3.png"),
    pygame.image.load("images/enemy4.png"),
    pygame.image.load("images/enemy_boss.png"),
    pygame.image.load("images/enemy_boss_f.png"),
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
hiscore = 10000  # ハイスコア
new_record = False  # 記録更新フラグ
bg_y = 0  # 背景スクロール用
tmr = 0  # タイマー
k_space = 0  # スペースキー用
k_z = 0  # zキー用

# プレイヤー
pl_x = 0  # x座標
pl_y = 0  # y座標
pl_d = 0  # 傾き
pl_e = 0  # エネルギー
pl_m = 0  # 無敵状態
# 弾
bu_no = 0  # リスト番号
bu_f = [False] * BULLET_MAX  # 発射中フラグ
bu_x = [0] * BULLET_MAX  # x座標
bu_y = [0] * BULLET_MAX  # y座標
bu_a = [0] * BULLET_MAX  # 角度
# 敵
en_no = 0  # リスト番号
en_f = [False] * ENEMY_MAX  # 発射中フラグ
en_x = [0] * ENEMY_MAX  # x座標
en_y = [0] * ENEMY_MAX  # y座標
en_a = [0] * ENEMY_MAX  # 角度
en_type = [0] * ENEMY_MAX  # 種類（本体or弾）
en_speed = [0] * ENEMY_MAX  # スピード
en_s = [0] * ENEMY_MAX  # シールド
en_c = [0] * ENEMY_MAX  # カウント
# 爆発
exp_no = 0  # リスト番号
exp_p = [0] * EXPLODE_MAX  # 画像番号
exp_x = [0] * EXPLODE_MAX  # x座標
exp_y = [0] * EXPLODE_MAX  # y座標
# SE
se_radiation = None  # 放射
se_damage = None  # ダメージ
se_explosion = None  # 爆発
se_shot = None  # 撃つ


# 2点間の距離を求める関数
def get_dis(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


# 立体文字描画関数
def draw_txt(scrn, txt, x, y, siz, col):
    fnt = pygame.font.Font(None, siz)
    cr = int(col[0] / 2)
    cg = int(col[1] / 2)
    cb = int(col[2] / 2)
    sur = fnt.render(txt, True, (cr, cg, cb))
    x -= sur.get_width() / 2
    y -= sur.get_height() / 2
    scrn.blit(sur, [x + 1, y + 1])
    cr = col[0] + 128
    if cr > 255:
        cr = 255
    cg = col[1] + 128
    if cg > 255:
        cg = 255
    cb = col[2] + 128
    if cb > 255:
        cb = 255
    sur = fnt.render(txt, True, (cr, cg, cb))
    scrn.blit(sur, [x - 1, y - 1])
    sur = fnt.render(txt, True, col)
    scrn.blit(sur, [x, y])


# プレイヤー操作関数
def move_pl(src, key):
    global pl_x, pl_y, pl_d, k_space, k_z, pl_e, pl_m, phase, tmr
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
        se_shot.play()
    k_z = (k_z + 1) * key[K_z]
    if k_z == 1 and pl_e > 10:
        set_bullet(10)
        se_radiation.play()
        pl_e -= 10
    # 描画処理
    if pl_m % 2 == 0:
        src.blit(img_pl[3], [pl_x - 8, pl_y + 40 + (tmr % 3) * 2])
        src.blit(img_pl[pl_d], [pl_x - 37, pl_y - 48])
    if pl_m > 0:
        pl_m -= 1
        return
    elif phase == 1:
        # 敵との接触チェック
        for i in range(ENEMY_MAX):
            if en_f[i]:
                w = img_enemy[en_type[i]].get_width()
                h = img_enemy[en_type[i]].get_height()
                r = int((w + h) / 4 + (74 + 96) / 4)
                if get_dis(en_x[i], en_y[i], pl_x, pl_y) < r**2:
                    set_effect(en_x[i], en_y[i])
                    pl_e -= 10
                    if pl_e <= 0:
                        pl_e = 0
                        phase = 2
                        tmr = 0
                    if pl_m == 0:
                        pl_m = 60
                        se_damage.play()
                    if en_type[i] < 5:
                        en_f[i] = False


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
    sec = tmr / 30
    # if 0 < sec < 15 and tmr % 60 == 0:
    #     set_enemy(random.randint(20, 940), LINE[0], 90, 1, 8, 1)
    # if 15 < sec < 30:
    #     set_enemy(random.randint(20, 940), LINE[0], 90, 2, 12, 1)
    # if 30 < sec < 45:
    #     set_enemy(random.randint(100, 860), LINE[0], random.randint(60, 120), 3, 6, 3)
    # if 45 < sec < 60:
    #     set_enemy(random.randint(100, 860), LINE[0], 90, 4, 12, 2)
    if tmr == 30 * 5:
        set_enemy(480, -210, 90, 5, 4, 200)


# 敵のセット関数
def set_enemy(x, y, a, ty, sp, s):
    global en_no
    while True:
        if not en_f[en_no]:
            en_f[en_no] = True
            en_x[en_no] = x
            en_y[en_no] = y
            en_a[en_no] = a
            en_type[en_no] = ty
            en_speed[en_no] = sp
            en_s[en_no] = s
            en_c[en_no] = 0
            break
        en_no = (en_no + 1) % ENEMY_MAX


# 敵の移動関数
def move_enemy(scrn):
    global pl_e, phase, tmr, score
    for i in range(ENEMY_MAX):
        if en_f[i]:
            ang = -90 - en_a[i]
            png = en_type[i]
            # 敵の動き
            if en_type[i] < 5:
                en_x[i] += en_speed[i] * math.cos(math.radians(en_a[i]))
                en_y[i] += en_speed[i] * math.sin(math.radians(en_a[i]))
                if en_type[i] == 4:
                    # 弾の発射
                    en_c[i] += 1
                    ang = en_c[i] * 10
                    if en_y[i] > 240 and en_a[i] == 90:
                        en_a[i] = random.choice([50, 70, 110, 130])
                        set_enemy(en_x[i], en_y[i], 90, 0, 6, 0)
                if (
                    en_x[i] < LINE[2]
                    or LINE[3] < en_x[i]
                    or en_y[i] < LINE[0]
                    or LINE[1] < en_y[i]
                ):
                    en_f[i] = False
            # ボスの動き
            else:
                if en_c[i] == 0:
                    en_y[i] += 2
                    if en_y[i] > 200:
                        en_c[i] = 1
                elif en_c[i] == 1:
                    en_x[i] -= en_speed[i]
                    if en_x[i] < 200:
                        for j in range(0, 10):
                            set_enemy(en_x[i], en_y[i] + 80, j * 20, 0, 6, 0)
                        en_c[i] = 2
                else:
                    en_x[i] += en_speed[i]
                    if en_x[i] > 760:
                        for j in range(0, 10):
                            set_enemy(en_x[i], en_y[i] + 80, j * 20, 0, 6, 0)
                        en_c[i] = 1
                if en_s[i] < 100 and tmr % 30 == 0:
                    set_enemy(en_x[i], en_y[i] + 80, random.randint(60, 120), 0, 6, 0)
            # 弾と敵の接触判定
            if en_type[i] != 0:
                w = img_enemy[en_type[i]].get_width()
                h = img_enemy[en_type[i]].get_height()
                r = int((w + h) / 4 + 12)
                er = int((w + h) / 4)
                for n in range(BULLET_MAX):
                    if bu_f[n] and get_dis(en_x[i], en_y[i], bu_x[n], bu_y[n]) < r**2:
                        bu_f[n] = False
                        set_effect(
                            en_x[i] + random.randint(-er, er),
                            en_y[i] + random.randint(-er, er),
                        )
                        if en_type[i] == 5:
                            png = en_type[i] + 1
                        en_s[i] -= 1
                        score += 100
                        if en_s[i] == 0:
                            en_f[i] = False
                            if pl_e < 100:
                                pl_e += 1
                            if en_type[i] == 5 and phase == 1:
                                phase = 3
                                tmr = 0
                                for j in range(10):
                                    set_effect(
                                        en_x[i] + random.randint(-er, er),
                                        en_y[i] + random.randint(-er, er),
                                    )
                                se_explosion.play()
            # 描画処理
            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0)
            scrn.blit(
                img_rz,
                [en_x[i] - img_rz.get_width() / 2, en_y[i] - img_rz.get_height() / 2],
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
    global bg_y, tmr, phase, score, pl_x, pl_y, pl_d, pl_e, pl_m
    global se_radiation, se_damage, se_explosion, se_shot
    pygame.init()
    pygame.display.set_caption("Shooting Game")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()
    se_radiation = pygame.mixer.Sound("sounds/radiation.ogg")
    se_damage = pygame.mixer.Sound("sounds/damage.ogg")
    se_explosion = pygame.mixer.Sound("sounds/explosion.ogg")
    se_shot = pygame.mixer.Sound("sounds/shot.ogg")

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

        # タイトル画面
        if phase == 0:
            img_rz = pygame.transform.rotozoom(img_title[0], -tmr % 360, 1.0)
            screen.blit(
                img_rz, [480 - img_rz.get_width() / 2, 280 - img_rz.get_height() / 2]
            )
            screen.blit(img_title[1], [70, 160])
            draw_txt(screen, "Press [SPACE] to start!", 480, 600, 50, SILVER)
            if key[K_SPACE] == 1:
                phase = 1
                tmr = 0
                score = 0
                pl_x = 480
                pl_y = 600
                pl_d = 0
                pl_e = 100
                pl_m = 0
                for i in range(ENEMY_MAX):
                    en_f[i] = False
                for i in range(BULLET_MAX):
                    bu_f[i] = False
                pygame.mixer.music.load("sounds/bgm.ogg")
                pygame.mixer.music.play(-1)

        # ゲーム画面
        if phase == 1:
            move_pl(screen, key)
            move_bullet(screen)
            appear_enemy()
            move_enemy(screen)
            if tmr == 30 * 60:
                phase = 3
                tmr = 0

        # ゲームオーバー
        if phase == 2:
            move_bullet(screen)
            move_enemy(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr <= 90:
                if tmr % 5 == 0:
                    set_effect(
                        pl_x + random.randint(-60, 60), pl_y + random.randint(-60, 60)
                    )
                if tmr % 10 == 10:
                    se_damage.play()
            if tmr == 120:
                pygame.mixer.music.load("sounds/gameover.ogg")
                pygame.mixer.music.play(0)
            if tmr > 120:
                draw_txt(screen, "GAME OVER", 480, 300, 80, RED)
            if tmr == 400:
                phase = 0
                tmr = 0

        # ゲームクリア
        if phase == 3:
            move_pl(screen, key)
            move_bullet(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr == 2:
                pygame.mixer.music.load("sounds/gameclear.ogg")
                pygame.mixer.music.play(0)
            if tmr > 20:
                draw_txt(screen, "GAME CLEAR", 480, 300, 80, SILVER)
            if tmr == 300:
                phase = 0
                tmr = 0

        draw_explode(screen)
        draw_txt(screen, "SCORE " + str(score), 200, 30, 50, SILVER)
        if phase != 0:
            screen.blit(img_energy, [40, 680])
            pygame.draw.rect(
                screen, (64, 32, 32), [40 + pl_e * 4, 680, (100 - pl_e) * 4, 12]
            )

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
