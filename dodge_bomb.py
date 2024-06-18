import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectか爆弾Rect
    戻り値:タプル（横方向判定効果, 縦方向判定効果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate  = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:  # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()  # rectを取得
    kk_rct.center = 900, 400  # 中心を900, 400にする
    bomb = pg.Surface((20, 20))  # 爆弾surfaceを生成
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)  # 爆弾をsurfaceに描画
    bomb.set_colorkey((0, 0, 0))  # 爆弾の隅を透明にする
    bomb_rct = bomb.get_rect()  # rectを取得
    bomb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) 
    vx, vy = +5, +5  # 爆弾の横方向速度、縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 元の場所に戻す
        screen.blit(kk_img, kk_rct)
        bomb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bomb_rct)
        if not yoko:  # 横にはみ出たら
            vx *= -1
        if not tate:  # 縦にはみ出たら
            vy *= -1
        screen.blit(bomb, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
