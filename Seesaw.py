import pygame
from pygame.locals import *
import sys

from const import *

class Seesaw(pygame.sprite.Sprite):
    def __init__(self, x, y, l, h, speed, image1, image2):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed     # 縦方向には動かない
        self.image1 = pygame.image.load(image1)  # 左下がりの絵
        self.image1 = self.image1.convert()
        self.image1.set_colorkey((255, 255, 255))  # 白を透過色に指定
        self.image2 = pygame.image.load(image2)  # 右下がりの絵
        self.image2 = self.image2.convert()
        self.image2.set_colorkey((255, 255, 255))  # 白を透過色に指定
        self.image = self.image1
        self.rect = pygame.Rect(x, y, l, h)
        self.init_x = x
        self.vx = 0            # 初期状態は静止

    def back_origin(self):  # 1ダウンの後、初期位置に戻す
        xmove = self.init_x - self.rect.x
        self.rect.move_ip(xmove, 0)
        self.image = self.image1
        self.vx = 0

    def update(self):
        if self.rect.x + self.vx < WEST:  # 左端
            self.rect.move_ip(-self.rect.x, 0)
            self.vx = 0
            self.rider.move(0)  # 立ってる人も停止させる
        elif self.rect.x + self.rect.w + self.vx > EAST: # 右端
            self.rect.move_ip(EAST - self.rect.w - self.rect.x, 0)
            self.vx = 0
            self.rider.move(0)
        else:
            self.rect.move_ip(self.vx, 0)

    def move_left(self):
        self.vx = -self.speed
        self.rider.move(self.vx)  # 立ってる人も同じスピードで移動させる

    def move_right(self):
        self.vx = self.speed
        self.rider.move(self.vx)

    def stop(self):
        self.vx = 0
        self.rider.move(0)

    def ride(self, performer):
        self.rider = performer
        self.rider.move(self.vx)  # シーソーと同速度で水平異動
        if self.image == self.image2:  # シーソーの絵を切り替え
            self.image = self.image1   # 参照だけ切り替え
        else:
            self.image = self.image2