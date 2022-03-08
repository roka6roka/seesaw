import pygame
from pygame.locals import *
import sys

from const import *

class JumpBoard(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, w, h)
        self.id = id
        if x < X_CENTER:
            self.side = LEFT_BOARD   # 左と右の区別
        else:
            self.side = RIGHT_BOARD

    def bump(self, performer):
        if performer.vy < 0:    # 下からの衝突では、透過させる
            return
        performer.vy = - performer.vy
        # 少し浮かせる
        performer.rect.y = self.rect.y - performer.rect.h - 2
        if -1 <= performer.vx <= 1: # ジャンプ台で止まってしまわないように
            if self.side == LEFT_BOARD:
                performer.vx = -2
            else:
                performer.vx = 2