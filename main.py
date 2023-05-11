import pygame
import sys

# 画像
img_bg = pygame.image.load("images/galaxy.png")

# ============ 変数 ============
bg_y = 0 # 背景スクロール用

def main():
    global bg_y
    pygame.init()
    pygame.display.set_caption("Shooting Game")
    screen = pygame.display.set_mode((960,720))
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # F1キーでフルスクリーンモード
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((960,720),pygame.FULLSCREEN)
                # F2キー or ESCキーで通常表示
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((960,720))
                    
        # 背景スクロール処理
        bg_y = (bg_y + 16) % 720
        screen.blit(img_bg,[0,bg_y -720])
        screen.blit(img_bg,[0,bg_y])
        
        pygame.display.update()
        clock.tick(30)
    
if __name__ == "__main__":
    main()