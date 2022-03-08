import pygame
from pygame.locals import *
import sys

from const import *

class Performer(pygame.sprite.Sprite):
    def __init__(self, id, x, y, w, h, status, image):
        pygame.sprite.Sprite.__init__(self)
        self.status = status    # 状態
        self.image = pygame.image.load(image)
        self.image = self.image.convert()
        self.image.set_colorkey((255, 255, 255))  # 白を透過色に指定
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = self.vy = 0
        self.init_x, self.init_y = (x, y)
        self.init_status = status
        self.id = id
        self.down = False
        self.inactive_y = 0

    def back_origin(self, seesaw):
        xmove = self.init_x - self.rect.x
        ymove = self.init_y - self.rect.y
        self.rect.move_ip(xmove, ymove)  # 初期位置に戻す
        self.vx = self.vy = 0
        if self.id == 1:    # Jumperの時
            self.vx = 2
        self.status = self.init_status
        self.down = False
        if self.id == 2:
            seesaw.ride(self)

    def update(self):
        if self.status == STATE_JUMPING:
            self.vy += GRAVITY
            self.vy = min(self.vy, MAX_VY)
            self.rect.move_ip(self.vx, self.vy)
        else:
            self.vy = 0
            self.rect.move_ip(self.vx, 0)
        if self.status == STATE_JUMPING:
            if self.rect.y + self.rect.h > SOUTH:
                self.vy = 0
                self.down = True
            if self.rect.x <= WEST:  # 壁で跳ね返る
                if self.vx < 0:
                    self.vx = -self.vx
                elif self.vx == 0:
                    self.vx = 1
            if self.rect.x + self.rect.w >= EAST:
                if self.vx > 0:
                    self.vx = -self.vx
                elif self.vx == 0:
                    self.vx = -1
            if self.rect.y <= NORTH:
                self.vy = -self.vy

    def move(self, vx):
        self.vx = vx

    # 着地点に応じて、加速する
    def check(self, seesaw):
        x_diff = self.rect.x - seesaw.rect.x
        # id:1は左に着地、id:2は右に着地しないと、アウト
        # はみ出したらアウト
        if self.id == 1:
            if (x_diff+self.rect.w < 0 \
                or x_diff + self.rect.w/2 > JUMP_CENTER):
                return (0, 0)
            x_offset = -1
        else:
            if (x_diff + self.rect.w/2 < JUMP_CENTER \
                or x_diff > seesaw.rect.w):
                return (0, 0)
            else:
                x_diff = seesaw.rect.w - x_diff - self.rect.w
            x_offset = 1
        # ここで、0 <= x_diff <= JUMP_CENTER となる。
        # 0の時2倍、JUMP_CENTERの時 0.5倍に線形に変換する。
        rate = 2 - 1.5 * x_diff / JUMP_CENTER
        x_offset *= rate
        return (x_offset, rate)

    def landed(self, seesaw):
        vy = self.vy
        vx = self.vx
        self.vy = 0
        self.status = STATE_STANDING
        # 現在座標から引き上げる分だけ移動
        ymove = seesaw.rect.y + seesaw.rect.h - self.rect.h - 1 - self.rect.y
        if self.id == 1:
            xmove = seesaw.rect.x - self.rect.x
        else:
            xmove = (seesaw.rect.x + seesaw.rect.w - self.rect.w) - self.rect.x
        self.rect.move_ip(xmove, ymove)
        seesaw.ride(self)  # vxの値を一致させる
        return (vx, vy)

    def jump(self, vx, vy, seesaw):
        self.vx = vx
        self.vy = vy
        self.status = STATE_JUMPING
        ymove = SEESAW_Y - PERFORMER_H - 1 \
                - self.rect.y - seesaw.rect.h
        self.rect.move_ip(self.vx, ymove)
        self.inactive_y = self.rect.y - seesaw.rect.y + self.rect.h