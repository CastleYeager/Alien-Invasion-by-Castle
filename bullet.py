"""
通过子弹类来管理子弹的所有功能和动作
"""
import pygame
# 子弹需要依靠精灵类来继承
from pygame.sprite import Sprite


class Bullet(Sprite):   # 之所以要继承自精灵类，是因为精灵类可以通过精灵编组类来管理一系列精灵对象
    """
    管理子弹的动作和方法
    """
    # 初始化子弹，即生成子弹，需要在飞船的顶部中间位置初始化出一枚子弹
    def __init__(self, screen, ship, settings):
        super().__init__()
        self.screen = screen
        # 先在（0，0）处初始化一个子弹对象，之后再将它移到正确的位置上
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        # 然后将初始化的子弹位置移动到飞船的中间顶部
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 需要将子弹的纵坐标保存为小数类型，这样可以接受小数速度的移动
        self.y = float(self.rect.centery)
        # 设置子弹的速度和颜色
        self.speed = settings.bullet_speed
        self.color = settings.bullet_color

    # 更新子弹的位置，延垂直方向递减
    def update(self, settings):
        # 保证可以接受小数值的速度
        self.y -= self.speed
        self.rect.centery = self.y

    # 在屏幕上绘制子弹
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
