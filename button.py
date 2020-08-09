"""
用于维护按钮类的模块
"""
import pygame


# 按钮的基类，我们可以通过实例化按钮类来创建各种按钮
class Button():
    # 初始化按钮
    def __init__(self, settings, screen, msg):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        # 设置按钮的尺寸
        self.width = 200
        self.height = 50
        # 设置按钮的颜色
        self.button_color = (0, 255, 0)
        # 设置文本的颜色
        self.text_color = (255, 255, 255)
        # 设置文本的字体
        self.font = pygame.font.Font(None, 48)
        # 设置按钮的图像
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 将按钮设置到屏幕中间
        self.rect.center = self.screen_rect.center
        # 将文本渲染成 Surface对象
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # 将文本字符串渲染成一个Surface对象
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # 获取文本的坐标
        self.msg_rect = self.msg_image.get_rect()
        # 将文本位置放到按钮中间
        self.msg_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_rect)
