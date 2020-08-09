"""
创建 Ship 类，负责管理飞船的大部分行为
"""
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    # 初始化飞船，飞船刚出现时，是位于屏幕的中间靠最底边的位置
    def __init__(self, screen, settings):  # 这里需要传入屏幕，是因为我们设置飞船的坐标需要用到屏幕的坐标
        #
        super().__init__()
        # 飞船将来要在哪个屏幕上进行显示
        self.screen = screen

        # 加载飞船显示时的图片资源
        self.image = pygame.image.load('images/ship.bmp')

        # 获取飞船的坐标变量，以便我们之后设置它们
        self.rect = self.image.get_rect()

        # 获取屏幕的坐标，以便我们之后使用它们
        self.screen_rect = screen.get_rect()

        # 设置飞船初始化时的位置，通过屏幕的坐标和尺寸来控制飞船处在屏幕中间靠底的位置
        # 飞船的横坐标 与 屏幕的横坐标相同
        self.rect.centerx = self.screen_rect.centerx

        # 飞船的底边 与 屏幕的底边相同
        self.rect.bottom = self.screen_rect.bottom

        # 飞船移动的速度
        self.speed = settings.ship_speed

        # 通过一个临时属性来为横坐标增加小数值
        self.x = float(self.rect.centerx)

        # 飞船是否向右移动的标志，初始化时为False
        self.moving_right = False

        # 飞船是否向左移动的标志，初始化时为False
        self.moving_left = False

    def blitme(self):
        """
        将飞船显示到屏幕上的方法
        """
        # 通过将飞船图片和飞船坐标传入，以实现在屏幕上显示的目的
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 当飞船正在向右移动时，飞船的横坐标递增 ， 而且需要防止飞船飞出屏幕外
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # 为了能让飞船以小数值的速度飞行，因此使用self.centerx_f来递增坐标
            self.x += self.speed
        # 当飞船正在向左移动时，飞船的横坐标递减 ， 而且需要防止飞船飞出屏幕外
        if self.moving_left and self.rect.left > 0:
            self.x -= self.speed
        # 将根据小数递增的坐标值给到飞船的坐标变量上
        self.rect.centerx = self.x

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
