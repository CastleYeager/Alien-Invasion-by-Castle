"""
管理外星人类的模块，维护外星人的所有行为
"""
import pygame
from pygame.sprite import Sprite


# 外星人类，管理外星人的所有行为
class Alien(Sprite):
    # 初始化一只外星人，创建时使其位于屏幕的左上角附近
    def __init__(self, screen, settings):
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings
        # 载入外星人图片
        self.image = pygame.image.load(r'images\alien.bmp')
        # 获取外星人的坐标变量
        self.rect = self.image.get_rect()
        # 通过坐标，控制外星人初始化时在屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 获取外星人的准确位置
        self.x = float(self.rect.x)

    # 绘制外星人到屏幕上
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # 更新外星人位置的方法
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    # 检查外星人是否达到屏幕边界的方法
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.x >= screen_rect.width:
            return True
        elif self.rect.x <= 0:
            return True
