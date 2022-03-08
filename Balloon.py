import pygame
from pygame.locals import *
import sys

from const import *

class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y, d, vx, score, image1, image2):
        pygame.sprite.Sprite.__init__(self)
        self.vx = vx     # 縦方向には動かない
        self.image = self.image1 = image1
        self.image2 = image2
        self.rect = pygame.Rect(x, y, d, d)
        self.score = score
        self.balloon_tilt = 0

    def update(self):
        # 描画位置を移動させる
        self.rect.move_ip(self.vx, 0)
        if self.rect.x < - BALLOON_DIAM:   # 左に消えるまで表示
            self.rect.move_ip(BALLOON_JUMP, 0)
        if self.rect.x > EAST:             # 右に消えるまで表示
            self.rect.move_ip(- BALLOON_JUMP, 0)
        if self.balloon_tilt < FPS/2:  # 0.5 秒ごとに傾く
            self.image = self.image1
        else:
            self.image = self.image2

    def bump(self, performer):   # パフォーマとの衝突
        performer.vy = - performer.vy
        return self.score

    def set_balloon_tilt(self, balloon_tilt):
        self.balloon_tilt = balloon_tilt