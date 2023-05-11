import pygame
import sys

# 画像
img_bg = pygame.image.load("images/background.png")
img_pl = pygame.image.load("images/player.png")

# ============ 変数 ============
bg_y = 0  # 背景スクロール用
# プレイヤー
pl_x = 480  # x座標
pl_y = 360  # y座標


# プレイヤー操作関数
def movd_pl(src, key):
    global pl_x, pl_y
    if key[pygame.K_UP] == 1:
        pl_y -= 20
        if pl_y < 80:
            pl_y = 80
    if key[pygame.K_DOWN] == 1:
        pl_y += 20
        if pl_y > 640:
            pl_y = 640
    if key[pygame.K_LEFT] == 1:
        pl_x -= 20
        if pl_x < 40:
            pl_x = 40
    if key[pygame.K_RIGHT] == 1:
        pl_x += 20
        if pl_x > 920:
            pl_x = 920
    src.blit(img_pl, [pl_x - 37, pl_y - 48])


def main():
    global bg_y
    pygame.init()
    pygame.display.set_caption("Shooting Game")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # F1キーでフルスクリーンモード
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((960, 720), pygame.FULLSCREEN)
                # F2キー or ESCキーで通常表示
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((960, 720))

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
